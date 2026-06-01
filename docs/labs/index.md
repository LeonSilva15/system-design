# Labs Guide

This section will explain the learning goals behind runnable labs and connect
lab observations back to architecture decisions.

Runnable lab code lives outside the docs site in the top-level `labs/`
directory.

## Current Labs

| Lab | Focus |
| --- | --- |
| [Token bucket rate limiter](https://github.com/LeonSilva15/system-design/tree/main/labs/rate-limiter/) | burst capacity, refill rate, retry hints, and limiter behavior |
| [Cache-aside demo](https://github.com/LeonSilva15/system-design/tree/main/labs/cache-aside-demo/) | cache miss, hit, TTL, stale data, invalidation, and database fallback |
| [Queue worker demo](https://github.com/LeonSilva15/system-design/tree/main/labs/queue-worker-demo/) | enqueue, worker processing, retry, failure, visibility timeout, and observability |
| [Replication lag simulator](https://github.com/LeonSilva15/system-design/tree/main/labs/replication-lag-simulator/) | leader writes, follower lag, stale reads, and read-your-writes violations |
| [Quorum read/write simulator](https://github.com/LeonSilva15/system-design/tree/main/labs/quorum-read-write-simulator/) | read quorum, write quorum, unavailable replicas, stale reads, and latency trade-offs |
| [Sharding simulator](https://github.com/LeonSilva15/system-design/tree/main/labs/sharding-simulator/) | hash sharding, range sharding, resharding, hot partitions, and cross-shard query limits |
| [Hot-key demo](https://github.com/LeonSilva15/system-design/tree/main/labs/hot-key-demo/) | skewed traffic, overloaded partition or cache key, and mitigation strategies |
| [Log compaction demo](https://github.com/LeonSilva15/system-design/tree/main/labs/log-compaction-demo/) | append-only logs, latest-value compaction, consumer offsets, and retention gaps |
| [Dead-letter queue demo](https://github.com/LeonSilva15/system-design/tree/main/labs/dead-letter-queue-demo/) | poison messages, retry exhaustion, DLQ inspection, replay, and alerting |
| [Retry and idempotency demo](https://github.com/LeonSilva15/system-design/tree/main/labs/retry-idempotency-demo/) | duplicate requests, idempotency keys, duplicate events, and guarded side effects |

Use each lab's `README.md` for setup, commands, expected output, and
what-to-observe guidance.

Use the [challenge progression](../practice/challenge-progression.md) to decide
which lab to run before a related walkthrough.

Return to the [documentation index](../).
