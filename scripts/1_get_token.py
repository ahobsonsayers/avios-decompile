# 1_get_token.py — Get a new Auth0 access token via PKCE
# Run: uv run scripts/api/1_get_token.py
#
# Opens a browser for you to log into BA Executive Club.
# After login, exchanges the code for tokens, decodes the membership number
# from the JWT, and saves everything to data/auth.json.

import os
import uuid
import http.server
import secrets
import hashlib
import base64
import urllib.parse
import json
import webbrowser
from pathlib import Path
import httpx
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_DOMAIN = "accounts.britishairways.com"
REDIRECT_URI = "http://localhost:8484/callback"
AUDIENCE = "https://api.avios.com/"
SCOPE = "openid profile email read:transaction read:member read:account offline_access"
PORT = 8484
AUTH_FILE = Path("data/auth.json")
PROGRAMME = "BAEC"

verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(
    hashlib.sha256(verifier.encode()).digest()
).rstrip(b"=").decode()

params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "code_challenge": challenge,
    "code_challenge_method": "S256",
    "scope": SCOPE,
    "audience": AUDIENCE,
    "redirect_uri": REDIRECT_URI,
}
auth_url = f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(params)}"
print(f"Opening browser for login...\n{auth_url}\n")
webbrowser.open(auth_url)

auth_code = None

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urllib.parse.urlparse(self.path).query
        parsed = urllib.parse.parse_qs(query)
        auth_code = parsed.get("code", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Done! You can close this tab.</h1>")
    def log_message(self, *args):
        pass

server = http.server.HTTPServer(("localhost", PORT), Handler)
server.handle_request()

if not auth_code:
    print("No auth code received.")
    exit(1)

print("Got auth code, exchanging for token...")
resp = httpx.post(
    f"https://{AUTH0_DOMAIN}/oauth/token",
    json={
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": auth_code,
        "code_verifier": verifier,
        "redirect_uri": REDIRECT_URI,
    },
)
resp.raise_for_status()
tokens = resp.json()

# Decode membership number from the JWT
payload = tokens["access_token"].split(".")[1]
payload += "=" * (4 - len(payload) % 4)
decoded = json.loads(base64.urlsafe_b64decode(payload))
tokens["membership_number"] = decoded["https://avios.com/membership_id"]

# Generate x-auth-client-id if not already saved (app generates a random UUID per install)
if AUTH_FILE.exists():
    existing = json.loads(AUTH_FILE.read_text())
    tokens["x_auth_client_id"] = existing.get("x_auth_client_id", f"{PROGRAMME}-{uuid.uuid4()}")
else:
    tokens["x_auth_client_id"] = f"{PROGRAMME}-{uuid.uuid4()}"

AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
AUTH_FILE.write_text(json.dumps(tokens, indent=2))

print(f"ACCESS_TOKEN: {tokens['access_token'][:60]}...")
print(f"REFRESH_TOKEN: {tokens.get('refresh_token', 'N/A')[:20]}...")
print(f"MEMBERSHIP_NUMBER: {tokens['membership_number']}")
print(f"X_AUTH_CLIENT_ID: {tokens['x_auth_client_id']}")
print(f"EXPIRES_IN: {tokens.get('expires_in', 'N/A')}s")
print(f"Saved to {AUTH_FILE}")