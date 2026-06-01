# How To Use This Cookbook

## Purpose

Use this guide when you are opening the cookbook for the first time and want a
clear way to begin.

You do not need to read every page before designing something. Start with one
goal, read the first few pages for that goal, then apply the questions to a
small design or lab. Start small, write down what changed your decision, and
revisit harder pages when a real constraint appears.

## When This Matters

This page helps when you are:

- new to system design and unsure where to start;
- preparing for interviews and need a repeatable answer structure;
- trying to connect documentation pages to runnable labs;
- reviewing a production design and looking for gaps;
- returning to the cookbook after finishing one path.

## Docs Vs Labs

The cookbook has two kinds of material:

| Material | Where It Lives | Use It For |
| --- | --- | --- |
| Docs pages | `docs/` | Decision guidance, checklists, diagrams, walkthroughs, and review prompts |
| Labs | `labs/` | Small runnable examples that make behavior visible in code |

Use docs when you need to decide what matters. Use labs when you want to
observe a behavior directly.

For example, read [caching strategies](../scalability/caching-strategies.md)
when deciding whether stale reads are acceptable. Run the
[cache-aside lab](https://github.com/LeonSilva15/system-design/tree/main/labs/cache-aside-demo/) when you want to observe hits,
misses, TTL expiry, and stale data.

## First Pages To Read

If you only read five pages first, read these:

1. [Project guardrails](project-guardrails.md) - understand the repository
   scope, originality rules, and attribution boundaries.
2. [Learning paths](learning-paths.md) - choose the route that matches your
   current goal.
3. [System design process](../method/system-design-process.md) - learn the
   repeatable problem-to-architecture loop.
4. [Requirement discovery](../method/requirement-discovery.md) - practice
   turning vague prompts into constraints.
5. [Component selection map](../components/) - connect requirements to justified
   components.

After those pages, move to a walkthrough or lab instead of continuing to read
passively.

## Choose A Path

### Beginner Path

Use this path if you are learning the basics.

1. Read [System design process](../method/system-design-process.md).
2. Read [Requirement discovery](../method/requirement-discovery.md) and
   [functional vs non-functional requirements](../method/functional-vs-nonfunctional-requirements.md).
3. Read the [requirements map](../requirements/) and choose one requirement
   page that changes your design.
4. Read the [component selection map](../components/).
5. Study the [URL shortener walkthrough](../walkthroughs/url-shortener.md).
6. Run the [rate limiter lab](https://github.com/LeonSilva15/system-design/tree/main/labs/rate-limiter/) to observe one concrete
   behavior.

Goal: explain a small design with requirements, components, trade-offs, and a
simple version 1.

### Interview Path

Use this path if you are practicing system design prompts.

1. Read [System design process](../method/system-design-process.md) as your
   answer structure.
2. Use [Scale estimation](../method/scale-estimation.md) and
   [capacity estimation](../scalability/capacity-estimation.md) for rough
   numbers.
3. Read [Trade-off vocabulary](../method/tradeoff-vocabulary.md) so your answer
   names consequences, not just components.
4. Practice with [rate limiter](../walkthroughs/rate-limiter.md),
   [notification system](../walkthroughs/notification-system.md), and
   [news feed](../walkthroughs/news-feed.md) walkthroughs.
5. Use the [design review checklist](../method/design-review-checklist.md) to
   find missing requirements, failure modes, and simplifications.

Goal: give a clear answer under time pressure without memorizing a perfect
architecture.

### Builder Path

Use this path if you learn best by running code.

1. Read the component pages for [cache](../components/cache.md),
   [queue](../components/queue.md),
   [stream](../components/stream.md), and
   [background workers](../components/background-workers.md).
2. Read [sync vs async](../communication/sync-vs-async.md),
   [retries and backoff](../communication/retries-and-backoff.md), and
   [idempotency](../communication/idempotency.md).
3. Run the [cache-aside](https://github.com/LeonSilva15/system-design/tree/main/labs/cache-aside-demo/),
   [queue worker](https://github.com/LeonSilva15/system-design/tree/main/labs/queue-worker-demo/),
   [retry and idempotency](https://github.com/LeonSilva15/system-design/tree/main/labs/retry-idempotency-demo/), and
   [dead-letter queue](https://github.com/LeonSilva15/system-design/tree/main/labs/dead-letter-queue-demo/) labs.
4. Compare what you observed to a worked system such as
   [payment workflow](../walkthroughs/payment-workflow.md) or
   [video processing](../walkthroughs/video-processing.md).

Goal: connect a design choice to behavior you can see in a small program.

### Production Architecture Path

Use this path if you are reviewing a design for real users and operations.

1. Start with production-impacting requirements:
   [availability](../requirements/availability.md),
   [durability](../requirements/durability.md),
   [security](../requirements/security.md),
   [privacy](../requirements/privacy.md),
   [operability](../requirements/operability.md), and
   [cost](../requirements/cost.md).
2. Read reliability pages for [timeouts](../reliability/timeouts.md),
   [retries](../reliability/retries.md),
   [failover](../reliability/failover.md), and
   [disaster recovery](../reliability/disaster-recovery.md).
3. Read operations pages for
   [observability basics](../operations/observability-basics.md),
   [metrics](../operations/metrics.md), [logs](../operations/logs.md),
   [alerting](../operations/alerting.md), and
   [runbooks](../operations/runbooks.md).
4. Read security pages for [authentication](../security/authentication.md),
   [authorization](../security/authorization.md),
   [audit logs](../security/audit-logs.md), and
   [rate limiting and abuse](../security/rate-limiting-and-abuse.md).
5. Run the [replication lag](https://github.com/LeonSilva15/system-design/tree/main/labs/replication-lag-simulator/),
   [quorum read/write](https://github.com/LeonSilva15/system-design/tree/main/labs/quorum-read-write-simulator/), and
   [hot-key](https://github.com/LeonSilva15/system-design/tree/main/labs/hot-key-demo/) labs.

Goal: find what fails, what must be observable, what data is at risk, and what
can stay simple in version 1.

## A Practical Study Loop

Use this loop for any path:

1. Pick a problem in one sentence.
2. Write three functional requirements and three non-functional requirements.
3. Choose one walkthrough or lab that matches the hardest requirement.
4. Explain which component is justified and what trade-off it introduces.
5. Name one failure mode and one signal that would reveal it.
6. Remove one component and describe the smaller version 1.

This loop keeps the cookbook active. Reading alone is not the goal; explaining
and revising a design is the goal.

## Original Example

Suppose you are designing a small appointment reminder service for a clinic.

- Start with the beginner path to define reminders, patients, providers,
  appointment state, and delivery channels.
- Use the interview path to explain why reminders can be queued, why duplicate
  sends need idempotency, and why failed messages need inspection.
- Use the builder path to run the queue worker and dead-letter queue labs before
  deciding how retries should behave.
- Use the production architecture path to check privacy, audit logs, provider
  outage handling, alerts, and runbooks.

The same design can move through more than one path. That is normal: learning a
system means revisiting it from different constraints.

## Common Mistakes

- Reading component pages before naming requirements.
- Treating walkthroughs as scripts to memorize.
- Running labs without writing down what behavior changed the design.
- Calling a design production-ready before checking observability, security,
  recovery, and cost.
- Adding advanced scale mechanisms before version 1 has a clear bottleneck.

## Checklist

Before moving on, confirm you can answer:

- Which path am I using and why?
- What are the first pages I need for this goal?
- Which lab or walkthrough will make the next decision concrete?
- What requirement justifies the component I am considering?
- What trade-off does that component introduce?
- What can fail, and how would I notice?
- What is the smallest useful version 1?

## Related Pages

- [Learning paths](learning-paths.md)
- [System design process](../method/system-design-process.md)
- [Requirement discovery](../method/requirement-discovery.md)
- [Component selection map](../components/)
- [Labs guide](../labs/)
- [Walkthroughs](../walkthroughs/)
