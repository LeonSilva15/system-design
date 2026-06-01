# Functional vs Non-Functional Requirements

Functional requirements describe product behavior. Non-functional requirements
describe the qualities and constraints that shape how that behavior is built.

Both matter. A system that has the right features but the wrong latency,
consistency, security, or recovery behavior still fails the design.

## Purpose

Use this page to separate:

- what the system must let people or services do;
- how well the system must do it;
- which architecture choices each requirement justifies.

This distinction keeps design conversations practical. It helps you avoid
turning every feature into infrastructure and every quality goal into vague
words like fast, reliable, or scalable.

## When This Matters

This split matters when:

- a feature sounds simple but has correctness or latency constraints;
- stakeholders use broad quality words without measurable meaning;
- you need to decide whether to add a cache, queue, replica, lock, rate limit,
  audit log, or separate service;
- version 1 needs to stay small without ignoring user-visible risk;
- a reviewer asks why an architecture choice exists.

## Questions To Ask

For a functional requirement, ask:

- Who performs the action?
- What data does the action read or change?
- What state transition happens?
- Who can see the result?
- What should happen if the same action is repeated?

For a non-functional requirement, ask:

- How fast must the action feel?
- How correct, fresh, durable, or available must the result be?
- What happens when dependencies fail?
- What must be protected from misuse or disclosure?
- What must operators observe or repair?
- What scale dimension could break the simple design?

## Definitions

### Functional Requirements

Functional requirements define the system's behavior from the user's or
integrating service's point of view.

Examples:

- a resident can reserve an appointment;
- staff can approve or cancel a reservation;
- a service can submit a payment authorization request;
- a reader can search saved articles by tag;
- a worker sends a reminder before a deadline.

Functional requirements usually become:

- APIs;
- user workflows;
- commands and queries;
- entities and relationships;
- state machines;
- permissions;
- background jobs.

### Non-Functional Requirements

Non-functional requirements define constraints on the behavior.

Examples:

- a reservation confirmation should be visible within two seconds;
- two users must not receive the same limited slot;
- reminders may be delayed by up to five minutes;
- staff actions must be auditable;
- public search can tolerate stale results;
- abusive clients should not create unbounded work.

Non-functional requirements usually become:

- consistency decisions;
- indexes, caches, replicas, or queues;
- idempotency keys and deduplication;
- rate limits and quotas;
- encryption and authorization boundaries;
- logs, metrics, traces, and alerts;
- backup, restore, and recovery plans;
- operational runbooks or manual repair flows.

## Decision Guidance

### Pair Behavior With Quality

Do not stop at the feature. Add the quality that changes the design.

| Functional Requirement | Non-Functional Requirement | Architecture Impact |
| --- | --- | --- |
| A student reserves a study room. | A room cannot be double-booked for overlapping times. | Transaction, uniqueness rule, or conditional write |
| A reader searches saved articles. | Results may be stale for one minute. | Cache or search index can be refreshed asynchronously |
| A clinic sends appointment reminders. | Delivery can be delayed but must not duplicate messages repeatedly. | Queue, retry policy, idempotency key |
| Staff export monthly activity. | Export can take minutes and should not slow user requests. | Background job and stored export artifact |
| A partner submits an order. | The API must reject invalid signatures and excessive retries. | Authentication, request validation, rate limits |

The same feature can lead to different designs when the quality target changes.

### Make Vague Quality Words Concrete

Replace broad claims with a measurable or observable statement:

| Vague Claim | Better Requirement |
| --- | --- |
| The system should be fast. | The checkout confirmation page should load within 500 ms for cached catalog reads. |
| The system should be reliable. | A failed reminder send should be retried and visible to operators within five minutes. |
| The system should scale. | Signup can peak at 200 reservation writes per minute for the first 10 minutes. |
| The system should be secure. | Only staff with the coordinator role can cancel another user's reservation. |
| The system should be observable. | Each reservation write logs reservation ID, actor ID, slot ID, and conflict outcome. |

If the requirement cannot be measured, observed, or reviewed, it is probably not
specific enough to drive architecture.

### Let Requirements Challenge Components

Use the requirement type to test whether a component is justified:

- A cache needs a freshness requirement.
- A queue needs delayed work, retry, buffering, fanout, or isolation.
- A transaction needs a correctness boundary.
- A read replica needs a read scale or isolation requirement.
- A rate limit needs an abuse, fairness, or cost requirement.
- An audit log needs accountability, compliance, support, or debugging value.

If the design includes a component without a matching requirement, remove it or
write the missing requirement explicitly.

For interviews and reviews, use this answer shape:

```text
Behavior: <what the user or service does>
Quality constraint: <how correct, fast, durable, secure, or observable it must be>
Design consequence: <the simplest architecture choice that satisfies both>
```

The design consequence does not always need new infrastructure. Sometimes the
right version 1 answer is a database constraint, an index, an explicit limit, a
manual review step, or a log field.

## Trade-Offs

Functional requirements help keep the design anchored to user value. If you only
collect functional requirements, the design may ignore correctness, failure,
operations, and cost.

Non-functional requirements make architecture decisions explicit. If you treat
every quality as strict, the design can become too complex for version 1.

The practical balance is to rank non-functional requirements by the damage they
avoid or the user workflow they protect.

## Common Mistakes

- Calling every requirement functional because it appears in the product flow.
- Treating quality goals as slogans instead of measurable constraints.
- Designing for maximum availability, consistency, and scale before knowing
  which workflow needs them.
- Adding a cache without naming acceptable staleness.
- Adding asynchronous work without naming retry and duplicate behavior.
- Ignoring operator and support requirements because they are not end-user
  features.
- Forgetting to record what version 1 will not support.

## Example

A local art studio wants a system for members to reserve shared kiln firing
slots.

Functional requirements:

- Members can request a firing slot for a pottery batch.
- Staff can approve, reschedule, or cancel a slot.
- Members can see the status of their own requests.
- Staff can record that a firing completed or failed.
- The system sends reminders before approved slots.

Non-functional requirements:

- A kiln slot cannot be approved for two batches at the same time.
- Members should see request status changes within a few seconds.
- Reminder delivery may lag by five minutes.
- Staff actions should be auditable because cancellations can affect class
  deadlines.
- Public member search is not needed in version 1.

Architecture consequences:

- Use one durable database for members, slots, requests, and audit records.
- Protect slot approval with a transaction or conditional write.
- Keep reminders in a queue or scheduled job because reminder timing is less
  strict than the approval write path.
- Add structured logs for approval conflicts and cancellation actions.
- Skip search infrastructure in version 1 because no requirement needs it.

## Checklist

Before using requirements to choose architecture, confirm:

- Each product behavior is written as a functional requirement.
- Each quality constraint is written separately from the behavior.
- Vague words such as fast, reliable, scalable, secure, and real-time have been
  made specific.
- Each major component maps to at least one requirement.
- Consistency requirements identify the data that must not conflict.
- Latency requirements identify the user-visible path they protect.
- Async requirements identify retry, duplicate, and delay expectations.
- Security requirements identify actors, permissions, and trust boundaries.
- Observability requirements identify what operators need to debug or repair.
- Version 1 excludes unsupported behaviors explicitly.

## Related Pages

- [Requirement discovery](requirement-discovery.md)
- [System design process](system-design-process.md)
- [Definition of Done](../start-here/definition-of-done.md)
- [Style guide](https://github.com/LeonSilva15/system-design/blob/main/STYLE_GUIDE.md)
