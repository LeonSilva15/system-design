# Data

Data modeling turns product behavior into durable state, relationships, and
access paths. A good data model starts with the workflow, not the database
product.

Use this section when deciding what data exists, who owns it, how it changes,
how it is read, and what guarantees it needs.

## Purpose

Data choices answer questions such as:

- Which entities does the system manage?
- How are those entities related?
- Which reads and writes shape the model?
- Which data must survive failures?
- Which data must be fresh, consistent, or conflict-free?
- Which storage model is justified by the access pattern?

The goal is to connect product behavior to storage decisions before choosing a
database, cache, index, stream, or analytics store.

## When This Matters

Data modeling matters when:

- a feature creates or changes durable state;
- two users can act on the same resource at the same time;
- a read path needs a specific shape, filter, sort, or freshness guarantee;
- old data must be retained, archived, deleted, or audited;
- a storage choice would make version 1 harder to operate;
- a later walkthrough needs a clear source of truth.

## Questions To Ask

Start with the product workflow:

- What is the user trying to create, reserve, send, buy, schedule, or inspect?
- Which actor owns or can change each piece of data?
- Which relationships matter: one-to-one, one-to-many, many-to-many, hierarchy,
  membership, ownership, or event history?
- Which reads must be fast?
- Which writes must be correct under concurrency?
- Which data can be recomputed, and which cannot be lost?
- Which data can be stale, and for how long?
- Which data needs privacy, retention, deletion, or audit rules?

## Decision Guidance

### Identify Entities And Relationships

Entities are the nouns the system must remember. Relationships explain how those
nouns constrain each other.

Example:

```text
A repair clinic has residents, mechanics, appointment slots, repair requests,
status changes, and reminder jobs.
```

Important relationships:

- one resident can create many repair requests;
- one mechanic has many appointment slots;
- one slot can have at most one approved request;
- one request can have many status changes;
- one reminder job belongs to one request.

The relationship "one slot can have at most one approved request" is not just a
schema detail. It creates a consistency requirement.

### Map Access Patterns

Access patterns describe how the data is used:

- lookup by ID;
- list by owner, status, or time window;
- search by text or tags;
- append event history;
- update current state;
- aggregate counts or reports;
- expire old data.

Design for the important read and write paths. A model that is elegant on paper
but cannot answer the main query is not useful.

### Choose Storage From Data Shape

Storage decisions should follow the data shape and access pattern:

- Use relational tables when relationships, constraints, transactions, and
  flexible queries matter.
- Use document-style storage when an aggregate is usually read and written as
  one object.
- Use key-value storage when access is mostly by key and the value shape is
  simple.
- Use object storage for large blobs that do not belong in the primary
  transactional database.
- Use search indexes when ranked, text-heavy, or faceted retrieval is a core
  requirement.
- Use analytical stores when reporting scans and aggregations should not compete
  with operational traffic.

These are starting points, not rules. The same product may use more than one
storage shape, but version 1 should start with the fewest justified stores.

### Decide Durability

Durability asks what must survive failures and for how long.

Classify data:

- authoritative: cannot be lost without user or business harm;
- audit: needed to explain or repair decisions;
- derived: can be rebuilt from authoritative data;
- temporary: can expire or be dropped safely;
- external: owned by another system and referenced locally.

This classification affects backups, retention, replication, object storage,
and whether a failed write should block the user.

### Decide Consistency

Consistency asks what must be true when data is read or written.

Common questions:

- Must users read their own writes immediately?
- Can two actors update the same entity at the same time?
- What conflict must never happen?
- Can a list or dashboard be stale?
- Are duplicate commands safe?
- Does an event or message need idempotency?

Prefer strong guarantees only where the workflow needs them. A reservation
confirmation may need conflict-free writes, while an analytics dashboard can
often lag.

## Data Pages

Current pages:

- [Data overview](./)
- [Identifying entities](identifying-entities.md)
- [Read and write patterns](read-write-patterns.md)
- [Relational vs document vs key-value](relational-vs-document-vs-key-value.md)

Planned pages:

- `docs/data/consistency-models.md`

These paths become linked pages as their tickets are completed.

## Trade-Offs

Data modeling trades simplicity against future flexibility.

- A normalized relational model can protect consistency, but joins and schema
  changes may need care.
- A denormalized model can make reads fast, but writes and backfills become
  more complex.
- A cache can reduce load, but stale reads and invalidation become design
  concerns.
- A separate analytical store can protect user traffic, but pipelines add delay
  and failure modes.

Name the requirement before adding another store or derived copy.

## Common Mistakes

- Choosing a database before identifying entities and access patterns.
- Modeling only current state and forgetting audit or lifecycle history.
- Treating every read as fresh and every write as strongly consistent.
- Adding a cache before naming acceptable staleness.
- Storing large blobs in the transactional database by default.
- Ignoring retention, deletion, backups, and restore time.
- Letting analytics queries compete with the critical write path.

## Example

A neighborhood equipment library lets members reserve shared tools.

Entities:

- member;
- tool;
- pickup window;
- reservation;
- reservation status change;
- reminder job.

Access patterns:

- members search available tools by category and pickup date;
- members view their own reservations;
- staff list overdue reservations;
- staff update reservation state;
- a reminder worker finds upcoming approved pickups.

Storage guidance:

- Keep tools, members, reservations, and status changes in one relational
  database for version 1.
- Use a uniqueness rule or transaction to prevent two approved reservations for
  the same tool and pickup window.
- Store reminder jobs as durable rows or in a persisted queue because delayed
  delivery is acceptable but silent loss is not.
- Avoid a separate search service until tool catalog search needs ranking, typo
  tolerance, or measured read load relief.

Durability:

- reservations and status changes are authoritative;
- reminder jobs are retryable but should be visible to operators;
- search results are derived and can be rebuilt.

Consistency:

- reservation approval must prevent double booking;
- a member should read their own new reservation immediately;
- staff dashboards can lag by a short interval if the source of truth is still
  correct.

## Checklist

Before choosing storage, confirm:

- Core entities are named.
- Relationships and ownership are clear.
- Main read and write access patterns are listed.
- Authoritative, derived, temporary, and audit data are separated.
- Durability expectations are explicit.
- Consistency needs are tied to specific workflows.
- Storage choices map to data shape and access patterns.
- Version 1 uses the fewest stores that satisfy the requirements.
- Future data pages or decision records can link back to this overview.

## Related Pages

- [System design process](../method/system-design-process.md)
- [Requirement discovery](../method/requirement-discovery.md)
- [Functional vs non-functional requirements](../method/functional-vs-nonfunctional-requirements.md)
- [Design review checklist](../method/design-review-checklist.md)
- [Requirements](../requirements/)
- [Components](../components/)
- [Glossary](../glossary.md)
- [Documentation index](../)
