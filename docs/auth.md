# Authentication

OAuth2 Authorization Code with PKCE via Auth0.

## Config

See [config.md](config.md) for how to obtain these values.

| Field | Value |
|---|---|
| Domain | `accounts.britishairways.com` |
| Token endpoint | `https://accounts.britishairways.com/oauth/token` |
| Authorize endpoint | `https://accounts.britishairways.com/authorize` |
| Audience | `https://api.avios.com/` |
| Scopes | `openid profile email read:transaction read:member read:account offline_access` |
| Token lifetime | ~24h (access), longer (refresh) |

## Auth header format differs per slice

The `spend/v3/` and `whitelabel/v3/` endpoints want the **raw JWT** (no `Bearer ` prefix).
All other slices (`member`, `collect`, `alerts`, `content`, `purchase`, `goals`) use
`Bearer <token>`.

Confirmed from the HAR capture — the app sends the header differently depending on the
API slice. See [README.md](README.md) for which prefix each slice uses.

## Flow

1. App opens browser to `/authorize` with `client_id`, `response_type=code`, PKCE
   `code_challenge`/`code_challenge_method=S256`, `scope`, `audience`, `redirect_uri`.
2. User logs in with BA Executive Club credentials.
3. Auth0 redirects back with an authorization code.
4. App POSTs `grant_type=authorization_code` + code + PKCE verifier to `/oauth/token`.
5. Receives `access_token` + `refresh_token` + `id_token`.
6. Access token sent on all API requests (raw or `Bearer ` depending on slice — see above).
7. When expired, POSTs `grant_type=refresh_token` to `/oauth/token` for a new access token.

## Token claims (decoded JWT)

```json
{
  "https://avios.com/membership_id": "05608372",
  "https://avios.com/membership_type": "BAEC",
  "iss": "https://accounts.britishairways.com/",
  "aud": ["https://api.avios.com/", "https://ba-prod.eu.auth0.com/userinfo"],
  "azp": "{AUTH0_CLIENT_ID}",
  "scope": "openid profile email read:transaction read:member read:account offline_access"
}
```

## Required headers (all requests)

| Header | Value | Notes |
|---|---|---|
| `Authorization` | raw JWT or `Bearer <jwt>` | See above — differs per slice |
| `x-api-programme` | `BAEC` | British Airways Executive Club |
| `x-api-iso` | `GB` | Country ISO code |
| `x-auth-type` | `access_token` | |
| `x-api-version` | `3.2.0` | |
| `x-auth-client-id` | `BAEC-<uuid>` | Generated per install (random UUID) |
| `x-api-key` | `unused` | Legacy header, always literal "unused" |
| `accept` | `application/json` | |
| `user-agent` | `android;V5.35.0 Build:22340160-RN` | |

## Getting a token

OAuth2 PKCE flow via the Auth0 authorize + token endpoints. Access token ~24h,
refresh token lasts longer. `offline_access` scope required for refresh tokens.