# Quorum Read/Write Trade-Offs

## What Quorums Buy

Quorums let a replicated system make progress without waiting for every
replica. They can improve latency and tolerate some unavailable replicas while
still requiring more than one response.

## What They Cost

Quorum settings create trade-offs:

- small read quorums can be fast but stale;
- large read quorums wait for slower replicas;
- small write quorums can acknowledge before every replica is updated;
- large write quorums reduce stale copies but fail under more outages;
- unavailable replicas can make reads or writes impossible;
- read repair improves convergence but does not fix the read that already
  returned.

## R + W > N

A common rule of thumb is that `read_quorum + write_quorum > replica_count`
creates quorum intersection in a fixed membership set when operations really
touch the selected replicas and the system can compare versions correctly. This
lab shows the intuition, but it is still simplified. Real systems also need
clear version selection, conflict handling, repair, membership changes, timeout
behavior, and failure detection.

## When This Pattern Fits

Quorum reads and writes fit systems that replicate data across several nodes
and can choose a trade-off between latency, availability, and stale-read risk.

Use stronger quorums for workflows where stale reads are dangerous. Use smaller
quorums only when the product can tolerate stale data or has a later
authoritative check.

## When To Avoid It

Avoid treating quorum settings as a substitute for product guarantees. A final
reservation, payment, permission, or inventory decision still needs a clear
source of truth and conflict handling.

## Production Differences

A production design would usually add:

- durable replication logs;
- conflict detection for concurrent writes;
- hinted handoff or anti-entropy repair;
- timeout and retry policy;
- health checks and membership changes;
- version vectors or timestamps instead of one simple counter;
- dashboards for stale reads, failed quorums, repair backlog, and tail latency.

The lab keeps one key and deterministic latencies so the quorum behavior is easy
to inspect.
