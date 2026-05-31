# Requirement Discovery

Requirement discovery turns a vague prompt into design constraints. The goal is
not to ask every possible question. The goal is to find the few answers that
will change the architecture.

Use this page before drawing components or choosing storage.

## Purpose

A good system design starts with explicit requirements:

- functional requirements: what the system must do;
- non-functional requirements: how the system must behave under constraints;
- excluded requirements: what version 1 will not do yet.

The discovery step protects the design from two common mistakes: building for a
problem the user did not ask for, and adding infrastructure before the
constraint is real.

## When This Matters

Use requirement discovery when:

- the prompt is broad, such as "design a booking system";
- stakeholders disagree about what success means;
- performance, consistency, reliability, privacy, or cost could change the
  architecture;
- you need to explain why a design choice is justified;
- you are deciding what belongs in version 1.

## Questions To Ask

Ask questions in groups. Stop when the answer no longer changes the design.

### Problem And Scope

- What user problem are we solving?
- Which user action proves the system is useful?
- Which workflows are explicitly out of scope for version 1?
- Is this an internal tool, public product, partner API, or background platform?
- What is the simplest useful launch scenario?

### Actors And Permissions

- Who creates, reads, updates, deletes, approves, or audits data?
- Which actors are human users, operators, services, or external systems?
- Which actions require authorization?
- Are there untrusted users, abusive clients, or partner systems?
- Who needs an admin or support workflow when something goes wrong?

### Functional Requirements

- What must a user be able to do first?
- What are the main read flows?
- What are the main write flows?
- Which state transitions matter?
- Which notifications, callbacks, exports, imports, or reports are required?
- What should happen when a user repeats the same action?

### Non-Functional Requirements

- Which requests need low latency?
- Which data must be strongly consistent?
- Which data can be stale, delayed, or eventually corrected?
- What availability is expected for the critical path?
- How much data is created and retained?
- What peak read, write, fanout, or storage dimension could stress the system?
- What privacy, security, compliance, or abuse risks matter?
- What cost limit or operational constraint should shape the design?

### Failure And Recovery

- What can fail without user-visible harm?
- What needs retry, deduplication, or manual repair?
- What happens if a downstream system is slow or unavailable?
- How should the system behave during partial outage?
- What should operators measure, search, or alert on?

## Functional Versus Non-Functional Requirements

Functional requirements describe product behavior. They usually become APIs,
workflows, entities, state transitions, and permissions.

Non-functional requirements describe quality constraints. They usually become
architecture choices: consistency model, storage strategy, caching, queues,
replication, rate limits, observability, and operational procedures.

Use this split:

| Requirement Statement | Type | Later Design Impact |
| --- | --- | --- |
| A member can reserve a pickup slot. | Functional | Reservation API, slot entity, write path |
| Two members cannot reserve the same slot. | Non-functional | Transaction, uniqueness rule, lock, or conflict check |
| Confirmation should appear within one second. | Non-functional | Read path, indexes, cache only if freshness permits |
| Staff can cancel unsafe requests. | Functional | Admin workflow, authorization, audit record |
| Reminder delivery can be delayed by minutes. | Non-functional | Queue or scheduled worker instead of inline send |

Some statements have both product and quality parts. Split them so the design
can treat each part directly.

## Mapping Requirements To Design Choices

Every architecture choice should trace back to a requirement or constraint.

| Discovery Answer | Design Question It Triggers |
| --- | --- |
| Users need instant reads of mostly unchanged data. | Can a cache help, and what staleness is acceptable? |
| Writes must prevent conflicting updates. | Do we need transactions, conditional writes, or a single writer? |
| Work can finish after the response. | Should asynchronous workers and retry queues handle it? |
| Events fan out to many recipients. | Do we need batching, backpressure, and delivery state? |
| Data grows quickly but old data is rarely read. | Do we need retention rules, archival, partitioning, or cold storage? |
| Users belong to organizations or roles. | Where do authorization checks live? |
| Operators must debug one failed action. | Which IDs, logs, traces, metrics, and audit records are required? |
| Abuse can create expensive work. | Where should rate limits, quotas, validation, or moderation happen? |

If a component cannot be mapped to one of these answers, do not add it yet.

## Decision Guidance

### Start Broad, Then Narrow

Begin with the user outcome, then move toward the architecture-shaping details.

```text
What is the user trying to finish?
Who else touches that workflow?
What data changes?
What must be fast, correct, durable, private, or observable?
What can be simpler in version 1?
```

Do not start with "Should we use a queue?" Start with "Does any work need to
finish after the response, be retried, or be isolated from the user request?"

### Rank Requirements By Design Impact

Not every requirement deserves the same design weight.

High-impact requirements usually involve:

- correctness under concurrency;
- latency on the critical user path;
- high write volume, read volume, storage growth, or fanout;
- regulatory, privacy, or abuse constraints;
- failure recovery and operator visibility.

Low-impact requirements can often be handled with simple application logic or a
manual process in version 1.

### Turn Answers Into Assumptions

When an answer is unknown, write an assumption instead of silently designing
around a guess.

Example:

```text
Assumption: pickup reservations peak at 20 writes per minute during signup
windows. If writes are closer to 2,000 per minute, revisit the single-database
write path and conflict handling.
```

Assumptions make it clear when the design should change.

### Keep Version 1 Honest

Discovery should reduce scope as well as add clarity.

Ask:

- Which workflow proves the system works?
- Which rare case can be handled manually?
- Which report can be delayed?
- Which integration can be replaced with a CSV upload for the first release?
- Which scale number is not real yet?

## Trade-Offs

Requirement discovery improves architecture quality because it makes constraints
visible before design choices harden. The trade-off is that it can slow down the
first sketch and expose missing product decisions.

Too little discovery leads to technology-first architecture. Too much discovery
turns early design into a survey. Use enough questioning to justify the next
decision.

## Common Mistakes

- Asking only about features and skipping latency, consistency, failure, and
  observability.
- Treating "scale" as a single concern instead of asking which dimension grows.
- Accepting vague words like fast, reliable, secure, and real-time without
  defining what they mean for one workflow.
- Designing for every future integration before version 1 has a useful path.
- Forgetting operators, support users, and background jobs as actors.
- Failing to record assumptions when stakeholders do not know the answer yet.
- Adding a cache, queue, search index, or distributed store without tying it to a
  discovered requirement.

## Example

A weekend repair clinic wants a small system for residents to reserve bicycle
repair appointments.

Discovery prompts and answers:

| Prompt | Answer | Requirement Type | Design Impact |
| --- | --- | --- | --- |
| What proves the system is useful? | A resident gets a confirmed repair slot. | Functional | Reservation creation and confirmation flow |
| Can two residents get the same slot? | No, each mechanic can handle one bike at a time. | Non-functional | Conflict check or transaction around slot assignment |
| How fast must confirmation be? | Within a few seconds is fine. | Non-functional | Simple synchronous write is acceptable |
| Are reminders required? | Yes, but they can arrive later. | Functional and non-functional | Store reminder jobs and process asynchronously |
| Who handles exceptions? | Clinic staff can cancel no-shows and unsafe requests. | Functional | Staff role, cancellation state, audit note |
| What scale matters? | Signup opens Monday morning and may create a short write spike. | Non-functional | Index slots, protect writes, postpone sharding |
| What should operators observe? | Failed reminders and duplicate-slot conflicts. | Non-functional | Metrics and logs with reservation ID and slot ID |

Version 1 design consequences:

- Use one relational database for mechanics, slots, reservations, and audit
  notes.
- Enforce one reservation per mechanic slot with a uniqueness rule or
  transaction.
- Keep reminder delivery outside the request path because delayed reminders are
  acceptable.
- Add staff cancellation and audit notes because exception handling is part of
  the real workflow.
- Defer multi-location routing, complex waitlists, and advanced search until the
  clinic actually operates in more places.

## Checklist

Before leaving requirement discovery, confirm:

- The problem statement names the user, job, and system boundary.
- Actors include users, operators, services, and external systems.
- Functional requirements are listed separately from non-functional
  requirements.
- The critical read and write workflows are named.
- Correctness, latency, availability, scale, security, privacy, cost, and
  observability have been considered where relevant.
- Unknown answers are recorded as assumptions.
- Each major design choice maps to a requirement or constraint.
- Version 1 scope is explicit.
- Excluded features and future revisits are named.

## Related Pages

- [System design process](system-design-process.md)
- [Definition of Done](../start-here/definition-of-done.md)
- [Templates](../../templates/README.md)
- [Content guardrails](../../CONTENT_GUARDRAILS.md)
- [Style guide](../../STYLE_GUIDE.md)
