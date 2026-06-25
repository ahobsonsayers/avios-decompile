# 5_search_dates.py — Find all destinations from an origin with seats on specific dates
# Run: uv run scripts/api/5_search_dates.py
#
# Calls flight/routes to get all destinations, then checks allcabins
# for each one and filters to your specific dates. Slow (one API call
# per destination) but thorough.

import json
from pathlib import Path
import httpx


AUTH_FILE = Path("data/auth.json")
OUTPUT_FILE = Path("data/search_results.json")
auth = json.loads(AUTH_FILE.read_text())

MEMBERSHIP_NUMBER = auth["membership_number"]
ORIGIN = "LON"
OUTBOUND_DATE = "2026-09-09"
RETURN_DATE = "2026-09-13"
ADULTS = "2"
CABIN = "Economy"  # Economy / Premium / Business / First — change or set to "" for all cabins

import time
import random
from tqdm import tqdm

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

routes_resp = httpx.get(
    f"{BASE_URL}/spend/v3/programmes/BAEC/GB/flight/routes",
    headers=HEADERS,
    params={
        "ByAirport": "true",
        "OriginAirport": ORIGIN,
        "Adults": ADULTS,
        "YoungAdults": "0",
        "Children": "0",
        "Infants": "0",
        "OneWay": "false",
    },
)
routes_resp.raise_for_status()
routes = routes_resp.json()

destinations = []
seen = set()
for origin in routes["origins"]:
    for dest in origin["destinations"]:
        code = dest["destinationAirportCode"]
        if code in seen:
            continue
        seen.add(code)
        destinations.append({
            "code": code,
            "name": dest["destinationName"],
            "country": dest["countryName"],
        })

print(f"Checking {len(destinations)} destinations from {ORIGIN}...\n")

found = []

for dest in tqdm(destinations, desc="Checking routes"):
    code = dest["code"]
    resp = httpx.get(
        f"{BASE_URL}/spend/v3/programmes/BAEC/GB/{MEMBERSHIP_NUMBER}/flight/availability/allcabins",
        headers=HEADERS,
        params={
            "Origin": ORIGIN,
            "Destination": code,
            "OneWay": "false",
            "Adults": ADULTS,
            "YoungAdults": "0",
            "Children": "0",
            "Infants": "0",
            "IncludeNonBookableFlights": "false",
        },
        timeout=30,
    )
    if resp.status_code in (401, 403):
        print(f"\nBlocked! Got {resp.status_code} — your token may have expired or you're being rate-limited.")
        print("Run scripts/api/1b_refresh_token.py then try again.")
        break
    if resp.status_code == 429:
        print(f"\nRate limited (429). Stopping to avoid getting flagged.")
        break
    if resp.status_code >= 500:
        print(f"\nServer error {resp.status_code}. Stopping.")
        break
    if resp.status_code != 200:
        continue
    data = resp.json()
    time.sleep(random.uniform(1, 2))

    cabins = data.get("cabinAvailability")
    if not cabins:
        continue
    if CABIN:
        cabins = {CABIN: cabins.get(CABIN, {})}

    for cabin_name, cabin_data in cabins.items():
        outbound_flights = cabin_data.get("outbound", {}).get("availableFlights", {})
        return_flights = cabin_data.get("inbound", {}).get("availableFlights", {})

        ob_key = f"{OUTBOUND_DATE}T00:00:00"
        ib_key = f"{RETURN_DATE}T00:00:00"

        ob_seats = [f for f in outbound_flights.get(ob_key, []) if f["seats"] >= int(ADULTS)]
        ib_seats = [f for f in return_flights.get(ib_key, []) if f["seats"] >= int(ADULTS)]

        if ob_seats and ib_seats:
            ob = ob_seats[0]
            ib = ib_seats[0]
            found.append({
                "destination": code,
                "destination_name": dest["name"],
                "country": dest["country"],
                "cabin": cabin_name,
                "outbound_time": ob["time"],
                "outbound_seats": ob["seats"],
                "outbound_direct": ob.get("direct", False),
                "outbound_carrier": ob["carrier"],
                "return_time": ib["time"],
                "return_seats": ib["seats"],
                "return_direct": ib.get("direct", False),
                "return_carrier": ib["carrier"],
            })
            print(f"  {code:4} {dest['name']:20} {cabin_name:10}  out {ob['time']} seats={ob['seats']}  ret {ib['time']} seats={ib['seats']}")

print(f"\n{len(found)} route(s) found with seats for {ADULTS} adults on {OUTBOUND_DATE} -> {RETURN_DATE}")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(json.dumps({
    "origin": ORIGIN,
    "outbound_date": OUTBOUND_DATE,
    "return_date": RETURN_DATE,
    "adults": ADULTS,
    "cabin": CABIN,
    "results": found,
}, indent=2))
print(f"\nSaved to {OUTPUT_FILE}")