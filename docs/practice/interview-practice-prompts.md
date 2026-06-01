# Interview Practice Prompts

## Purpose

Use these prompts to practice system design at different difficulty levels. Each
prompt names the main design pressure and links decision trees or decision maps
that help you reason before reading a walkthrough.

The goal is not to memorize a perfect architecture. The goal is to practice
turning requirements into justified components, trade-offs, failure behavior,
and a simple version 1.

## When This Matters

Use this page when you want:

- a prompt matched to your current skill level;
- a short list of decision trees to read after attempting a design;
- interview practice that covers more than common component names;
- a way to compare your answer with the [self-review checklist](self-review-checklist.md)
  and [system design rubric](system-design-rubric.md).

## How To Practice

1. Pick one prompt and set a time box.
2. Write requirements before drawing the architecture.
3. Sketch read and write paths before choosing components.
4. Use the linked decision trees only after your first attempt.
5. Revise the design with the [self-review checklist](self-review-checklist.md).
6. Score the second draft with the [system design rubric](system-design-rubric.md).

## Beginner Prompts

Beginner prompts should stay small. Focus on requirements, data ownership,
basic APIs, and one or two trade-offs.

| Prompt | Practice Focus | Decision Trees And Maps |
| --- | --- | --- |
| Design a neighborhood tool reservation system | reservations, conflicts, version 1 scope | [Requirement discovery](../method/requirement-discovery.md), [consistency](../requirements/consistency.md), [database selection](../components/database-selection.md) |
| Design a URL shortener for event invitations | write path, redirect read path, generated identifiers, abuse limits | [Latency](../requirements/latency.md), [read/write patterns](../data/read-write-patterns.md), [rate limiting and abuse](../security/rate-limiting-and-abuse.md) |
| Design a shared grocery list app for families | collaboration, stale reads, simple sync | [Functional vs non-functional requirements](../method/functional-vs-nonfunctional-requirements.md), [consistency](../requirements/consistency.md), [API layer](../components/api-layer.md) |
| Design a small appointment reminder service | delayed work, retries, duplicate sends | [Sync vs async](../communication/sync-vs-async.md), [queue](../components/queue.md), [idempotency](../communication/idempotency.md) |
| Design a photo upload and sharing service for a local club | object metadata, file storage, permissions | [Object storage](../components/object-storage.md), [privacy](../requirements/privacy.md), [authorization](../security/authorization.md) |
| Design a simple rate limiter for one API | counters, abuse, user-visible rejection | [Rate limiting](../scalability/rate-limiting.md), [throughput](../requirements/throughput.md), [rate limiting and abuse](../security/rate-limiting-and-abuse.md) |

## Intermediate Prompts

Intermediate prompts add scale, async work, search, caching, and more explicit
failure handling.

| Prompt | Practice Focus | Decision Trees And Maps |
| --- | --- | --- |
| Design a notification system for email and push reminders | preferences, queues, provider failures | [Queue](../components/queue.md), [retries and backoff](../communication/retries-and-backoff.md), [dead-letter queues](../communication/dead-letter-queues.md) |
| Design search autocomplete for product names | indexing, freshness, ranking, hot prefixes | [Search index](../components/search-index.md), [latency](../requirements/latency.md), [capacity estimation](../scalability/capacity-estimation.md) |
| Design a cache for a public catalog | cache freshness, invalidation, fallback | [Caching strategies](../scalability/caching-strategies.md), [cache](../components/cache.md), [cost](../requirements/cost.md) |
| Design a queue-backed export job system | long-running jobs, retry, job status | [Background workers](../components/background-workers.md), [queue](../components/queue.md), [retries and backoff](../communication/retries-and-backoff.md) |
| Design a feed of recent posts for a small social app | fanout, reads, ordering, freshness | [Scalability](../requirements/scalability.md), [capacity estimation](../scalability/capacity-estimation.md), [database read scaling](../scalability/database-read-scaling.md) |
| Design an audit log for admin actions | append-only records, retention, access | [Audit logs](../security/audit-logs.md), [compliance](../requirements/compliance.md), [data retention](../data/data-retention.md) |

## Senior Prompts

Senior prompts require explicit trade-offs across data correctness, reliability,
operations, and cost. Expect to discuss failure modes and rejected alternatives.

| Prompt | Practice Focus | Decision Trees And Maps |
| --- | --- | --- |
| Design a payment workflow with an external provider | idempotency, ambiguous outcomes, reconciliation | [Idempotency](../communication/idempotency.md), [saga pattern](../communication/saga-pattern.md), [failure-mode analysis](../reliability/failure-mode-analysis.md) |
| Design a metrics ingestion and dashboard platform | write volume, aggregation, retention, queries | [Throughput](../requirements/throughput.md), [streams](../communication/streams.md), [operability](../requirements/operability.md) |
| Design file upload, virus scanning, and download links | object lifecycle, async processing, signed access | [Object storage](../components/object-storage.md), [background workers](../components/background-workers.md), [data privacy](../security/data-privacy.md) |
| Design a sharded inventory service | write contention, partitioning, hot keys | [Partitioning and sharding](../data/partitioning-and-sharding.md), [sharding strategies](../scalability/sharding-strategies.md), [hot-key mitigation](../scalability/hot-key-mitigation.md) |
| Design a multi-tenant admin dashboard | roles, tenant boundaries, auditability | [Authorization](../security/authorization.md), [access control models](../security/access-control-models.md), [operability](../requirements/operability.md) |
| Design a resilient chat delivery service | ordering, offline users, retries, presence | [Sync vs async](../communication/sync-vs-async.md), [availability](../requirements/availability.md), [graceful degradation](../reliability/graceful-degradation.md) |

## Staff-Level Prompts

Staff-level prompts are intentionally broader. Practice framing the scope,
choosing what not to solve, and naming organizational or operational trade-offs.

| Prompt | Practice Focus | Decision Trees And Maps |
| --- | --- | --- |
| Design a regional failover plan for a critical booking system | RPO/RTO, degraded mode, data loss, operations | [RPO/RTO](../reliability/rpo-rto.md), [disaster recovery](../reliability/disaster-recovery.md), [availability](../requirements/availability.md) |
| Design a migration from a monolithic database to service-owned data | boundaries, schema evolution, dual writes, rollback | [Schema evolution](../data/schema-evolution.md), [outbox pattern](../communication/outbox-pattern.md), [transactions](../data/transactions.md) |
| Design platform-wide abuse controls for public APIs | quotas, identity, audit, false positives | [Security](../requirements/security.md), [rate limiting and abuse](../security/rate-limiting-and-abuse.md), [cost](../requirements/cost.md) |
| Design an observability strategy for several services | signals, ownership, incident response, cost | [Operability](../requirements/operability.md), [metrics](../operations/metrics.md), [incident response](../operations/incident-response.md) |
| Design a data retention and deletion program for user content | policy, deletion evidence, backups, audit | [Privacy](../requirements/privacy.md), [data retention and deletion](../security/data-retention-and-deletion.md), [backups and restore](../data/backups-and-restore.md) |

## Difficulty Guide

| Level | A Good Answer Should Show |
| --- | --- |
| Beginner | Clear requirements, one source of truth, simple APIs, and version 1 scope |
| Intermediate | Scale estimate, async or cache trade-off, and basic failure behavior |
| Senior | Correctness boundaries, operational signals, security, cost, and rejected alternatives |
| Staff-level | Scope control, migration or organizational trade-offs, failure planning, and long-term operability |

Move up a level when your self-review finds fewer missing requirements and more
specific trade-offs.

## Original Example Practice Loop

Prompt: design a queue-backed export job system.

First attempt:

```text
Users request exports. The API stores a job, a worker generates the file, and
the user downloads it later.
```

Decision-tree review:

- Use [background workers](../components/background-workers.md) to justify why
  export generation should leave the request path.
- Use [retries and backoff](../communication/retries-and-backoff.md) to define
  retryable failures and retry limits.
- Use [object storage](../components/object-storage.md) if exports are large
  files with lifecycle and access rules.
- Use [observability basics](../operations/observability-basics.md) to decide
  which job IDs, metrics, and alerts operators need.

Second attempt should add job states, retry exhaustion, output lifecycle,
authorization for downloads, cost of stored exports, and the version 1
simplification.

## Common Mistakes

- Reading the linked pages before making a first attempt.
- Treating the difficulty level as a required architecture size.
- Adding every linked component instead of deciding whether the prompt needs it.
- Skipping security, cost, and observability on senior prompts.
- Memorizing walkthrough shape instead of explaining the requirement path.

## Checklist

Before finishing a practice session, confirm:

- I wrote requirements before components.
- I used at least one linked decision tree to revise the answer.
- I named the source of truth and the main read/write path.
- I justified or removed each cache, queue, stream, replica, shard, or worker.
- I named one failure mode and one observability signal.
- I stated what version 1 can skip.
- I scored the result or wrote a concrete next revision step.

## Related Pages

- [Self-review checklist](self-review-checklist.md)
- [System design rubric](system-design-rubric.md)
- [Requirement discovery](../method/requirement-discovery.md)
- [Design review checklist](../method/design-review-checklist.md)
- [Requirements map](../requirements/)
- [Component selection map](../components/)
