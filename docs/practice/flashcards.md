# Flashcards

## Purpose

Use these concise Q/A cards for repeated system design practice. They are meant
to trigger recall, not replace the decision guides.

Read the question, answer in your own words, then compare with the suggested
answer. If the answer feels memorized, add a small example before moving on.

## Requirements

| Question | Suggested Answer |
| --- | --- |
| What is the first thing to clarify in a system design prompt? | The user problem, actors, and system boundary. Components come later. |
| Why separate functional and non-functional requirements? | Functional requirements say what the system does; non-functional requirements say what qualities make the design hard. |
| What makes a requirement architecture-shaping? | It changes data ownership, component choice, failure handling, scale, security, cost, or operations. |
| What is a useful version 1 requirement? | One that solves the core user workflow while naming what is intentionally out of scope. |
| Why are vague words like fast or reliable risky? | They sound useful but do not tell you which workflow, target, or failure behavior matters. |
| What should you ask before accepting a real-time requirement? | Which user action needs fresh data, how fresh it must be, and what happens when updates are delayed. |
| How can a cost requirement change architecture? | It may justify simpler storage, shorter retention, quotas, batching, or avoiding always-on infrastructure. |
| What is the difference between privacy and security requirements? | Security controls access and abuse; privacy limits collection, exposure, retention, and use of personal data. |

## Components

| Question | Suggested Answer |
| --- | --- |
| When is a cache justified? | When repeated reads are expensive or slow and the workflow can tolerate a defined freshness rule. |
| What question should come before choosing a database type? | What data shape, invariant, query pattern, and consistency need must the source of truth support? |
| When does a queue belong in a design? | When work can finish later, needs retry, or must be buffered away from the user request path. |
| What does a stream add beyond a queue? | Retained event history, replay, ordering boundaries, and multiple independent consumers. |
| Why add a background worker? | To move slow, retryable, CPU-heavy, scheduled, or provider-dependent work out of the synchronous path. |
| What makes a search index different from a database query? | It optimizes ranking, text matching, filters, or autocomplete while introducing freshness and reindexing work. |
| When is object storage a better fit than database rows? | When the system stores large blobs such as images, videos, exports, backups, or attachments. |
| When should you avoid adding a queue? | When the work must complete before responding, duplicates are unsafe, or version 1 can use a direct call with clear timeout behavior. |
| What should every added component include? | A requirement, a trade-off, a failure mode, and a revisit or removal signal. |

## Trade-Offs

| Question | Suggested Answer |
| --- | --- |
| What is the basic trade-off shape to explain in review? | This choice improves one requirement but makes another quality harder, costlier, slower, or riskier. |
| Why is "more scalable" not enough justification? | It does not name the bottleneck, scale dimension, cost, or complexity being accepted. |
| What is a good revisit signal? | A metric, incident, user need, or scale threshold that would justify changing the design later. |
| Why discuss rejected alternatives? | They show the design considered simpler or different options and chose based on constraints. |
| When is manual work acceptable in version 1? | When it is rare, low risk, observable, and cheaper than automating before the workflow is proven. |
| What is a hidden cost of denormalization? | Faster reads can require extra write coordination, backfills, repair jobs, and stale-data handling. |
| What is the trade-off of stronger consistency? | It can improve correctness while reducing availability, concurrency, latency, or implementation simplicity. |
| How should you explain a deferred component? | State what risk remains, why it is acceptable now, and what signal would bring the component back. |

## Reliability

| Question | Suggested Answer |
| --- | --- |
| Why name the critical path? | It focuses reliability work on the user-visible flow where failure hurts most. |
| What makes a retry safe? | The operation is idempotent, bounded, observable, and does not duplicate unsafe side effects. |
| What should a timeout design include? | A timeout value, user-visible result, retry or fallback behavior, and how ambiguous outcomes are repaired. |
| What is graceful degradation? | Serving a reduced but honest experience instead of failing the whole workflow. |
| Why are dead-letter queues not a complete fix? | They store failed work for inspection, alerting, replay, or manual repair; they do not repair it automatically. |
| What is the difference between failover and backup restore? | Failover keeps service running elsewhere; restore rebuilds lost or corrupted data from backup. |
| What should an alert tell an operator? | What symptom happened, why it matters, where to look, and what action to take next. |
| Why include user-visible failure behavior? | It defines whether the system rejects, delays, degrades, retries, or asks for manual follow-up. |

## Data

| Question | Suggested Answer |
| --- | --- |
| What is the source of truth? | The place whose state is authoritative when derived copies disagree. |
| Why identify core entities before storage technology? | Entities and relationships reveal invariants, access patterns, ownership, and lifecycle needs. |
| What is derived data? | Data copied, transformed, cached, indexed, or aggregated from a source of truth. |
| What does read-your-writes mean? | After a user writes data, their later read should show that write within the required scope. |
| Why does retention matter in system design? | It affects storage cost, privacy, compliance, recovery, and backfill behavior. |
| What is a hot key? | A single key, tenant, partition, object, or user receiving enough traffic to overload one part of the system. |
| What should a schema evolution plan include? | Backward compatibility, migration order, backfill safety, rollback behavior, and observability. |
| What is the risk of cached authorization data? | Stale permissions can allow access after a role or policy changed. |

## Practice Loop

1. Pick five cards from different sections.
2. Answer without opening the docs.
3. Explain one answer out loud in under one minute.
4. Add one concrete example for every weak answer.
5. Link the weak answer to a requirement, component, trade-off, reliability, or
   data page.
6. Revisit the cards after writing or reviewing a design.

## Related Pages

- [Requirement discovery](../method/requirement-discovery.md)
- [Component selection map](../components/)
- [Trade-off vocabulary](../method/tradeoff-vocabulary.md)
- [Failure-mode analysis](../reliability/failure-mode-analysis.md)
- [Identifying entities](../data/identifying-entities.md)
- [System design rubric](system-design-rubric.md)
