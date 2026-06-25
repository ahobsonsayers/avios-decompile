# 2_check_balance.py — Check your Avios balance
# Run: uv run scripts/api/2_check_balance.py

import json
from pathlib import Path
import httpx


AUTH_FILE = Path("data/auth.json")
auth = json.loads(AUTH_FILE.read_text())

BASE_URL = "https://api.rewardsapp.iagl.digital"
HEADERS = {
    "Authorization": f"Bearer {auth['access_token']}",
    "x-api-programme": "BAEC",
    "x-api-iso": "GB",
    "x-auth-type": "access_token",
    "x-api-version": "3.2.0",
    "x-auth-client-id": auth["x_auth_client_id"],
    "x-api-key": "unused",
    "accept": "application/json",
    "user-agent": "android;V5.35.0 Build:22340160-RN",
}

resp = httpx.get(f"{BASE_URL}/member/v1/balance", headers=HEADERS)
resp.raise_for_status()
print(resp.json())