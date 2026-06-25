# 4_flight_availability.py — Check reward seat availability for a route
# Run: uv run scripts/api/4_flight_availability.py

import json
from pathlib import Path
import httpx


AUTH_FILE = Path("data/auth.json")
auth = json.loads(AUTH_FILE.read_text())

MEMBERSHIP_NUMBER = auth["membership_number"]
ORIGIN = "LON"
DESTINATION = "ABV"
ONE_WAY = "false"
ADULTS = "1"

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
    "Origin": ORIGIN,
    "Destination": DESTINATION,
    "OneWay": ONE_WAY,
    "Adults": ADULTS,
    "YoungAdults": "0",
    "Children": "0",
    "Infants": "0",
    "IncludeNonBookableFlights": "true",
}

resp = httpx.get(
    f"{BASE_URL}/spend/v3/programmes/BAEC/GB/{MEMBERSHIP_NUMBER}/flight/availability/allcabins",
    headers=HEADERS,
    params=PARAMS,
)
resp.raise_for_status()
data = resp.json()

high = data["highSeatAvailabilityThreshold"]
med = data["mediumAvailabilityThreshold"]
low = data["lowSeatAvailabilityThreshold"]

for cabin, cabin_data in data["cabinAvailability"].items():
    print(f"\n=== {cabin} ===")
    for direction in ["outbound", "inbound"]:
        flights = cabin_data.get(direction, {}).get("availableFlights", {})
        if not flights:
            continue
        print(f"\n  {direction}:")
        for date_key in sorted(flights):
            for flight in flights[date_key]:
                seats = flight["seats"]
                if seats >= high:
                    colour = "GREEN"
                elif seats >= med:
                    colour = "YELLOW"
                elif seats >= low:
                    colour = "RED"
                else:
                    colour = "---"
                print(
                    f"    {flight['date'][:10]} {flight['time']} "
                    f"seats={seats} {flight['carrier']} "
                    f"{'direct' if flight.get('direct') else '1stop'} "
                    f"{colour}"
                )