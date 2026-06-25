# Avios API Documentation

Reverse-engineered from the Avios Android app (`com.usablenet.ba.avios` v5.35.0) via
Hermes bytecode disassembly + live HAR capture.

## Sections

- [Authentication](auth.md) — OAuth2 PKCE flow, token management, auth header quirks
- [Flight Availability](flight-availability.md) — allcabins, routes, broadsearch, bookingurls
- [Flight Alerts](flight-alerts.md) — alert subscriptions (create, list, update, delete)
- [Other Endpoints](other-endpoints.md) — balance, member, collect GraphQL, spend, etc.
- [Rate Limiting](rate-limiting.md) — bot detection, delays, error handling
- [DevCycle](devcycle.md) — feature flags and runtime config

## Quick reference

**Base URL:** See [config.md](config.md) for API URLs.

**Path prefixes:**

| Prefix | Purpose | Auth header |
|---|---|---|
| `spend/v3/` | Flight availability, routes, spend | Raw JWT (no `Bearer `) |
| `whitelabel/v3/` | Home page | Raw JWT (no `Bearer `) |
| `member/v1/` | Balance, details, preferences | `Bearer <jwt>` |
| `collect/v1/` | GraphQL shopping/offers | `Bearer <jwt>` |
| `alerts/v1/` | Flight availability alerts | `Bearer <jwt>` |
| `purchase/v1/` | Buy/boost Avios | `Bearer <jwt>` |
| `goals/v1/` | Savings goals | `Bearer <jwt>` |
| `content/v1/` | External links, screen config | `Bearer <jwt>` |

**Status legend:** Confirmed live = verified with authenticated request/response.
Bytecode = found in Hermes disassembly, params inferred, not yet tested live.