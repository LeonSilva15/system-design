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
| [Queue worker demo](../../labs/queue-worker-demo/) | enqueue, worker processing, retry, failure, visibility timeout, and observability |
| [Replication lag simulator](../../labs/replication-lag-simulator/) | leader writes, follower lag, stale reads, and read-your-writes violations |
| [Quorum read/write simulator](../../labs/quorum-read-write-simulator/) | read quorum, write quorum, unavailable replicas, stale reads, and latency trade-offs |
| [Sharding simulator](../../labs/sharding-simulator/) | hash sharding, range sharding, resharding, hot partitions, and cross-shard query limits |
| [Hot-key demo](../../labs/hot-key-demo/) | skewed traffic, overloaded partition or cache key, and mitigation strategies |
| [Retry and idempotency demo](../../labs/retry-idempotency-demo/) | duplicate requests, idempotency keys, duplicate events, and guarded side effects |

Use each lab's `README.md` for setup, commands, expected output, and
what-to-observe guidance.

Return to the [documentation index](../).
