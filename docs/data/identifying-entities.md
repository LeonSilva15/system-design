# Identifying Entities

Entity discovery turns product behavior into the nouns, relationships, rules,
and lifecycle states the system must remember.

Do this before choosing tables, collections, topics, caches, or indexes. If you
cannot name the actors, resources, ownership rules, and invariants, the storage
model is still guesswork.

## Purpose

Use entity identification to answer:

- Who acts in the system?
- What resources do they create, inspect, reserve, update, or delete?
- Who owns each resource?
- How do resources relate to each other?
- What lifecycle states matter?
- What invariant must stay true even when two things happen at once?

An entity is not just a table. It is a concept the product and architecture must
reason about.

## When This Matters

This matters when:

- a workflow creates durable state;
- multiple actors can change the same resource;
- permissions depend on ownership or membership;
- a status transition changes what actions are allowed;
- a relationship creates a consistency requirement;
- audit, retention, or deletion rules depend on lifecycle state.

## Questions To Ask

Start with actors:

- Who performs actions?
- Who approves, rejects, audits, or repairs actions?
- Which external systems call or receive data?
- Which background jobs act on behalf of the system?

Then identify resources:

- What does each actor create or change?
- What does each actor search, list, or inspect?
- What needs a stable ID?
- What has a status, owner, timestamp, or audit trail?

Then identify rules:

- Who owns the resource?
- Can ownership transfer?
- Which relationships are required?
- Which relationship must be unique?
- Which lifecycle states allow or block actions?
- Which invariant must never be violated?

## Decision Guidance

### Separate Actors From Resources

Actors do things. Resources are things the system remembers.

Examples:

| Actor | Resource They Touch | Why It Matters |
| --- | --- | --- |
| Member | Reservation | Authorization and ownership |
| Staff reviewer | Approval decision | Audit and privileged actions |
| Reminder worker | Reminder job | Retry and observability |
| Partner service | Import batch | Trust boundary and validation |

Do not model every actor as a user row. A background worker or external system
may need identity in logs, permissions, and audit records even if it is not a
human account.

### Name Ownership

Ownership answers who can see, change, transfer, archive, or delete data.

Common ownership patterns:

- user-owned: one user controls the resource;
- organization-owned: members act through roles;
- system-owned: generated state, jobs, and projections;
- shared: multiple actors have different permissions;
- external-owned: another system is the source of truth.

Ownership affects authorization, deletion, audit, tenancy boundaries, and data
retention.

### Map Relationships

Relationships explain how entities constrain each other:

- one-to-one: one profile belongs to one account;
- one-to-many: one project has many tasks;
- many-to-many: many learners join many study groups;
- hierarchy: folders contain folders and documents;
- membership: users belong to organizations with roles;
- event history: one resource has many state changes.

The most important relationships often become constraints or indexes.

### Define Lifecycle

Lifecycle states describe what can happen next.

Example:

```text
draft -> submitted -> approved -> fulfilled -> closed
                     -> rejected
                     -> cancelled
```

For each state, ask:

- Who can move the entity into this state?
- What data is required before the transition?
- What side effects happen?
- Can the transition be retried?
- Is the transition reversible?
- Does the state affect retention or visibility?

### Identify Invariants

An invariant is a rule that must remain true.

Examples:

- a room cannot have two approved reservations for the same time window;
- an account balance cannot be calculated from unposted ledger entries;
- a deleted workspace cannot accept new projects;
- a user cannot approve their own privileged access request;
- a retry must not create two shipments for one order.

Invariants drive transaction boundaries, uniqueness rules, conditional writes,
idempotency, and conflict handling.

If violating a rule would harm users or operators, write it as an invariant.

## Trade-Offs

Detailed entity modeling improves correctness and makes storage choices easier.
It also takes time and can become too abstract if it drifts away from workflows.

Keep the first model close to product actions. Add more detail when it changes
ownership, lifecycle, consistency, audit, or storage choices.

## Common Mistakes

- Treating UI screens as entities.
- Treating every noun in the prompt as durable data.
- Forgetting background jobs and external systems as actors.
- Modeling only current state and losing lifecycle history.
- Failing to name who owns a resource.
- Hiding many-to-many relationships in comma-separated fields.
- Discovering invariants only after choosing storage.
- Ignoring deletion, retention, and audit states.

## Example

A neighborhood compost pickup service lets residents request pickup bins and
drivers complete pickup routes.

Actors:

| Actor | Actions |
| --- | --- |
| Resident | Requests a bin pickup, cancels a request, views pickup status |
| Driver | Claims a route, marks stops completed or skipped |
| Dispatcher | Assigns drivers, reopens skipped stops, audits route progress |
| Reminder worker | Sends pickup reminders and retryable notifications |

Resources:

| Resource | Owner | Lifecycle |
| --- | --- | --- |
| Pickup request | Resident | requested, scheduled, completed, cancelled, skipped |
| Pickup stop | Dispatch team | planned, assigned, completed, skipped |
| Route | Dispatch team | draft, assigned, in progress, closed |
| Status change | System | appended, retained |
| Reminder job | System | pending, sent, failed, retried |

Relationships:

- one resident can create many pickup requests;
- one route contains many pickup stops;
- one pickup stop points to one pickup request;
- one pickup request can have many status changes;
- one reminder job belongs to one pickup request.

Invariants:

- one pickup request can appear on only one active route at a time;
- a driver cannot complete a stop that is not assigned to their route;
- a cancelled pickup request cannot receive new reminder jobs;
- every dispatcher override must create a status change;
- retrying a reminder job must not send duplicate messages without a recorded
  attempt.

Design consequences:

- Store pickup requests, routes, stops, and status changes in the source of
  truth for version 1.
- Protect route assignment with a transaction or conditional write so one active
  request cannot be assigned twice.
- Keep status changes append-only enough for audit and repair.
- Treat reminder jobs as retryable system-owned resources with logs and metrics.

## Checklist

Before choosing a data model, confirm:

- Human, system, and external actors are named.
- Resources have stable names and IDs.
- Ownership is clear for each resource.
- Relationships are listed, including cardinality where it matters.
- Lifecycle states are named for resources with status changes.
- Allowed and forbidden transitions are clear.
- Invariants are written as concrete rules.
- Each invariant maps to a constraint, transaction, conditional write, or
  idempotency rule.
- Audit, retention, deletion, and privacy needs are identified.
- The model can explain the main read and write paths.

## Related Pages

- [Data overview](./)
- [System design process](../method/system-design-process.md)
- [Requirement discovery](../method/requirement-discovery.md)
- [Design review checklist](../method/design-review-checklist.md)
- [Glossary](../glossary.md)
