# Component Metrics Catalog

This catalog lists useful metric families for common system components. Use it
as a starting point when designing dashboards, alerts, SLOs, runbooks, and
capacity plans.

Do not instrument every metric by default. Start from the workflow, choose the
signals that explain user-visible health, and add component metrics that help a
responder find the likely cause.

Use [Metrics](metrics.md) for metric selection principles,
[Dashboards](dashboards.md) for layout, [Alerting](alerting.md) for paging
rules, and [Capacity planning](capacity-planning.md) for growth triggers.

## Purpose

Use this catalog to answer:

- Which metrics should an API, database, cache, queue, worker, search index,
  CDN, or object store expose?
- Which metrics show symptoms, and which metrics explain causes?
- Which dimensions are safe and useful for routing and diagnosis?
- Which metrics should appear on dashboards, alerts, SLO reviews, runbooks, or
  capacity reviews?
- Which metrics create cost, cardinality, or privacy risk?

The goal is practical coverage, not exhaustive telemetry.

## How To Use This Catalog

For each component, choose:

- one or two workflow health signals;
- request, error, latency, and saturation signals where applicable;
- backlog, freshness, durability, quota, or cost signals when those risks
  exist;
- bounded dimensions such as route template, result class, region, tenant tier,
  dependency name, queue name, job type, cache name, or object class;
- a dashboard panel, alert, SLO, runbook, or capacity trigger that will use the
  metric.

Avoid high-cardinality labels such as raw URL, user ID, email address, session
ID, request ID, object key, cache key, search query, stack trace, or raw error
message. Use [Logs](logs.md) and [Tracing](tracing.md) for single-request
debugging.

## API And Service Metrics

APIs should show whether callers can complete the request path and which routes
are failing, slow, or saturated.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Traffic | requests per second, accepted requests, rejected requests, throttled requests | Baseline for capacity, error rate, and cost |
| Success and errors | success rate, error rate by result class, validation failures, auth failures, conflict outcomes, dependency failures | Separates user mistakes from system defects |
| Latency | p50, p95, p99 end-to-end latency by route or command | Shows user experience and tail behavior |
| Saturation | request concurrency, worker/thread pool use, open connections, in-flight requests | Explains rising latency and rejections |
| Payload shape | request size, response size, compression ratio | Reveals bandwidth, serialization, and memory pressure |
| Dependency calls | calls per dependency, timeout rate, retry count, fallback count | Connects API symptoms to downstream causes |

Useful dimensions:

- route template or command name;
- result class;
- tenant tier or region;
- dependency name;
- client type when safe and bounded.

Related pages:

- [Metrics](metrics.md)
- [Alerting](alerting.md)
- [Retries](../reliability/retries.md)
- [Bottleneck analysis](../scalability/bottleneck-analysis.md)

## Database Metrics

Database metrics should show whether the source of truth can keep up with the
read, write, transaction, backup, and recovery expectations of the workflow.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Query traffic | queries per second by query family, reads versus writes | Identifies dominant access paths |
| Query latency | p50, p95, p99 query duration by operation class | Shows slow paths before API latency hides them |
| Connections | active, idle, waiting, pool exhaustion | Explains request queueing and timeouts |
| Locks and transactions | lock wait time, transaction duration, deadlocks, conflict retries | Reveals write contention and correctness pressure |
| Rows and indexes | rows scanned, rows returned, index size, index hit rate | Shows missing indexes or inefficient access paths |
| Replication and recovery | replication lag, backup age, backup duration, restore-test age | Protects freshness and durability expectations |
| Storage growth | data size, index size, write-ahead log size, free space | Supports retention, cost, and capacity planning |

Useful dimensions:

- query family or operation name;
- table or logical data area;
- result class;
- primary versus replica;
- region or tenant tier when the deployment supports it.

Related pages:

- [Indexes](../data/indexes.md)
- [Transactions](../data/transactions.md)
- [Backups and restore](../data/backups-and-restore.md)
- [Database read scaling](../scalability/database-read-scaling.md)
- [Capacity planning](capacity-planning.md)

## Cache Metrics

Cache metrics should prove that the cache reduces load without hiding stale,
incorrect, or unauthorized data.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Hit and miss | hit rate, miss rate, bypass count | Shows whether the cache is useful |
| Latency | lookup latency, fallback latency, fill latency | Separates cache speed from source-of-truth speed |
| Eviction and memory | memory use, item count, eviction rate, hot key count | Reveals saturation and churn |
| Freshness | key age, refresh age, stale-read count, invalidation failure count | Shows correctness risk |
| Source pressure | database load after misses, cache stampede count, fill error count | Detects cache failures that move load downstream |
| Availability | cache connection errors, timeout rate, fallback use | Shows whether cache failure affects users |

Useful dimensions:

- cache name;
- read path;
- result class;
- tenant tier or region;
- bounded key category, not full key.

Related pages:

- [Metrics](metrics.md)
- [Bottleneck analysis](../scalability/bottleneck-analysis.md)
- [Graceful degradation](../reliability/graceful-degradation.md)

## Queue And Stream Metrics

Queue and stream metrics should show whether asynchronous work is keeping up
with freshness, ordering, retry, and failure expectations.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Arrival and drain | enqueue rate, dequeue rate, publish rate, consume rate | Shows whether work is arriving faster than it drains |
| Backlog | depth, oldest age, age percentiles, consumer lag | Age often maps better to user impact than depth |
| Processing | processing duration, batch size, handler success rate | Shows worker throughput and slow job types |
| Retries | retry count, retry age, retry exhaustion, backoff delay | Reveals poison messages and dependency failure |
| Dead letters | dead-letter count, quarantine count, replay count | Tracks work that needs repair |
| Ordering and duplication | duplicate detection count, out-of-order count, idempotency conflict count | Protects correctness-sensitive workflows |

Useful dimensions:

- queue or stream name;
- job or message type;
- priority;
- result class;
- dependency name;
- tenant tier or region when bounded.

Related pages:

- [Runbooks](runbooks.md)
- [Incident response](incident-response.md)
- [Idempotency](../communication/idempotency.md)
- [Outbox pattern](../communication/outbox-pattern.md)
- [Pub/sub](../communication/pub-sub.md)

## Worker Metrics

Worker metrics should show whether background processors are alive, saturated,
safe to scale, and able to repair failed work.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Liveness | heartbeat age, active worker count, restart count | Detects stopped or flapping workers |
| Utilization | worker concurrency, busy workers, idle workers, CPU and memory use | Shows headroom and saturation |
| Processing | jobs started, completed, failed, skipped, processing duration | Explains throughput and result quality |
| Retry behavior | retry attempts, retry age, retry exhaustion, poison job count | Shows repeated failure and repair needs |
| Dependency pressure | provider call rate, timeout rate, quota use, fallback count | Prevents workers from amplifying downstream incidents |
| Safety | idempotency conflict count, duplicate suppression count, manual repair count | Protects correctness when replaying or scaling workers |

Useful dimensions:

- worker pool;
- job type;
- result class;
- dependency name;
- priority;
- tenant tier when bounded.

Related pages:

- [Capacity planning](capacity-planning.md)
- [Runbooks](runbooks.md)
- [Retries and backoff](../communication/retries-and-backoff.md)
- [Idempotency](../communication/idempotency.md)

## Search Metrics

Search metrics should show whether results are fast, fresh, complete enough,
and affordable to compute.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Query traffic | searches per second, autocomplete requests, filtered searches | Shows load by search path |
| Query latency | p50, p95, p99 query latency, timeout rate | Shows user-facing search performance |
| Result quality signals | zero-result rate, partial-result count, fallback count | Catches broken indexing or bad query behavior |
| Indexing freshness | indexing lag, update failure count, stale document age | Shows whether reads reflect recent writes |
| Index health | document count, index size, shard or partition pressure, merge duration | Reveals storage and maintenance pressure |
| Dependency pressure | source-of-truth backfill rate, reindex job age, queue lag | Connects search health to data pipelines |

Useful dimensions:

- query type, not raw query text;
- index name;
- result class;
- filter category when bounded;
- region or tenant tier when bounded.

Related pages:

- [Metrics](metrics.md)
- [Dashboards](dashboards.md)
- [Indexes](../data/indexes.md)
- [Bottleneck analysis](../scalability/bottleneck-analysis.md)

## CDN Metrics

CDN metrics should show whether content delivery is fast, cached correctly,
safe to operate, and not hiding origin or invalidation problems.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Traffic | requests, bandwidth, bytes served, regional traffic | Baseline for capacity and cost |
| Cache behavior | hit rate, miss rate, bypass count, origin fetch count | Shows whether the CDN protects the origin |
| Latency | edge latency, origin fetch latency, time to first byte | Separates edge performance from origin slowness |
| Errors | 4xx rate, 5xx rate, origin error rate, timeout rate | Shows user impact and origin dependency failure |
| Invalidation | invalidation count, invalidation age, stale object reports | Protects freshness for changed content |
| Cost and abuse | bandwidth spikes, hot object traffic, blocked requests, rate-limit count | Detects cost growth and misuse |

Useful dimensions:

- cache status;
- path category, not full URL when high-cardinality;
- region;
- object class;
- result class.

Related pages:

- [Capacity planning](capacity-planning.md)
- [Rate limiting](../scalability/rate-limiting.md)
- [Graceful degradation](../reliability/graceful-degradation.md)

## Object Storage Metrics

Object storage metrics should show whether uploads, downloads, retention,
durability checks, and cost remain healthy.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Object growth | object count, bytes stored, growth rate, retained bytes | Supports capacity, retention, and cost planning |
| Request traffic | upload rate, download rate, delete rate, metadata reads | Shows workload shape |
| Latency | upload latency, download latency, metadata lookup latency | Shows user and background-job impact |
| Errors | access denied, not found, timeout, checksum failure, multipart failure | Separates permission, consistency, and transport issues |
| Lifecycle | lifecycle transition count, deletion backlog, retention violations | Ensures policy and cleanup work |
| Durability and recovery | checksum verification, restore test age, replication lag, failed copy count | Protects recovery expectations |
| Cost drivers | egress bytes, retrieval count, storage tier mix, abandoned multipart uploads | Reveals cost surprises |

Useful dimensions:

- bucket or logical storage area;
- object class;
- operation type;
- result class;
- storage tier;
- region.

Do not use full object keys, filenames, user IDs, or private metadata as metric
labels. Use logs or audit records for individual object investigations.

Related pages:

- [Backups and restore](../data/backups-and-restore.md)
- [Data loss scenarios](../reliability/data-loss-scenarios.md)
- [Capacity planning](capacity-planning.md)
- [Logs](logs.md)

## Cross-Component Metrics

Some metrics should be visible across several components because they explain
workflow health better than any one component does.

| Metric Family | Examples | Why It Matters |
| --- | --- | --- |
| Correlation coverage | percentage of requests with request ID, trace ID, tenant ID, job ID | Makes logs and traces usable during incidents |
| SLO burn | short-window and long-window burn by workflow | Connects component behavior to reliability decisions |
| Cost growth | compute, storage, bandwidth, provider calls, observability volume | Prevents capacity fixes from creating cost incidents |
| Recovery readiness | backup age, restore-test age, runbook review age, rollback success | Shows whether incidents are repairable |
| Business outcome | completed reservations, fulfilled orders, delivered reminders, stuck states | Confirms technical health matches product health |

Related pages:

- [SLOs](slos.md)
- [Tracing](tracing.md)
- [Logs](logs.md)
- [Incident response](incident-response.md)

## Checklist

Before accepting a component metrics design, confirm:

- APIs include traffic, errors, latency, saturation, payload, and dependency
  signals.
- Databases include query, connection, lock, transaction, index, replication,
  backup, and storage-growth signals.
- Caches include hit/miss, latency, eviction, freshness, source-pressure, and
  availability signals.
- Queues and streams include arrival, drain, backlog age, processing, retry,
  dead-letter, and duplication signals.
- Workers include liveness, utilization, processing, retry, dependency, and
  safety signals.
- Search includes query traffic, latency, result quality, indexing freshness,
  index health, and pipeline pressure signals.
- CDN includes traffic, cache behavior, latency, errors, invalidation, cost, and
  abuse signals.
- Object storage includes growth, request traffic, latency, errors, lifecycle,
  recovery, and cost-driver signals.
- Dimensions are bounded, useful, and safe.
- Each metric has a dashboard, alert, SLO, runbook, capacity trigger, or
  debugging purpose.
- Related pages and runbooks explain what to do when important signals move.

## Related Pages

- [Metrics](metrics.md)
- [Dashboards](dashboards.md)
- [Alerting](alerting.md)
- [SLOs](slos.md)
- [Capacity planning](capacity-planning.md)
- [Runbooks](runbooks.md)
- [Incident response](incident-response.md)
- [Logs](logs.md)
- [Tracing](tracing.md)
- [Bottleneck analysis](../scalability/bottleneck-analysis.md)
- [Capacity estimation](../scalability/capacity-estimation.md)
