# Self-Review Checklist

## Purpose

Use this checklist before reading a walkthrough, comparing your answer to
someone else's design, or asking for review. It helps you find missing
requirements, vague component choices, and unhandled failure modes while the
design is still easy to revise.

This is not a scoring rubric. If you want a numeric baseline, use the
[system design rubric](system-design-rubric.md) after this checklist.

## When This Matters

Use this checklist when:

- you finished a timed system design practice answer;
- you drafted a walkthrough and want to find gaps before review;
- your diagram has components that are not yet justified;
- you are about to read a worked solution and want to compare reasoning, not
  memorize the final shape;
- you need a short revision plan.

## How To Use It

1. Write your design without looking at the walkthrough.
2. Review each section below.
3. Mark each prompt `clear`, `missing`, or `needs evidence`.
4. Revise the lowest-confidence sections before reading the walkthrough.
5. After reading, compare the decision path, not just the component list.

If a prompt does not matter for the system, write why. A conscious omission is
better than a hidden gap.

## Requirements

- Can I state the problem in one sentence?
- Did I name the users, operators, administrators, services, or external systems
  involved?
- Did I separate functional requirements from non-functional requirements?
- Did I rank the requirements that change the architecture?
- Did I define version 1 and what is explicitly out of scope?
- Did I avoid vague requirements such as fast, scalable, secure, or real-time
  without a target or workflow?

## Data

- Did I name the core entities and relationships?
- Did I identify the source of truth?
- Did I label derived, cached, indexed, archived, or temporary data?
- Did I explain read-heavy, write-heavy, or mutation-sensitive data paths?
- Did I cover retention, deletion, privacy, or audit needs when relevant?
- Did I choose storage because of data shape and access patterns, not habit?

## Components

- Can I explain why every component exists?
- Does each cache, queue, stream, replica, scheduler, or worker map to a
  requirement, scale assumption, data constraint, or failure mode?
- Did I reject at least one plausible simpler alternative?
- Did I avoid adding future-scale infrastructure before naming the bottleneck?
- Does my diagram show responsibilities rather than generic boxes?

## APIs And Workflows

- Did I sketch the main read path?
- Did I sketch the main write path?
- Do APIs or commands name actors, inputs, outputs, errors, and authorization
  checks?
- Did I define what happens after retries, duplicate requests, or repeated
  submissions?
- Did I include user-visible behavior for success, validation failure, conflict,
  and delayed work?

## Failure And Reliability

- What fails first on the critical path?
- What timeout, retry, or backoff behavior is safe?
- Could a retry create duplicate work or an ambiguous external side effect?
- What should the user see during partial failure?
- What degraded mode is acceptable?
- What needs manual repair, reconciliation, replay, or failover?
- What recovery target matters, such as data loss, downtime, or delayed work?

## Security And Abuse

- Did I name roles, permissions, and trust boundaries?
- Which actions need authorization checks?
- Which data is sensitive, private, regulated, or audit-worthy?
- What abuse path exists: spam, scraping, replay, quota bypass, privilege
  escalation, or data exfiltration?
- Are validation, rate limits, audit logs, and secrets handling placed on
  concrete workflows?
- Did I avoid reducing security to only authentication?

## Observability And Operations

- What metric would show the main user-visible failure?
- What log or trace ID would let an operator debug one request or user?
- Which dashboards or alerts are needed before launch?
- What does an operator do after an alert fires?
- How would a failed background job, stuck queue, stale cache, or provider
  outage be noticed?
- Did I include rollout, rollback, backfill, or runbook concerns when relevant?

## Simplification

- What can I remove from version 1?
- Which manual step is acceptable because it is rare or low risk?
- Which component is only needed after a measured bottleneck?
- What signal would justify adding caching, sharding, replicas, queues, or
  multi-region behavior later?
- Did I explain the trade-off I accept by keeping the design simple?
- Can I still solve the core problem if the advanced component is removed?

## Original Example

Suppose your answer designs a group reading club app.

Initial design:

```text
Use a web API, database, cache, queue, search service, and recommendation
worker. Users join clubs, create reading sessions, and get reminders.
```

Self-review findings:

- Requirements: missing. The answer does not say whether version 1 needs
  recommendations or only club schedules.
- Data: needs evidence. It names sessions but not membership, invitations, or
  the source of truth for attendance.
- Components: missing. Search, cache, queue, and recommendation worker are not
  tied to requirements.
- Failure: missing. Reminder delivery and duplicate session creation are not
  handled.
- Security: needs evidence. Club membership and private sessions imply
  authorization checks.
- Observability: missing. There is no signal for missed reminders or failed
  joins.
- Simplification: clear next step. Version 1 can remove recommendations and
  search, keep a relational database, and revisit search after session count or
  query latency becomes a measured problem.

The improved answer should first define actors, version 1, data ownership, and
the write path for joining or creating a session. Only then should it decide
whether reminders need a queue or search needs a separate component.

## Common Mistakes

- Reading the walkthrough before critiquing your own design.
- Checking only whether your components match the walkthrough.
- Treating a missing advanced component as a flaw when version 1 does not need
  it.
- Ignoring security or observability because the prompt is short.
- Adding reliability language without naming user-visible failure behavior.
- Keeping every component because it appeared in the first diagram.

## Revision Plan Template

```text
Strongest section:
Weakest section:
One missing requirement:
One unjustified component:
One failure mode to add:
One security or abuse question:
One observability signal:
One simplification:
Next revision step:
```

## Related Pages

- [System design rubric](system-design-rubric.md)
- [Design review checklist](../method/design-review-checklist.md)
- [System design process](../method/system-design-process.md)
- [Requirement discovery](../method/requirement-discovery.md)
- [Component selection map](../components/)
- [Walkthroughs](../walkthroughs/)
