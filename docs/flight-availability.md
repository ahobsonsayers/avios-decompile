# Flight Availability

Reward flight seat availability endpoints. All under `spend/v3/` — uses **raw JWT**
auth (no `Bearer ` prefix). See [Authentication](auth.md).

## 1. All-cabin availability (Confirmed live)

Returns seat availability across all cabins for a route, for the full 355-day booking
window. This powers the destinations colour-heatmap view in the app.

```
GET /spend/v3/programmes/BAEC/GB/{MEMBERSHIP_NUMBER}/flight/availability/allcabins
```

**Query params (capitalised):**

| Param | Example | Notes |
|---|---|---|
| `Origin` | `LON` | IATA airport or city code |
| `Destination` | `ABV` | IATA airport or city code |
| `OneWay` | `false` | `true` or `false` |
| `Adults` | `1` | |
| `YoungAdults` | `0` | |
| `Children` | `0` | |
| `Infants` | `0` | |
| `IncludeNonBookableFlights` | `true` | Include flights with 0 seats |

**Response:**

```json
{
  "origin": {"code": "LON", "name": ""},
  "destination": {"code": "ABV", "name": ""},
  "highSeatAvailabilityThreshold": 9,
  "mediumAvailabilityThreshold": 5,
  "lowSeatAvailabilityThreshold": 1,
  "cabinAvailability": {
    "Economy": {
      "outbound": {
        "fromAvios": 0,
        "availabilityFrom": "2026-06-23T00:00:00+00:00",
        "availabilityTo": "2027-06-21T00:00:00+00:00",
        "availableFlights": {
          "2026-06-23T00:00:00": [
            {
              "date": "2026-06-23T22:30:00",
              "time": "22:30",
              "peak": true,
              "direct": true,
              "avios": 0,
              "seats": 9,
              "carrier": "BA"
            }
          ]
        }
      },
      "inbound": { "..." }
    },
    "Premium": { "..." },
    "Business": { "..." },
    "First": { "..." }
  }
}
```

**Seat thresholds (colour mapping):**
- `seats >= 9` → green (high)
- `seats >= 5` → medium
- `seats >= 1` → low
- `seats == 0` → none

## 2. Routes (Confirmed live)

Returns all reward-flight destinations from an origin, with Avios price ranges per cabin
and continent categories. Powers the "explore destinations" list.

```
GET /spend/v3/programmes/BAEC/GB/flight/routes
```

**Query params:**

| Param | Example | Notes |
|---|---|---|
| `ByAirport` | `true` | Group by airport |
| `OriginAirport` | `LON` | IATA code (optional — omit for all origins) |
| `Adults` | `1` | |
| `YoungAdults` | `0` | |
| `Children` | `0` | |
| `Infants` | `0` | |
| `OneWay` | `false` | |
| `DateFrom` | `2026-06-01` | Optional date filter |
| `DateTo` | `2027-05-31` | Optional date filter |

**Response includes:**
- `origins[].destinations[]` — each destination has:
  - `destinationAirportCode` — IATA code (e.g. `KLX`)
  - `destinationAirportName` — full airport name
  - `destinationName` — city name (e.g. `Kalamata`)
  - `countryCode` / `countryName` — country (e.g. `GR` / `Greece`)
  - `broadSearchCategories` — continent/area category (e.g. `["Mediterranean"]`)
  - `aviosPerCabinClass` — min/max Avios per cabin
  - `flownByPartners` — carrier codes (e.g. `["BA"]`)
- `broadSearchCategories` — continent list with destination counts and price ranges

**Note:** The same destination appears multiple times (once per London airport — LHR, LGW,
LCY). Dedupe by `destinationAirportCode` when iterating.

**Continent categories:**
Asia & Oceania, South Europe, South & Central America, Caribbean, Africa,
Northern Europe, Eastern Europe, Mediterranean, Central Europe, United Kingdom,
Western Europe, Middle East, North America

**Note:** BA's grouping is loose — e.g. Milan is in "Mediterranean" alongside actual
Mediterranean destinations like Kalamata and Corfu.

## 3. Broad search (Bytecode — unconfirmed)

Search availability across a date range for a specific cabin class. Found in the
bytecode — params inferred from disassembly, not yet confirmed with a live request.

```
GET /spend/v3/programmes/BAEC/GB/{MEMBERSHIP_NUMBER}/flight/availability/broadsearch
```

| Param | Notes |
|---|---|
| `Origin` | IATA code |
| `Destination` | IATA code |
| `Adults`, `YoungAdults`, `Children`, `Infants` | counts |
| `OneWay` | boolean |
| `StartMonth` | e.g. `2026-09` |
| `EndMonth` | e.g. `2026-10` |
| `CabinClass` | `economy`/`premium`/`business`/`first` |
| `Category` | `reward` |

## 4. Booking URLs (Bytecode — unconfirmed)

Deep links to BA booking for available flights. Same params as allcabins. Found in
bytecode — not yet confirmed with a live request.

```
GET /spend/v3/programmes/BAEC/GB/{MEMBERSHIP_NUMBER}/flight/availability/bookingurls
```