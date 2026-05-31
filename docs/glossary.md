# Glossary

This glossary defines common system design terms in plain language. Use it as a
starting point, then follow the related section links for decision guidance.

## Starter Terms

### API

An interface that lets one part of a system ask another part to do something or
return data. APIs matter because they shape coupling, latency, and failure
handling. Related: [Components](components/), [Communication](communication/).

### Availability

How often a system can serve users successfully. Availability is not just
uptime; it also includes degraded behavior when dependencies fail. Related:
[Requirements](requirements/), [Reliability](reliability/).

### Backpressure

A way for a busy component to slow down incoming work instead of accepting more
than it can process. Backpressure helps prevent queues, workers, or databases
from being overwhelmed. Related: [Communication](communication/),
[Scalability](scalability/).

### Cache

A faster place to keep data that would otherwise be slower or more expensive to
fetch. Caches help when stale data is acceptable, but they add invalidation and
consistency trade-offs. Related: [Components](components/),
[Scalability](scalability/).

### Capacity

The amount of traffic, data, or work a system can handle before it becomes too
slow, too costly, or unreliable. Capacity planning starts with rough estimates,
not exact predictions. Related: [Method](method/), [Operations](operations/).

### Consistency

How different reads and writes agree with each other over time. Stronger
consistency can make behavior simpler for users, but it may reduce availability
or increase latency. Related: [Requirements](requirements/), [Data](data/).

### Durability

The chance that saved data survives failures. Durable systems usually rely on
persistent storage, replication, backups, or recovery processes. Related:
[Data](data/), [Reliability](reliability/).

### Event

A record that something happened, such as `OrderPlaced` or `PasswordReset`.
Events help systems react asynchronously, but consumers must handle retries,
duplicates, and ordering limits. Related: [Communication](communication/).

### Failure mode

A specific way a system can break or degrade. Naming failure modes helps teams
design fallbacks, alerts, retries, and recovery steps. Related:
[Reliability](reliability/), [Operations](operations/).

### Idempotency

The property that repeating the same operation has the same effect as doing it
once. Idempotency is important when clients retry requests or workers process
messages more than once. Related: [Communication](communication/),
[Reliability](reliability/).

### Index

A data structure that makes some database lookups faster. Indexes improve read
paths but add write overhead and storage cost. Related: [Data](data/).

### Latency

How long one operation takes from the user's or caller's point of view. Latency
requirements should distinguish typical cases from slow tail cases. Related:
[Requirements](requirements/), [Operations](operations/).

### Load balancer

A component that spreads requests across multiple service instances. Load
balancers can improve availability and scaling, but they also need health
checks and failure behavior. Related: [Components](components/),
[Reliability](reliability/).

### Message queue

A buffer between producers and workers. Queues help with asynchronous work,
bursts, retries, and worker isolation, but they introduce delay and duplicate
processing risks. Related: [Components](components/),
[Communication](communication/).

### Observability

The ability to understand what a system is doing from signals such as metrics,
logs, traces, and events. Observability matters because failures are easier to
fix when the system explains itself. Related: [Operations](operations/).

### Partition

A slice of data or traffic assigned to part of a system. Partitioning can spread
load, but it introduces routing, rebalancing, and hot-key problems. Related:
[Data](data/), [Scalability](scalability/).

### Rate limit

A rule that caps how much work a user, client, tenant, or system can request in
a time window. Rate limits protect reliability and abuse resistance, but they
must be clear enough for legitimate users. Related: [Security](security/),
[Scalability](scalability/).

### Replication

Keeping copies of data in more than one place. Replication can improve
availability, read scaling, or durability, but replicas may lag or disagree.
Related: [Data](data/), [Reliability](reliability/).

### Scalability

The ability to handle growth in users, requests, data, or work without
unacceptable cost or reliability loss. Scaling should answer a measured
bottleneck, not just add complexity. Related: [Scalability](scalability/).

### Sharding

Splitting data across multiple storage nodes by a key such as user ID, tenant,
or region. Sharding can increase capacity, but it complicates queries,
transactions, and rebalancing. Related: [Data](data/),
[Scalability](scalability/).

### SLO

A target for service behavior, such as request success rate or latency over a
time window. SLOs help teams decide how reliable a system needs to be and when
to prioritize reliability work. Related: [Operations](operations/).

### Throughput

How much work a system completes per unit of time, such as requests per second
or jobs per minute. Throughput requirements should include bursts and peak
traffic, not just averages. Related: [Requirements](requirements/),
[Scalability](scalability/).

### Timeout

A limit on how long a caller waits before giving up. Timeouts prevent stuck
requests from consuming resources forever, but they must be paired with retry
and fallback decisions. Related: [Reliability](reliability/),
[Communication](communication/).

### Trade-off

A decision where improving one property makes another property worse, more
expensive, or harder to operate. Good system design names the trade-off instead
of hiding it. Related: [Method](method/), [Practice](practice/).

## Related Pages

- [Method](method/)
- [Requirements](requirements/)
- [Components](components/)
- [Data](data/)
- [Communication](communication/)
- [Scalability](scalability/)
- [Reliability](reliability/)
- [Security](security/)
- [Operations](operations/)
- [Practice](practice/)
