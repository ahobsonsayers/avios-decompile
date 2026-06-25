# Rate Limiting & Bot Detection

No confirmed rate limits, but the app makes requests with natural delays. If building
automation:

## Best practices

- **Add random delays** between requests (1-2 seconds)
- **Watch for error responses:**
  - `401` / `403` — token expired or blocked → refresh token
  - `429` — rate limited → stop immediately
  - `5xx` — server error → stop and retry later
- **The availability endpoint returns large responses** (~400KB per route) — don't hammer it
- **Dedupe destinations** before checking — the routes API returns the same destination
  multiple times (once per origin airport). See [Flight Availability](flight-availability.md#routes).