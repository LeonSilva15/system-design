# Trade-Off Vocabulary

Trade-offs are the cost of choosing one design over another. Good system design
does not hide that cost. It names what improves, what gets worse, and what would
make the decision change later.

Use this vocabulary when explaining requirements, component choices, and design
review feedback.

## Purpose

This page gives shared language for common engineering trade-offs:

- speed versus correctness;
- consistency versus availability;
- simplicity versus flexibility;
- latency versus throughput;
- storage cost versus query speed;
- isolation versus coordination;
- operational control versus managed convenience.

The point is not to memorize pairs. The point is to communicate the consequence
of a decision clearly enough that another engineer can challenge or approve it.

## When This Matters

Trade-off vocabulary matters when:

- two designs both satisfy the feature but fail in different ways;
- a requirement is vague and needs a measurable quality target;
- a reviewer asks why a simpler component is enough;
- version 1 should avoid future-scale complexity;
- a team needs to agree on what risk it is accepting.

## Questions To Ask

For any major choice, ask:

- What requirement does this choice satisfy?
- What does this choice improve?
- What does it make worse, harder, slower, more expensive, or riskier?
- Who pays the cost: user, operator, developer, business, or future team?
- What assumption makes this trade-off acceptable?
- What metric, incident, cost, or user behavior would make us revisit it?

## Decision Guidance

### Use A Consistent Trade-Off Sentence

Use this format in design reviews:

```text
We choose <option> because <requirement or constraint>.
This improves <benefit>.
It costs <downside>.
We reject <alternative> for now because <reason>.
Revisit when <signal changes>.
```

Example:

```text
We choose a single relational database for reservation state because the main
risk is double booking. This improves correctness and keeps version 1 simple.
It costs some read scalability. We reject sharding for now because peak writes
are still below one request per second. Revisit when write latency or lock
contention becomes measured.
```

### Define The Common Trade-Offs

| Trade-Off | What It Means | Concrete Example |
| --- | --- | --- |
| Latency vs throughput | Optimizing for fast individual responses can conflict with batching more work per unit of time. | Sending each notification immediately lowers delay; batching improves worker efficiency but can delay messages. |
| Consistency vs availability | Strictly coordinated writes can protect correctness but may reject or delay work during partial failure. | A slot booking system refuses confirmation when the database cannot prove the slot is free. |
| Freshness vs cost | Fresher data often requires more reads, writes, invalidation, or coordination. | A dashboard that refreshes every second costs more than one that refreshes every minute. |
| Simplicity vs flexibility | A simple design is easier to build and operate but may support fewer future variations. | One checkout workflow is simpler than a configurable workflow engine. |
| Durability vs latency | Waiting for durable storage improves recovery but can slow the response. | Writing an audit record before confirming an admin action adds work to the request path. |
| Isolation vs efficiency | Isolating workloads protects one path from another but can duplicate infrastructure or data. | Running exports in a background worker protects user requests but adds job state and retry handling. |
| Storage cost vs query speed | Precomputed or indexed data can make reads faster but increases storage and write complexity. | Storing a denormalized member summary speeds profile reads but requires update logic. |
| Build speed vs operational burden | A quick custom component can launch faster but may be harder to monitor, scale, and repair. | A small cron job is fast to build, but a managed scheduler may reduce long-term maintenance. |
| User experience vs abuse resistance | Frictionless flows are easier for legitimate users but can invite spam or expensive work. | Allowing unlimited reservation searches feels easy but may require rate limits later. |
| Automation vs human review | Automation reduces manual work but can make rare edge cases harder to correct. | Auto-approving tool reservations is fast, but staff review may be safer for expensive equipment. |

### Tie Trade-Offs To Requirements

Trade-offs are useful only when tied to a requirement.

Weak:

```text
Queues are more scalable.
```

Stronger:

```text
Use a queue for reminder delivery because reminders can be delayed by five
minutes and should not slow reservation confirmation. The trade-off is extra
job state, retry behavior, and operator visibility.
```

The stronger version names the requirement, benefit, and cost.

### Separate Current Choice From Future Choice

Good trade-off communication distinguishes version 1 from the likely future.

```text
For version 1, use database indexes for catalog search because the catalog is
small and exact filters are enough. This keeps operations simple. Revisit a
separate search index when users need ranking, typo tolerance, or search load
starts competing with reservation writes.
```

This makes simplification explicit instead of accidental.

## Trade-Offs

Using shared vocabulary improves review quality because it turns disagreement
into specific questions. It also has a risk: teams can use familiar trade-off
names as shortcuts without explaining the actual requirement.

Do not say "consistency versus availability" and stop. Say which data must be
consistent, what failure mode affects availability, and what user-visible result
is acceptable.

## Common Mistakes

- Naming only the benefit and hiding the cost.
- Treating a trade-off as universal instead of tied to a requirement.
- Using vague pairs such as speed versus quality without defining the workflow.
- Presenting the rejected alternative as foolish instead of explaining when it
  would be right.
- Ignoring who pays the cost of the decision.
- Forgetting the revisit signal.
- Using advanced terminology to avoid a simple version 1 decision.

## Example

A neighborhood food pantry lets volunteers reserve packing shifts.

Requirement:

```text
Volunteers should not receive two confirmations for the same limited shift.
```

Trade-off statement:

```text
We choose transactional shift reservation writes because duplicate
confirmations would create a staffing problem. This improves correctness and
operator trust. It costs some write-path latency and requires clear conflict
errors. We reject an eventually consistent reservation counter for version 1
because the write volume is low and correctness matters more than accepting
every request during a partial failure. Revisit when measured write contention
prevents volunteers from reserving available shifts.
```

Another requirement:

```text
Reminder messages may arrive up to ten minutes late.
```

Trade-off statement:

```text
We choose a background reminder job because reminder delivery does not need to
block shift reservation. This improves user-facing latency and gives retries a
place to run. It costs job state, duplicate-send protection, and monitoring for
failed reminders. Revisit when reminder delay becomes user-visible or the job
queue delays critical operational work.
```

## Checklist

Before a design review, confirm:

- Each major choice names the requirement it satisfies.
- The benefit is specific.
- The downside is specific.
- The rejected alternative is described fairly.
- The trade-off names who pays the cost.
- Version 1 simplification is explicit.
- Failure, observability, security, and cost consequences are included when
  relevant.
- The decision has a revisit signal.
- The language is concrete enough for another engineer to challenge.

## Related Pages

- [Requirements](../requirements/)
- [Requirement discovery](requirement-discovery.md)
- [Functional vs non-functional requirements](functional-vs-nonfunctional-requirements.md)
- [Scale estimation](scale-estimation.md)
- [System design process](system-design-process.md)
- [Definition of Done](../start-here/definition-of-done.md)
