# Labs Guide

This section will explain the learning goals behind runnable labs and connect
lab observations back to architecture decisions.

Runnable lab code lives outside the docs site in the top-level `labs/`
directory.

## Current Labs

| Lab | Focus |
| --- | --- |
| [Token bucket rate limiter](../../labs/rate-limiter/) | burst capacity, refill rate, retry hints, and limiter behavior |
| [Cache-aside demo](../../labs/cache-aside-demo/) | cache miss, hit, TTL, stale data, invalidation, and database fallback |
| [Retry and idempotency demo](../../labs/retry-idempotency-demo/) | duplicate requests, idempotency keys, duplicate events, and guarded side effects |

Use each lab's `README.md` for setup, commands, expected output, and
what-to-observe guidance.

Return to the [documentation index](../).
