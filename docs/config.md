# Config Reference

All values extracted from `BuildConfig.java` in the decompiled APK. Replace placeholders with values from your own decompilation.

## Programme

| Field | BuildConfig Field |
|---|---|
| Programme Code | `PROGRAMME_CODE` |
| ISO Country | `ISO` |

## Auth0 (OAuth)

| Field | BuildConfig Field |
|---|---|
| Domain | `AUTH0_DOMAIN` |
| Client ID | `AUTH0_CLIENT_ID` |
| Audience | `https://api.avios.com/` (fixed) |

## DevCycle (Feature Flags)

| Field | BuildConfig Field |
|---|---|
| SDK Key | `DVC_CLIENT_SDK_KEY` |
| Endpoint | `https://sdk-api.devcycle.com/v1/sdkConfig` (fixed) |

## API Base URLs

| Service | BuildConfig Field |
|---|---|
| Main API | `BASE_API_URL` |
| GraphQL | `BASE_GRAPHQL_URL` |
| IAGL Service | `IAGL_SERVICE_BASE_URL` |
| AWS Chat | `AWS_CHAT_URL` |
| Mention Me | `MENTION_ME_BASE_API_URL` |

## Third-Party Integrations

| Service | BuildConfig Field |
|---|---|
| Google Maps (Android) | `GOOGLE_MAPS_API_KEY_ANDROID` |
| Google Maps (iOS) | `GOOGLE_MAPS_API_KEY_IOS` |
| ContentSquare | `CONTENT_SQUARE_BASE_URL`, `CONTENT_SQUARE_ID` |
| Datadog | `DATADOG_CLIENT_TOKEN`, `DATADOG_SERVICE`, `DATADOG_SITE`, `DATA_DOG_ENVIRONMENT`, `DATA_DOG_ID` |
| Fidel (Card Linking) | `FIDEL_PROGRAM_ID`, `FIDEL_PUBLISHABLE_KEY` |
| Kameleoon | `KAMELEOON_SITE_CODE` |
| Mention Me | `MENTION_ME_PARTNER_CODE`, `MENTION_ME_SALT` |
| OneTrust | `ONE_TRUST_DOMAIN`, `ONE_TRUST_MOBILE_ID_ANDROID`, `ONE_TRUST_MOBILE_ID_IOS` |
| Sprig | `SPRIG_ENVIRONMENT_ID` |

## Adobe Marketing Cloud

| Field | BuildConfig Field |
|---|---|
| App ID | `MARKETINGCLOUD_APP_ID` |
| Access Token | `MARKETINGCLOUD_ACCESS_TOKEN` |
| MID | `MARKETINGCLOUD_MID` |
| Sender ID | `MARKETINGCLOUD_SENDER_ID` |
| Server URL | `MARKETINGCLOUD_SERVERURL` |

## App Metadata

| Field | BuildConfig Field |
|---|---|
| Package Name | `ANDROID_PACKAGE_NAME` or `APPLICATION_ID` |
| Version | `VERSION_NAME` |
| Build Code | `VERSION_CODE` |
| iOS App ID | `IOS_APP_ID` |