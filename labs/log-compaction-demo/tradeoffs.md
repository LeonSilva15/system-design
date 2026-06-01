# Trade-Offs

## What This Lab Teaches

Append-only logs, compaction, and retention solve different problems. The
append-only log preserves ordered history. Latest-value compaction keeps current
state cheaper to rebuild. Retention limits hot storage. Consumers need offsets
and recovery plans that match those choices.

## Append-Only Log

Append-only records make event order, replay, and consumer independence easier.

Trade-offs:

- storage grows with every update;
- payloads can create privacy and retention obligations;
- consumers must handle duplicate or replayed records safely;
- one hot key can create lag in its partition.

Use an append-only log when event history or independent consumers are real
requirements, not just because async processing is available.

## Latest-Value Compaction

Compaction keeps the newest record for each key and removes older versions.

Trade-offs:

- rebuilding current state becomes cheaper;
- consumers that need every transition cannot rely only on compacted history;
- delete markers need a retention rule;
- compaction work consumes I/O and can hide old debugging context.

Use compaction when current keyed state is the main replay target, such as a
cache, search index, materialized view, or account snapshot.

## Retention

Retention removes old records from hot storage.

Trade-offs:

- shorter retention lowers storage and operating cost;
- longer retention supports debugging, replay, and new consumers;
- too-short retention breaks slow consumers and backfills;
- rich payloads make long retention a privacy and deletion risk.

Retention should be tied to the longest expected replay window, not chosen only
from storage pressure.

## Consumer Offsets

Offsets let consumers checkpoint their progress independently.

Trade-offs:

- independent offsets let one consumer lag without blocking others;
- each consumer needs lag alerts and a recovery path;
- offset commits before side effects can lose work;
- offset commits after side effects can repeat work during retries.

Projection consumers should be idempotent. Side-effect consumers need stronger
dedupe guards before replay.

## Version 1 Simplification

For a first version, use the smallest event history that matches the product
need:

- use a queue if one worker group only needs task delivery;
- use a stream when multiple consumers or replay justify retained history;
- keep payloads minimal and versioned;
- set retention from replay promises;
- add snapshots or source rebuild paths before relying on short retention.

Avoid promising unlimited replay unless storage, privacy, and operations can
support it.
