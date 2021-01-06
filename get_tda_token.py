#!/usr/bin/env python
"""Get a refresh token from TD Ameritrade's API."""

import argparse
import os
import urllib.parse

import requests
import yaml

# The CLIENT_ID comes from the TD Ameritrade developer portal.
#   1. Go to https://developer.tdameritrade.com/
#   2. Set up an account.
#   3. Go to "My Apps" and create an application there.
#   4. Set the redirect URL to https://localhost:8080
#   5. Create the application and copy the "consumer_key" or "client_id".


def main():
    parser = argparse.ArgumentParser(description="Create yaml creds")
    parser.add_argument(
        "-c",
        "--client-id",
        default=os.getenv("TD_CLIENT_ID", None),
        required=True,
        help="TD Ameritrade Client ID",
    )
    parser.add_argument(
        "-p", "--path", default="creds.yaml", help="Path to store creds"
    )
    parser.add_argument(
        "-u",
        "--uri",
        default=os.getenv("TD_REDIRECT_URI", "https://localhost:8080"),
        help="Client Redirect URI",
    )

    args = parser.parse_args()

    client_id = "{}@AMER.OAUTHAP".format(args.client_id)

    params = {
        "client_id": client_id,
        "redirect_uri": args.uri,
        "response_type": "code",
    }

    print(
        'Go here authorize: "https://auth.tdameritrade.com/auth?{}"'.format(
            urllib.parse.urlencode(params)
        )
    )

    code = input("Paste the full URL redirect: ")

    data = {
        "access_type": "offline",
        "client_id": client_id,
        "code": urllib.parse.parse_qsl(code)[0][1],
        "grant_type": "authorization_code",
        "redirect_uri": args.uri,
    }

    response = requests.post(
        "https://api.tdameritrade.com/v1/oauth2/token", data=data
    )

    creds = {
        "client_id": args.client_id,
        "refresh_token": response.json()["refresh_token"],
    }

    with open(args.path, "w+") as fileh:
        yaml.dump(creds, fileh)


if __name__ == "__main__":
    main()
