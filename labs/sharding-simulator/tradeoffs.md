# Sharding Trade-Offs

## What Sharding Buys

Sharding can increase data capacity, isolate tenants or ranges, reduce per-node
load, and make operational work safer by moving one shard at a time.

It is useful only when the shard key matches the workload that must remain
local.

## What It Costs

Sharding adds permanent complexity:

- query routing needs a shard key or placement map;
- some queries become scatter-gather operations;
- hot tenants, hot keys, or hot ranges can overload one shard;
- resharding requires copy, verification, cutover, rollback, and monitoring;
- cross-shard transactions are harder to make correct and observable;
- backups, restores, migrations, and repair become shard-aware.

## Hash Sharding

Hash sharding is good for exact-key lookups and ordinary distribution. It is
weak for range scans, tenant reports, and any workflow where related records
need to stay together.

Hashing does not fix a single hot key. All traffic for that key still routes to
one shard unless the workflow changes.

## Range Sharding

Range sharding is good for time-window reads, retention, and archival. It is
weak when most writes target the newest range.

The current range should have a hot-partition plan before traffic arrives.

## Production Differences

A production design would usually add:

- a placement map or routing service;
- tenant movement or range split tooling;
- dual-read or dual-write migration states;
- verification by counts, checksums, or replay positions;
- per-shard metrics for load, errors, lag, and storage growth;
- derived search or reporting stores for broad cross-shard queries.

The lab keeps the mechanics small so the routing trade-off is visible.
