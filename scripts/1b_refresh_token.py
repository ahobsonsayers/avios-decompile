# 1b_refresh_token.py — Get a new access token using a refresh token
# Run: uv run scripts/api/1b_refresh_token.py
#
# Reads refresh_token from data/auth.json (created by 1_get_token.py).
# Decodes the new JWT for membership number, saves back to data/auth.json.

import os
import json
import base64
from pathlib import Path
import httpx
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_DOMAIN = "accounts.britishairways.com"
AUTH_FILE = Path("data/auth.json")

auth = json.loads(AUTH_FILE.read_text())
refresh_token = auth["refresh_token"]

resp = httpx.post(
    f"https://{AUTH0_DOMAIN}/oauth/token",
    json={
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
    },
)
resp.raise_for_status()
new_tokens = resp.json()

auth["access_token"] = new_tokens["access_token"]
auth["expires_in"] = new_tokens.get("expires_in")
if "refresh_token" in new_tokens:
    auth["refresh_token"] = new_tokens["refresh_token"]
# x_auth_client_id is preserved — already in auth, not overwritten

# Decode membership number from the new JWT
payload = new_tokens["access_token"].split(".")[1]
payload += "=" * (4 - len(payload) % 4)
decoded = json.loads(base64.urlsafe_b64decode(payload))
auth["membership_number"] = decoded["https://avios.com/membership_id"]

AUTH_FILE.write_text(json.dumps(auth, indent=2))
print(f"Refreshed. New access token: {auth['access_token'][:60]}...")
print(f"Expires in: {auth.get('expires_in', 'N/A')}s")
print(f"Saved to {AUTH_FILE}")