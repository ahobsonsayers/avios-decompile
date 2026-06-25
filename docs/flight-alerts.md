# Flight Availability Alerts

Notification-subscription service — "tell me when reward seats appear on a route."
Uses `Bearer` auth. See [Authentication](auth.md).

## Endpoints

| Method | Path | Status | Purpose |
|---|---|---|---|
| GET | `/alerts/v1/flights/availability/alerts` | Confirmed live | List your alerts |
| GET | `/alerts/v1/flights/availability/alerts/available-count` | Confirmed live | Count of alerts you can set |
| GET | `/alerts/v1/flights/availability/alert/{alertId}` | Bytecode | Get a specific alert |
| POST | `/alerts/v1/flights/availability/alert` | Bytecode | Create an alert |
| PATCH | `/alerts/v1/flights/availability/alert/{alertId}` | Bytecode | Update an alert |
| POST | `/alerts/v1/flights/availability/alerts/viewed-available` | Bytecode | Mark alerts as viewed |
| DELETE | `/alerts/v1/flights/availability/alerts/delete-expired` | Bytecode | Delete expired alerts |

## Create alert body (inferred from bytecode strings)

```json
{
  "originAirportCode": "LON",
  "destinationAirportCode": "ABV",
  "cabinClass": "economy",
  "oneWay": false,
  "adults": 1,
  "youngAdults": 0,
  "children": 0,
  "infants": 0,
  "outboundDate": "2026-09-09",
  "inboundDate": "2026-09-13",
  "notificationType": "..."
}
```

## Live responses (from HAR capture)

**List alerts:**
```json
{"alerts":[]}
```

**Available count:**
```json
{"total":0}
```