# Walkthroughs

Walkthroughs are end-to-end worked system designs. They show how to move from a
problem statement to requirements, component choices, data flow, trade-offs,
failure handling, observability, cost, and a simple version 1.

Use the [walkthrough template](../../templates/walkthrough-template.md) for
new walkthrough pages. Use the
[design doc template](../../templates/design-doc-template.md) when the work is a
proposal, exercise, or architecture note that does not need the full narrative
walkthrough format.

## Purpose

Use walkthroughs to practice the cookbook method on complete systems:

- start from a user problem and system boundary;
- translate requirements into concrete design constraints;
- choose components only when they solve a named problem;
- show read and write paths;
- explain data ownership, consistency, scaling, failure, security,
  observability, and cost decisions;
- simplify version 1 without hiding the trade-offs;
- state what changes when the system grows.

The goal is not to memorize perfect answers. The goal is to demonstrate the
reasoning path and the consequences of each design choice.

## Standard Walkthrough Structure

Every walkthrough should include these sections:

1. Problem statement
2. Functional requirements
3. Non-functional requirements
4. Core entities
5. API sketch
6. Read path
7. Write path
8. Data model
9. Component choices
10. Architecture diagram
11. Consistency decisions
12. Scaling strategy
13. Failure modes
14. Security concerns
15. Observability
16. Cost considerations
17. Version 1 simplification
18. What changes at 10x scale
19. Related pages

Use Mermaid for architecture, data-flow, sequence, or failure-mode diagrams
when a diagram clarifies the reasoning. Diagrams must be original and should
make a decision or flow easier to understand.

## Quality Bar

A walkthrough is ready when it:

- explains the problem before naming components;
- separates functional requirements from non-functional requirements;
- includes a small but concrete original example;
- states assumptions and rejects at least a few plausible alternatives;
- ties every major component to a requirement, constraint, or failure mode;
- includes both the happy path and important failure paths;
- names the source of truth and any derived, cached, indexed, or asynchronous
  data;
- discusses consistency, idempotency, retries, and backpressure when relevant;
- includes operational signals: metrics, logs, traces, alerts, dashboards, and
  runbooks where they matter;
- discusses security, privacy, abuse, and cost risks without turning the page
  into a vendor-specific implementation guide;
- keeps version 1 simple and says which signal would justify the next design
  step;
- links to relevant cookbook pages instead of restating every concept.

Avoid walkthroughs that present a final architecture as if it were the only
correct answer. The reader should see the decisions, alternatives, and
trade-offs.

## Current Walkthroughs

Completed walkthrough pages:

| Walkthrough | Focus |
| --- | --- |
| [Metrics platform](metrics-platform.md) | ingestion, buffering, aggregation, storage, dashboards, retention, high-cardinality data, and alerts |
| [Payment workflow](payment-workflow.md) | idempotency, external provider calls, state machine, retries, audit logs, reconciliation, and failure handling |
| [Rate limiter](rate-limiter.md) | requirements, algorithms, distributed counters, Redis-style storage, failure behavior, abuse, and metrics |
| [URL shortener](url-shortener.md) | short-code generation, redirect path, mapping storage, caching, analytics, failure modes, and 10x scale |
| [Notification system](notification-system.md) | email/SMS/push, preferences, queues, retries, templates, idempotency, provider failure, and dead-letter queues |
| [File storage system](file-storage-system.md) | upload, metadata, object storage, signed URLs, CDN, permissions, scanning, and lifecycle |
| [Chat system](chat-system.md) | conversations, messages, delivery, WebSockets, ordering, offline users, read receipts, and scaling |
| [News feed](news-feed.md) | fanout, feed generation, ranking, caching, celebrity users, freshness, and eventual consistency |
| [Search autocomplete](search-autocomplete.md) | indexing, prefix search, ranking, freshness, caching, typo tolerance, and reindexing |
| [Video processing](video-processing.md) | upload, object storage, transcoding, queues, workers, CDN, status tracking, and retries |

## Related Pages

- [System design process](../method/system-design-process.md)
- [Design review checklist](../method/design-review-checklist.md)
- [Functional vs non-functional requirements](../method/functional-vs-nonfunctional-requirements.md)
- [Scale estimation](../method/scale-estimation.md)
- [Capacity estimation](../scalability/capacity-estimation.md)
- [Bottleneck analysis](../scalability/bottleneck-analysis.md)
- [Operations](../operations/)
- [Reliability](../reliability/)
- [Security](../security/)

Return to the [documentation index](../).
