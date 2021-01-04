#!/usr/bin/env python
"""Get option trades that meet annual return requirements."""
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# To set up TDA's authentication, use the simple script and instructions here:
# https://github.com/areed1192/td-ameritrade-python-api#api-key-and-credentials
#
# Create a creds.yaml that contains two keys:
#   client_id: From your developer account
#   refresh_token: From the authentication step above
#
import argparse
import datetime as dt
import sys
import yaml

import pandas as pd
import tdameritrade as td


def get_returns(bid, strike_price, dte):
    """Calculate return and annual return for a sold option."""
    put_return = (bid / (strike_price - bid) * 100)
    annual_return = put_return / dte * 365
    return (round(put_return, 1), round(annual_return, 1))


# Parse the arguments.
parser = argparse.ArgumentParser(
    description="Find options that meet an annual rate of return requirement",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--credentials-path",
    default="./creds.yaml",
    help="TD Ameritrade Credentials Path",
)
parser.add_argument(
    "--pop-min",
    type=int,
    help="Minimum percent chance of profit",
    default=70
)
parser.add_argument(
    "--pop-max",
    type=int,
    help="Maximum percent chance of profit",
    default=90
)
parser.add_argument(
    "--min-return",
    type=int,
    help="Minimum annual return percentage",
    default=20,
)
parser.add_argument(
    "--dte-max",
    type=int,
    help="Maximum days until expiration",
    default=60
)
parser.add_argument("ticker", help="Stock ticker symbol", default="GME")
args = parser.parse_args()


def main():
    # Read TDA credentials file.
    with open(args.credentials_path, "r") as fileh:
        config = yaml.safe_load(fileh.read())

    # Connect to TDA's API.
    client = td.TDClient(
        client_id=config["client_id"],
        refresh_token=config["refresh_token"]
    )

    # Set the max DTE for options chains.
    max_exp = dt.datetime.now() + dt.timedelta(days=args.dte_max)

    # Get the options chain as a pandas dataframe. (Thanks dobby. 🤗)
    try:
        options = client.optionsDF(
            args.ticker,
            contractType="PUT",
            includeQuotes=True,
            toDate=max_exp.strftime("%Y-%m-%d"),
            optionType="S",
        )
    except KeyError:
        sys.exit(f"Could not find ticker: {args.ticker}")

    # Calculate a return for the trade and an annualized return.
    options["putReturn"], options['annualReturn'] = get_returns(
        options['bid'],
        options['strikePrice'],
        options["daysToExpiration"]
    )

    # Handle situations where 'delta' is NaN for a certain strike. Usually all
    # of the greeks are missing for these.
    options["delta"] = pd.to_numeric(options["delta"], errors="coerce")

    # Calculate PoP based on the delta.
    options["pop"] = (1 - options['delta'].abs()) * 100

    # Remove the time of day information from the expiration date.
    options['expirationDate'] = options['expirationDate'].dt.strftime(
        "%Y-%m-%d"
    )

    # Select options that meet all of our requirements.
    selected = options[
        (options["annualReturn"] >= args.min_return)
        & (args.pop_min <= options["pop"])
        & (options["pop"] <= args.pop_max)
    ].sort_values('annualReturn', ascending=False)

    # Create a view with the columns we care about.
    view = selected[
        [
            "symbol",
            "strikePrice",
            "expirationDate",
            "daysToExpiration",
            "bid",
            "pop",
            "putReturn",
            "annualReturn",
        ]
    ]
    print(
        view.rename(
            columns={
                "symbol": "💸",
                "strikePrice": "Strike",
                "expirationDate": "Exp Date",
                "daysToExpiration": "DTE",
                "bid": "Bid",
                "pop": "PoP %",
                "putReturn": "Ret. %",
                "annualReturn": "Annual %",
            }
        ).to_markdown(index=False)
    )

if __name__ == "__main__":
    main()
