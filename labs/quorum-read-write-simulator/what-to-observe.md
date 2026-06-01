# What To Observe

## Write Quorum

The first write returns after the fastest `write_quorum` replicas acknowledge.
With the default settings, two replicas store version 1 while the slowest
replica can remain stale.

Question to ask: Is it acceptable for a write to be acknowledged before every
replica has the new value?

## Read Quorum

The read returns the highest version among the replicas it contacted. A larger
read quorum is more likely to include a fresh copy, but it waits for more
replicas.

Question to ask: Which read paths need fresher data, and which can trade
freshness for latency?

## Unavailable Replicas

The demo marks one replica unavailable before a degraded read. If too few
replicas are available, the operation fails instead of guessing.

Question to ask: Should the product prefer a visible error or a stale answer
when a quorum cannot be reached?

## Stale Reads

The degraded read can include a stale replica. If the quorum misses the newest
copy, the returned version can be stale. Read repair can update stale responders
after a read, but it does not make the original read magically fresh.

The output's `stale` flag describes the returned value, not every response. A
read may contact a stale replica and still return a fresh value if another
responder has the latest version.

Question to ask: Does the client need a version token or leader fallback for
read-your-writes behavior?

## Latency Trade-Offs

Latency is the slowest responder in the quorum. A read quorum of 1 is fast but
can be stale. A full read quorum is fresher in this toy model but waits for the
slowest replica.

Question to ask: Which latency budget matters more: normal fast reads or
stronger freshness during degraded conditions?
