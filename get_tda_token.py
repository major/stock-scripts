#!/usr/bin/env python
"""Get a refresh token from TD Ameritrade's API."""
import yaml

import tdameritrade as td

# The CLIENT_ID comes from the TD Ameritrade developer portal.
#   1. Go to https://developer.tdameritrade.com/
#   2. Set up an account.
#   3. Go to "My Apps" and create an application there.
#   4. Set the redirect URL to https://localhost:8080
#   5. Create the application and copy the "consumer_key" or "client_id".
CLIENT_ID = ""
REDIRECT_URI = "https://localhost:8080"

result = td.auth.authentication(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI
)

creds = {
    "client_id": CLIENT_ID,
    "refresh_token": result['refresh_token']
}
with open("creds.yaml", "w+") as fileh:
    yaml.dump(creds, fileh)
