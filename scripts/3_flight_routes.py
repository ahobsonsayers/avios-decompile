# 3_flight_routes.py — Get all reward flight destinations from an origin
# Run: uv run scripts/api/3_flight_routes.py

import json
from pathlib import Path
import httpx


AUTH_FILE = Path("data/auth.json")
auth = json.loads(AUTH_FILE.read_text())

ORIGIN_AIRPORT = "LON"

BASE_URL = "https://api.rewardsapp.iagl.digital"
HEADERS = {
    "Authorization": auth["access_token"],
    "x-api-programme": "BAEC",
    "x-api-iso": "GB",
    "x-auth-type": "access_token",
    "x-api-version": "3.2.0",
    "x-auth-client-id": auth["x_auth_client_id"],
    "x-api-key": "unused",
    "accept": "application/json",
    "user-agent": "android;V5.35.0 Build:22340160-RN",
}
PARAMS = {
    "ByAirport": "true",
    "OriginAirport": ORIGIN_AIRPORT,
    "Adults": "1",
    "YoungAdults": "0",
    "Children": "0",
    "Infants": "0",
    "OneWay": "false",
}

resp = httpx.get(
    f"{BASE_URL}/spend/v3/programmes/BAEC/GB/flight/routes",
    headers=HEADERS,
    params=PARAMS,
)
resp.raise_for_status()
data = resp.json()

for origin in data["origins"]:
    for dest in origin["destinations"]:
        prices = dest["aviosPerCabinClass"]
        print(
            f"{origin['originAirportCode']} -> {dest['destinationAirportCode']} "
            f"({dest['destinationName']}, {dest['countryName']})  "
            f"Eco {prices['Economy']['min']}-{prices['Economy']['max']}  "
            f"Bus {prices['Business']['min']}-{prices['Business']['max']}"
        )