# Common System Design Mistakes

## Purpose

Use this catalog to spot common system design mistakes and replace them with
clearer reasoning. Each mistake includes the risk it creates and a practical
fix.

The goal is not to avoid every advanced component. The goal is to add complexity
only after a requirement, bottleneck, failure mode, or operating constraint
justifies it.

## When This Matters

Use this page when:

- reviewing your own design before reading a walkthrough;
- giving critique on an interview answer or architecture proposal;
- a design has many components but few named requirements;
- the answer sounds plausible but hides failure, consistency, or operational
  behavior.

## Quick Catalog

| Mistake | Typical Symptom | Better Move |
| --- | --- | --- |
| Premature microservices | Many services before boundaries are clear | Start with one deployable system or modular monolith and split after ownership or scale pressure appears |
| Unjustified Kafka | A stream is added for every async task | Use a queue, table, or direct call unless retention, replay, ordering, or many consumers are required |
| Missing failure modes | The design only shows the happy path | Name what fails, what users see, and how operators repair it |
| Vague consistency | The answer says eventual or strong consistency without scope | Name the data, workflow, freshness need, and conflict behavior |
| Overreliance on cache | Cache is used as the main performance answer | Define freshness, invalidation, fallback, authorization, and source-of-truth reads |

## Mistake 1: Premature Microservices

### What It Sounds Like

```text
We will create user, search, reservation, payment, notification, analytics, and
admin services so the system can scale.
```

### Why It Is Risky

Microservices can isolate teams and workloads, but they also add network calls,
deployment coordination, distributed tracing, data ownership questions, partial
failure, authorization boundaries, and operational overhead.

If the design has not named team boundaries, traffic bottlenecks, data ownership
pressure, or independent deployment needs, separate services may make version 1
harder without solving the real problem.

### Fix

Start with a simpler boundary:

- one deployable system with clear modules;
- one source of truth for the core workflow;
- explicit interfaces inside the codebase;
- logs and metrics that reveal which module becomes a bottleneck.

Split later when a module has a different scale profile, release cadence,
ownership boundary, reliability target, or data lifecycle.

### Revisit Signal

Consider splitting when one module repeatedly blocks independent delivery,
overloads the rest of the system, needs separate data ownership, or has a
different failure-isolation requirement.

## Mistake 2: Unjustified Kafka

### What It Sounds Like

```text
Every write publishes to Kafka, and all services consume events from it.
```

### Why It Is Risky

A retained event log is powerful when consumers need replay, ordering within
partitions, fanout, backfills, or durable event history. It is not the default
answer for every delayed task.

Using a stream without a retention, replay, or multi-consumer requirement adds
event schema management, partitioning, consumer lag, reprocessing, monitoring,
and cost before the design needs those properties.

### Fix

Choose the simplest async mechanism that matches the requirement:

- direct call when work must finish before the response;
- queue when work can finish later and needs retry or burst smoothing;
- table-backed worklist or scheduled job when one service owns the delayed work;
- database outbox when writes and event publication must stay coordinated;
- stream when retained history, replay, many independent consumers, or ordered
  event processing is a named requirement.

### Revisit Signal

Add a stream when independent consumers need event replay, audit-style event
history, backfills, or ordering guarantees that a simple queue cannot provide.

## Mistake 3: Missing Failure Modes

### What It Sounds Like

```text
The API writes to the database, sends a message, and the worker calls the
provider.
```

### Why It Is Risky

The design may be correct only when every dependency is healthy. Real systems
need behavior for timeouts, duplicate requests, partial writes, unavailable
providers, retry exhaustion, stale reads, and manual repair.

Without failure modes, reviewers cannot tell whether users see a clear error,
pending state, degraded response, duplicate side effect, or silent data loss.

### Fix

For the critical path, write:

```text
Failure:
User impact:
System response:
Repair or follow-up:
Signal:
```

Add failure paths only where they change the design. A payment provider timeout,
for example, may require idempotency keys, an attempt record, reconciliation,
and an operator-visible `needs_review` state.

Example:

```text
Failure: Payment provider times out after the order is created.
User impact: The checkout page shows "payment pending" instead of success.
System response: Record the attempt, retry with the same idempotency key, and
  stop retrying after a bounded number of attempts.
Repair or follow-up: Put exhausted attempts in a `needs_review` queue.
Signal: Alert on timeout rate and count pending payments older than 15 minutes.
```

### Revisit Signal

Add deeper reliability design when failures affect money, access, data loss,
legal evidence, high-volume user workflows, or expensive manual support.

## Mistake 4: Vague Consistency

### What It Sounds Like

```text
The system will be eventually consistent.
```

or:

```text
The database gives strong consistency.
```

### Why It Is Risky

Consistency is not useful until it is tied to a specific read, write, conflict,
and user expectation. A feed can tolerate stale counts. A reservation checkout
may need a transaction or conditional write to prevent double booking.

Vague consistency language hides the real decision: which data may be stale,
which write must be atomic, which duplicates are allowed, and how conflicts are
resolved.

### Fix

Use this shape:

```text
For [workflow], [read/write] must be [freshness or conflict rule] because
[user impact]. We accept [staleness or delay] for [other workflow].
```

Example:

```text
Reservation confirmation must atomically claim one available slot because two
confirmations for the same slot break the product promise. The availability
summary page may lag by 30 seconds because users confirm on the detail page.
```

### Revisit Signal

Revisit consistency when stale reads cause user-visible confusion, conflicts
need manual repair, write contention grows, or correctness requirements become
stricter.

## Mistake 5: Overreliance On Cache

### What It Sounds Like

```text
Add an in-memory cache in front of the database to make reads fast.
```

### Why It Is Risky

A cache can reduce latency and source load, but it also introduces stale data,
invalidation, fallback behavior, authorization leakage, cold starts, and
operational failure modes.

If the design does not define freshness and source-of-truth behavior, the cache
can become a second source of truth by accident.

### Fix

Before adding a cache, define:

- which read is slow or expensive;
- how stale the result may be;
- how entries expire or get invalidated;
- what happens on miss, stale entry, or cache outage;
- whether cached data includes permissions or private fields;
- which metric proves the cache is worth keeping.

For version 1, prefer indexed source reads if traffic is modest and freshness
matters.

### Revisit Signal

Add or expand caching when measured read latency, source load, bandwidth cost,
or repeated expensive computation exceeds the target and the workflow can
tolerate a clear freshness rule.

## Original Example

A team designs a volunteer meal pickup system and proposes:

```text
Use microservices for users, meals, pickups, notifications, and analytics. Use
Kafka for all events. Cache pickup availability. Everything is eventually
consistent.
```

Corrections:

- Start with one deployable service and modules for meals, pickups, and
  notifications until ownership or scale requires a split.
- Use a queue for reminder delivery; use an outbox if pickup confirmation and
  notification events must be coordinated.
- Keep pickup confirmation strongly guarded by one transactional write or
  conditional update.
- Cache only the public meal list if stale data is acceptable; do not cache
  pickup authorization decisions without a strict freshness rule.
- Add failure behavior for duplicate pickup attempts, reminder retry exhaustion,
  and provider outage.

The corrected design is smaller, easier to explain, and safer for version 1.

## Checklist

Before accepting a design, ask:

- Which requirement justifies each advanced component?
- Which data needs a precise consistency rule?
- What failure path changes the user or operator experience?
- Is a queue, stream, cache, replica, shard, or service split solving a named
  pressure?
- What simpler version 1 would still solve the core workflow?
- What metric or incident would justify adding the deferred complexity later?

## Related Pages

- [Trade-off vocabulary](../method/tradeoff-vocabulary.md)
- [Component selection map](../components/)
- [Consistency requirements](../requirements/consistency.md)
- [Cache](../components/cache.md)
- [Stream](../components/stream.md)
- [Failure-mode analysis](../reliability/failure-mode-analysis.md)
- [Self-review checklist](self-review-checklist.md)
- [Overengineering checklist](overengineering-checklist.md)
