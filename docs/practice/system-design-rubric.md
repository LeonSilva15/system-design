# System Design Rubric

## Purpose

Use this rubric to score a system design interview answer, walkthrough draft, or
architecture proposal. It turns broad feedback into concrete categories so a
learner can see what to improve next.

Use the [design review checklist](../method/design-review-checklist.md) when you
need pass/fail readiness prompts. Use this rubric when you want a score, a
practice baseline, or a before-and-after comparison.

## When This Matters

Use the rubric when:

- practicing a timed system design prompt;
- comparing two drafts of the same design;
- giving structured feedback to another learner;
- reviewing whether a walkthrough teaches the full decision path;
- deciding which topic to study next.

Do not use the score as a substitute for judgment. A small version 1 design can
score well when it explains its constraints clearly and avoids unjustified
complexity.

## Scoring Scale

Score each category from `0` to `3`.

| Score | Meaning |
| --- | --- |
| 0 | Missing or actively misleading |
| 1 | Mentioned, but vague or not tied to the design |
| 2 | Clear enough for the current scope, with some gaps |
| 3 | Clear, justified, and connected to trade-offs and failure behavior |

There are 10 categories for a maximum score of 30. A score around 18 can be a
useful early draft. A score above 24 should have few major gaps and clear
version 1 boundaries.

A low score in a high-risk category can override a good total. For example, a
payment design with strong communication but missing idempotency or auditability
still needs revision before it is safe to treat as complete.

## Rubric Categories

| Category | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Requirements | No clear problem, actors, or scope | Lists features but mixes goals, assumptions, and future scope | Separates functional and non-functional requirements with some ranking | Names the user problem, system boundary, version 1, and architecture-shaping requirements |
| Data Model | No core entities or source of truth | Names entities but not relationships, ownership, or lifecycle | Defines main entities, relationships, and source of truth | Explains authoritative, derived, cached, retained, deleted, and audited data where relevant |
| APIs And Workflows | No concrete read or write path | Shows happy-path APIs without errors, authorization, or retries | Defines main APIs, read/write paths, and important error cases | Connects APIs to actors, validation, authorization, idempotency, retries, and user-visible outcomes |
| Scaling | Adds scale components without estimates | Gives vague scale words such as large or high traffic | Estimates the main stress dimension and names likely bottlenecks | Uses estimates to justify or reject caches, queues, replicas, sharding, batching, or backpressure |
| Reliability | Assumes dependencies work | Mentions failures without recovery behavior | Covers likely failures, timeouts, retries, and degraded behavior | Explains partial failure, duplicate work, repair, failover, recovery targets, and user/operator impact |
| Security | Says to add authentication only | Mentions security generically | Names actors, roles, sensitive data, and basic abuse controls | Places authorization, privacy, audit, validation, secrets, and abuse controls on concrete workflows |
| Observability | No operational signals | Mentions logs or metrics generically | Ties logs, metrics, traces, dashboards, or alerts to critical paths | Shows how to debug one user-visible issue and how operators notice, triage, and repair failures |
| Cost | Ignores cost | Mentions cost without drivers | Names major cost drivers and a few expensive choices | Connects cost to requirements, usage growth, external services, operational labor, and version 1 simplification |
| Simplicity | Over-designed or unclear version 1 | Mentions version 1 but keeps most advanced components | Defines a smaller version 1 and some revisit signals | Removes unjustified complexity, names rejected alternatives, and states what evidence would justify expansion |
| Communication | Hard to follow or component list only | Some structure, but reasoning is scattered | Explains decisions in a mostly clear order | Presents a coherent story from problem to requirements, choices, trade-offs, failure modes, and next steps |

## How To Use The Score

1. Score each category independently.
2. Write one sentence explaining the score.
3. Pick the lowest two categories as the next revision target.
4. Re-score after revising.
5. Keep the original score so improvement is visible.

Avoid arguing over one-point differences. The goal is to identify the next
useful improvement, not to make the rubric feel mathematical.

## Example: Early Draft Score

Prompt: design a neighborhood tool reservation system.

Draft answer:

```text
Users can reserve tools. Use an API, relational database, cache, queue, and
worker. The system should be scalable and reliable. Send reminder emails before
pickup time.
```

Possible score:

| Category | Score | Reason |
| --- | --- | --- |
| Requirements | 1 | It names reservations but not actors, version 1, constraints, or success criteria |
| Data Model | 1 | It implies tools and reservations but does not define availability, holds, or source of truth |
| APIs And Workflows | 0 | No read path, write path, conflict behavior, or errors |
| Scaling | 0 | Cache and queue are added without load, read/write ratio, or bottleneck |
| Reliability | 1 | Reliability is named, but reminder retry and reservation conflict behavior are missing |
| Security | 0 | No roles, authorization, abuse, or privacy discussion |
| Observability | 0 | No signals for failed reservations or missed reminders |
| Cost | 0 | Cost is ignored even though the draft adds cache, queue, worker, and email delivery |
| Simplicity | 0 | The design starts with advanced components without a smaller version 1 |
| Communication | 1 | The answer is a component list, not a decision path |

Total: `4 / 30`

The next revision should focus on requirements, data ownership, and the write
path before adding components.

## Example: Improved Draft Score

Revised answer:

```text
Version 1 lets residents search available tools, reserve one pickup slot, and
cancel before pickup. Staff can mark tools unavailable after damage. The primary
database owns tools, reservation holds, confirmed reservations, and audit
events. The write path checks the tool and slot inside one transaction so two
users cannot reserve the same item. Reminder emails are queued because they do
not need to block reservation confirmation. Operators track reservation
conflicts, reminder failures, and overdue pickup counts. We skip caching until
search latency exceeds 300 ms at roughly 50 reads per second or database load is
measured as the bottleneck.
```

Possible score:

| Category | Score | Reason |
| --- | --- | --- |
| Requirements | 3 | Version 1, actors, actions, and constraints are clear |
| Data Model | 3 | Source of truth and key entities are named |
| APIs And Workflows | 2 | Main write behavior is clear; API shapes and error cases still need detail |
| Scaling | 2 | It gives a rough read-load threshold and names database load as the bottleneck to watch |
| Reliability | 2 | Queue and conflict handling are covered; retry exhaustion and repair need detail |
| Security | 1 | Staff action exists, but roles and authorization are not placed on workflows |
| Observability | 2 | Critical signals are named, but alert thresholds and IDs need detail |
| Cost | 2 | It removes cache for version 1; external email and operational labor need mention |
| Simplicity | 3 | Version 1 is smaller and includes revisit signals |
| Communication | 3 | The answer reads as a decision path instead of a component list |

Total: `23 / 30`

The next revision should improve security, API details, and reliability repair
paths.

## Interpreting Results

| Total Score | Interpretation | Next Action |
| --- | --- | --- |
| 0-9 | The design is mostly a sketch or component list | Rebuild from requirements, data, and workflows |
| 10-17 | The design has a direction but misses major review areas | Fix the lowest categories before adding more architecture |
| 18-24 | The design is reviewable and likely useful for practice | Tighten trade-offs, failure modes, and operational details |
| 25-30 | The design is strong for its scope | Look for hidden assumptions, over-complexity, and clearer communication |

High scores should still respect scope. Do not add every possible production
topic to a small interview answer if the prompt does not need it.

## Common Mistakes

- Scoring length instead of decision quality.
- Giving high scaling scores because a design includes many components.
- Treating reliability and observability as the same category.
- Ignoring communication even when the architecture is technically reasonable.
- Penalizing simple version 1 designs that clearly name revisit signals.
- Averaging scores without reading the lowest categories.

## Checklist

Before finishing a rubric review, confirm:

- Every required category has a score.
- Each score has a short reason.
- The lowest categories are named as the next improvement target.
- The feedback connects to requirements, trade-offs, and failure behavior.
- The review does not reward memorized architecture shapes.
- The learner knows what to revise next.

## Related Pages

- [Practice overview](./)
- [Design review checklist](../method/design-review-checklist.md)
- [System design process](../method/system-design-process.md)
- [Requirement discovery](../method/requirement-discovery.md)
- [Trade-off vocabulary](../method/tradeoff-vocabulary.md)
- [Walkthroughs](../walkthroughs/)
