# Learning Paths

## Purpose

Use these paths when the cookbook feels too broad to read from top to bottom.
Each path gives a learner goal, a sequence of concrete pages, and a few labs or
walkthroughs that turn the reading into practice.

The paths are guides, not tracks. Skip material you already understand, but do
not skip the requirement and trade-off pages when you are preparing to explain a
design decision.

## When This Matters

Learning paths help when you need to:

- start the cookbook without guessing which section matters first;
- prepare for system design interviews with a repeatable answer structure;
- connect runnable labs to real architecture choices;
- review a production design for reliability, security, and operations gaps;
- choose a smaller version 1 before adding more components.

## How To Choose A Path

| If Your Goal Is | Start With |
| --- | --- |
| Learn system design from the beginning | [Beginner path](#beginner-path) |
| Practice interview prompts and trade-off discussion | [Interview path](#interview-path) |
| Build small systems and observe behavior in code | [Builder path](#builder-path) |
| Review architecture for production readiness | [Production architecture path](#production-architecture-path) |

When in doubt, begin with the beginner path through requirement discovery, then
jump to the path that matches your current work.

## Questions To Ask

Before choosing a path, ask:

- Do I need foundations, interview practice, implementation intuition, or
  production review depth?
- Am I trying to explain a design, build a small demo, or critique an existing
  architecture?
- Which requirement is hardest for me to reason about: latency, scale,
  reliability, security, operations, or cost?
- Would a walkthrough, a lab, or a checklist make the next decision clearer?

## Path Trade-Offs

Each path optimizes for a different learning outcome:

- The beginner path builds the most complete foundation, but it takes longer
  before you reach larger systems.
- The interview path improves structure and explanation speed, but it can feel
  shallow if you do not follow it with labs or production review.
- The builder path makes failure modes observable, but a toy lab is not a full
  production architecture.
- The production architecture path finds operational gaps, but it assumes you
  already know the basic design loop.

## Beginner Path

Use this path if you are learning how to move from a prompt to a justified
architecture.

1. Read [Project guardrails](project-guardrails.md) so you understand the scope
   and originality rules behind the resource.
2. Read [System design process](../method/system-design-process.md) for the
   end-to-end design loop.
3. Practice [Requirement discovery](../method/requirement-discovery.md) and
   [functional vs non-functional requirements](../method/functional-vs-nonfunctional-requirements.md).
4. Use the [requirements map](../requirements/) to identify constraints such as
   [latency](../requirements/latency.md),
   [throughput](../requirements/throughput.md), and
   [availability](../requirements/availability.md).
5. Use the [component selection map](../components/) to connect requirements to
   components such as the [API layer](../components/api-layer.md),
   [database](../components/database-selection.md),
   [cache](../components/cache.md), and [queue](../components/queue.md).
6. Study the [URL shortener walkthrough](../walkthroughs/url-shortener.md) and
   [rate limiter walkthrough](../walkthroughs/rate-limiter.md).
7. Run the [token bucket rate limiter lab](../../labs/rate-limiter/) and compare
   the behavior to the [rate limiting](../scalability/rate-limiting.md) page.

By the end, you should be able to explain the problem, requirements, component
choices, trade-offs, failure modes, and simplest version 1 for a small design.

## Interview Path

Use this path when you need a repeatable way to answer prompts under time
pressure.

1. Read [System design process](../method/system-design-process.md) and keep its
   sequence visible while practicing.
2. Use [Requirement discovery](../method/requirement-discovery.md) to ask the
   first clarifying questions before drawing components.
3. Use [Scale estimation](../method/scale-estimation.md) and
   [capacity estimation](../scalability/capacity-estimation.md) to turn traffic
   guesses into rough constraints.
4. Read [Trade-off vocabulary](../method/tradeoff-vocabulary.md) so your answer
   explains what each choice improves and what it makes worse.
5. Practice with [URL shortener](../walkthroughs/url-shortener.md),
   [notification system](../walkthroughs/notification-system.md),
   [news feed](../walkthroughs/news-feed.md), and
   [metrics platform](../walkthroughs/metrics-platform.md) walkthroughs.
6. Use the [design review checklist](../method/design-review-checklist.md) after
   each practice answer.
7. Run small labs that make common interview trade-offs visible:
   [cache-aside](../../labs/cache-aside-demo/),
   [queue worker](../../labs/queue-worker-demo/),
   [retry and idempotency](../../labs/retry-idempotency-demo/), and
   [hot-key mitigation](../../labs/hot-key-demo/).

Do not memorize the walkthroughs. Use them to practice saying why a component
belongs, what could fail, and what you would simplify first.

## Builder Path

Use this path if you learn best by implementing small pieces and observing
their behavior.

1. Start with [component selection](../components/) and read the pages for
   [service layer](../components/service-layer.md),
   [database selection](../components/database-selection.md),
   [cache](../components/cache.md), [queue](../components/queue.md),
   [stream](../components/stream.md), [scheduler](../components/scheduler.md),
   and [background workers](../components/background-workers.md).
2. Read [read/write patterns](../data/read-write-patterns.md),
   [transactions](../data/transactions.md), and
   [schema evolution](../data/schema-evolution.md) before adding persistence.
3. Read [sync vs async](../communication/sync-vs-async.md),
   [retries and backoff](../communication/retries-and-backoff.md),
   [idempotency](../communication/idempotency.md), and the
   [outbox pattern](../communication/outbox-pattern.md) before adding
   asynchronous work.
4. Run the [cache-aside](../../labs/cache-aside-demo/),
   [queue worker](../../labs/queue-worker-demo/),
   [retry and idempotency](../../labs/retry-idempotency-demo/),
   [dead-letter queue](../../labs/dead-letter-queue-demo/), and
   [log compaction](../../labs/log-compaction-demo/) labs.
5. Compare the lab behavior to worked systems such as
   [payment workflow](../walkthroughs/payment-workflow.md),
   [file storage system](../walkthroughs/file-storage-system.md), and
   [video processing](../walkthroughs/video-processing.md).

This path is useful when you want code to expose the trade-off. For example, a
queue worker demo makes retry exhaustion and duplicate processing easier to
reason about than a static diagram alone.

## Production Architecture Path

Use this path when reviewing a design that must survive real traffic, real
users, and real operations.

1. Start with requirements that affect production risk:
   [availability](../requirements/availability.md),
   [durability](../requirements/durability.md),
   [consistency](../requirements/consistency.md),
   [security](../requirements/security.md),
   [privacy](../requirements/privacy.md),
   [compliance](../requirements/compliance.md),
   [operability](../requirements/operability.md), and
   [cost](../requirements/cost.md).
2. Read reliability pages for [timeouts](../reliability/timeouts.md),
   [retries](../reliability/retries.md),
   [circuit breakers](../reliability/circuit-breakers.md),
   [bulkheads](../reliability/bulkheads.md),
   [failover](../reliability/failover.md),
   [RPO/RTO](../reliability/rpo-rto.md), and
   [disaster recovery](../reliability/disaster-recovery.md).
3. Read operations pages for [observability basics](../operations/observability-basics.md),
   [metrics](../operations/metrics.md), [logs](../operations/logs.md),
   [tracing](../operations/tracing.md), [alerting](../operations/alerting.md),
   [runbooks](../operations/runbooks.md), and
   [cost analysis](../operations/cost-analysis.md).
4. Read security pages for [authentication](../security/authentication.md),
   [authorization](../security/authorization.md),
   [data privacy](../security/data-privacy.md),
   [audit logs](../security/audit-logs.md),
   [secrets management](../security/secrets-management.md), and
   [rate limiting and abuse](../security/rate-limiting-and-abuse.md).
5. Run labs that expose production failure modes:
   [replication lag](../../labs/replication-lag-simulator/),
   [quorum reads and writes](../../labs/quorum-read-write-simulator/),
   [sharding](../../labs/sharding-simulator/),
   [hot keys](../../labs/hot-key-demo/), and
   [dead-letter queues](../../labs/dead-letter-queue-demo/).
6. Review [metrics platform](../walkthroughs/metrics-platform.md),
   [news feed](../walkthroughs/news-feed.md),
   [search autocomplete](../walkthroughs/search-autocomplete.md), and
   [chat system](../walkthroughs/chat-system.md) for larger-system trade-offs.

This path should leave you with production review questions: what fails, what
is observable, what data can be lost, who can access what, what costs grow, and
which part needs a simpler version 1.

## Original Example

Imagine a team building a notification system for appointment reminders.

- The beginner path helps the team define the user problem, delivery channels,
  latency target, and first version.
- The interview path helps a candidate explain why preferences, queues,
  provider retries, idempotency keys, and dead-letter handling belong in the
  design.
- The builder path points to queue, retry, idempotency, and DLQ labs so the team
  can observe duplicate sends and poison messages.
- The production architecture path checks provider outages, audit logs,
  privacy, alerting, runbooks, cost, and recovery behavior.

The same system can use more than one path. The path changes the learning goal,
not the system being designed.

## Common Mistakes

- Reading only walkthroughs and skipping requirement discovery.
- Treating a lab as production architecture instead of a behavior demo.
- Adding caches, queues, streams, or sharding before naming the constraint they
  solve.
- Preparing for interviews by memorizing complete systems instead of practicing
  trade-off language.
- Reviewing production designs without observability, security, recovery, and
  cost questions.

## Checklist

Before leaving a path, confirm you can answer:

- What problem is this path helping me solve?
- Which requirements changed the design?
- Which component choices were justified by those requirements?
- What trade-off did each choice introduce?
- Which lab or walkthrough made the decision concrete?
- What would I simplify for version 1?
- What would I revisit at 10x scale or after the first incident?

## Related Pages

- [Documentation index](../)
- [Start here](./)
- [System design process](../method/system-design-process.md)
- [Design review checklist](../method/design-review-checklist.md)
- [Labs guide](../labs/)
- [Walkthroughs](../walkthroughs/)
