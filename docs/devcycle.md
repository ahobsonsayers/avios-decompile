# DevCycle (Feature Flags)

The app fetches feature flags from DevCycle at startup. These control UI visibility, not
API access — all endpoints work regardless of flag values.

## Config

See [config.md](config.md) for how to obtain these values.

| Field | Value |
|---|---|
| Endpoint | `https://sdk-api.devcycle.com/v1/sdkConfig` |
| Params | `sdkKey`, `user_id`, `isAnonymous`, `appVersion`, `appBuild`, `customData` (programme/iso/platform) |

```
GET https://sdk-api.devcycle.com/v1/sdkConfig?sdkKey={DVC_CLIENT_SDK_KEY}&user_id={MEMBERSHIP_NUMBER}&isAnonymous=false&appVersion=5.35.0&...
```

Returns JSON with `variables` (feature flags), `features`, and `settings`.

## Flight-related flags

| Flag | Type | Purpose |
|---|---|---|
| `broad-search` | Boolean | Broad search feature |
| `reward-flights-education` | Boolean | Reward flight education UI |
| `new-flights-redemption-flow` | Boolean | New redemption flow UI |
| `flight-finder-enabled` | Boolean | Flight finder visibility |
| `spend-tab-enabled` | Boolean | Spend tab visibility |
| `flight-alerts` | Boolean | Flight alerts feature |
| `new-calendar` | Boolean | New calendar UI |

## Other flags

`avios-rebrand`, `goals`, `onboarding`, `collect-special-offers`, `nearby-offers`,
`card-linking`, `referrals-*`, `home-page-evolution`, `purchase-avios-native`,
`member-api`, `aws-chat-v2`, `one-trust`, etc. All booleans controlling UI.

## API base URLs

The app uses a single hardcoded base URL. See [config.md](config.md) for the API URL.
The `*ApiBase` reducer names (whitelabelApiBase, spendApiBase, memberApiBase, etc.) are Redux slice names, not separate hosts.