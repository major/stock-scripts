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
# To create a configuration file, add a small json file into ~/.robinhood.json
# that contains the following:
#
# {
#   "login": "",
#   "password": "",
#   "totp": ""
# }
#
# Your login/password are what you normally use to login at robinhood.com. The
# TOTP is your alphanumberic 2FA token. This is displayed when you first
# configure 2FA at Robinhood.
#
import argparse
from datetime import datetime
import json
import logging
import os
import sys

import pyotp
import robin_stocks as r
from tabulate import tabulate

logging.basicConfig(level=logging.INFO)


def get_days_to_expiration(expiration_date):
    """Calculate the days between today and the option expiration date."""
    expiry = datetime.strptime(expiration_date, "%Y-%m-%d")
    time_left = datetime.now() - expiry
    return abs(time_left.days)


# Parse the arguments.
parser = argparse.ArgumentParser(
    description="Find options that meet an annual rate of return requirement",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
    default=20
)
parser.add_argument(
    "--dte-max",
    type=int,
    help="Maximum days until expiration",
    default=60
)
parser.add_argument(
    "ticker",
    help="Stock ticker symbol",
    default="GME"
)
args = parser.parse_args()

# Read the Robinhood configuration.
CONFIG_FILE = os.path.expanduser("~/.robinhood.json")
with open(CONFIG_FILE, 'r') as fileh:
    config = json.loads(fileh.read())

totp = pyotp.TOTP(config['totp']).now()
login = r.login(config['login'], config['password'], mfa_code=totp)

# Check if the ticker exists.
if r.stocks.get_fundamentals(args.ticker) == [None]:
    sys.exit(f"Cound not find ticker: {args.ticker}")

# Find all option expiration dates which are within our DTE requirement.
valid_expiration_dates = [
    x for x in r.options.get_chains(args.ticker)['expiration_dates']
    if get_days_to_expiration(x) <= args.dte_max
]


# Set up our variables that hold option data.
option_data = []
low_return_counter = 0

# Loop over each expiration date to retrieve options.
for expiration_date in valid_expiration_dates:
    logging.info(f"Getting {args.ticker} options for {expiration_date}")

    options = r.find_options_by_expiration(
        args.ticker,
        expirationDate=expiration_date,
        optionType="put"
    )

    for opt in options:
        # Get all of the options on the expiration date for this ticker.
        dte = get_days_to_expiration(opt["expiration_date"])

        # Sometimes Robinhood says that delta is None. 🤷🏻‍♂️
        delta = 0
        if opt['delta']:
            delta = float(opt['delta'].replace('-', ''))

        # Do the math for our return and annualized return.
        bid_price = float(opt['bid_price'])
        strike_price = float(opt['strike_price'])
        put_return = (bid_price / (strike_price - bid_price))
        annual_return = put_return / dte * 365

        # Skip this one if the percent of profit does not meet our spec.
        if not opt['chance_of_profit_short']:
            continue
        chance_of_profit = float(opt['chance_of_profit_short'])
        if chance_of_profit < (args.pop_min / 100):
            continue
        if chance_of_profit > (args.pop_max / 100):
            continue

        # Skip this one if the annual return is below our threshold.
        if annual_return < (args.min_return / 100):
            low_return_counter += 1
            continue

        # Add this data to our table.
        option_data.append(
            [
                opt["chain_symbol"],
                opt["strike_price"],
                opt["expiration_date"],
                dte,
                f"{chance_of_profit * 100:.1f}",
                f"{delta:.2f}",
                f"{put_return * 100:.1f}",
                f"{annual_return * 100:.1f}",
            ]
        )

# Sort by the annual return column.
option_data.sort(key=lambda x: float(x[7]), reverse=True)

# Add our table headers.
headers = [
    "",
    "Strike",
    "Exp Date",
    "DTE",
    "PoP %",
    "Delta",
    "Ret. %",
    "Annual % ",
]

# Print our table.
table = tabulate(option_data, headers=headers, tablefmt="github")
print(table)

# Show if we had extra options that didn't meet our annual return requirement.
print(
    "\n"
    f"Options found below annual return threshold of {args.min_return}%: "
    f"{low_return_counter}"
)
