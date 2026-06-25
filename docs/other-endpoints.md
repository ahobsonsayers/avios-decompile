# Other Endpoints

Non-flight endpoints discovered in the HAR capture. All use `Bearer` auth unless noted.
See [Authentication](auth.md).

## Member

| Method | Path | Purpose |
|---|---|---|
| GET | `/member/v1/balance` | Avios balance: `{"availableAvios":53231,"isHousehold":false}` |
| GET | `/member/v1/details?isFirstTimeLogin=false` | Member details |
| GET | `/member/v1/actions/suggestedactions` | Suggested actions |
| GET | `/member/v1/message` | Messages |
| GET | `/member/v1/cpm` | CPM data |
| GET | `/member/v1/preferences/notificationspreferences` | Notification preferences |
| GET | `/member/v1/preferences/notificationspreferences/settings/opt-in-screen` | Opt-in screen |
| GET | `/member/v1/preferences/flight-alerts/terms-and-conditions` | Flight alert T&Cs |
| POST | `/member/v1/memberdevice/update` | Update device registration |

## Collect (GraphQL)

```
GET /collect/v1/graphql?operationName={NAME}&extensions={"persistedQuery":{"version":1,"sha256Hash":"{HASH}"}}
```

61 GraphQL operations for shopping/offers/favourites/linked-cards. Uses persisted queries
(pre-computed hashes) — no inline query strings. Examples:

- `GetHomeHighlights`, `GetFsCarousel`, `GetTopOffersRecommended`
- `GetRecentlyVisitedOfferList`, `GetFavoriteOfferIds`
- `GetCollectConfiguration`, `GetMemberOfferTags`
- `GetCategories`

## Spend

| Method | Path | Purpose | Auth |
|---|---|---|---|
| GET | `/spend/v3/programmes/BAEC/GB/spend` | Spend tab content | Raw JWT |
| GET | `/spend/v3/programmes/BAEC/GB/flight/routes` | See [Flight Availability](flight-availability.md) | Raw JWT |
| GET | `/spend/v3/programmes/BAEC/GB/{MEMBERSHIP}/flight/availability/allcabins` | See [Flight Availability](flight-availability.md) | Raw JWT |

## Whitelabel

| Method | Path | Purpose | Auth |
|---|---|---|---|
| GET | `/whitelabel/v3/programmes/BAEC/GB/home/{MEMBERSHIP_NUMBER}` | Home page content + flight offers | Raw JWT |

## Purchase

| Method | Path | Purpose |
|---|---|---|
| GET | `/purchase/v1/users/current` | Current user |
| GET | `/purchase/v1/purchase/boost/options` | Avios boost purchase options |
| GET | `/purchase/v1/purchase/boost/available` | Available boost options |

## Goals

| Method | Path | Purpose |
|---|---|---|
| GET | `/goals/v1/member?PageNumber=1&PageSize=1` | Savings goals |

## Content

| Method | Path | Purpose |
|---|---|---|
| GET | `/content/v1/config` | App config |
| GET | `/content/v1/screen?type=HomeScreen` | Screen content |
| GET | `/content/v1/externallink/sidemenu` | Side menu links |