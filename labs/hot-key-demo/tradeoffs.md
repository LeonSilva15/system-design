# Trade-Offs

## What This Lab Teaches

Hot keys are not solved by generic scale-out. If one key keeps landing on one
owner, the owner remains the bottleneck. The mitigation must match the pressure:
read keys need distribution and refresh control; write keys often need a
correctness decision.

## Read Replication

Replicating a public hot read key can lower cache-owner load quickly.

Trade-offs:

- more copies need invalidation or short freshness windows;
- private or permissioned content needs scoped cache keys and authorization
  safeguards;
- replication can hide origin problems until a coordinated expiry happens;
- memory use rises for the replicated object.

Use it when stale or cached public data is acceptable and per-key load is the
main bottleneck.

## Request Coalescing And Fallback Caps

Coalescing prevents every caller from refreshing the same expired key.

Trade-offs:

- callers may wait for the in-flight refresh;
- a failed refresh needs a clear stale, retry, or error policy;
- fallback caps protect the origin but can return degraded responses;
- coalescing state must be local enough to work and shared enough to matter.

Use it when cache expiry or miss storms create origin spikes.

## Bucketed Writes

Bucketed counters split writes across several keys and aggregate later.

Trade-offs:

- live reads may be approximate or more expensive;
- idempotency and duplicate-event handling matter when writes are retried;
- bucket count becomes a tuning knob;
- bucket migration needs care if traffic grows.

Use it for likes, views, reactions, quotas, and analytics counters where exact
real-time values are not required.

## Serialization

The lab does not serialize scarce-resource writes, but production systems often
must. Inventory, booking slots, and payment decisions need an authoritative path
even when the key is hot.

Trade-offs:

- serialization protects correctness but caps throughput for that key;
- users may see more latency or queued work;
- side effects should move after the authoritative decision;
- admission control may be better than letting retries overload the source.

Use it when splitting the write would violate the product invariant.

## Version 1 Simplification

For a first version, measure top keys and apply the smallest mitigation that
matches the risk:

- cache and coalesce refresh for hot public reads;
- cap origin fallback before it harms unrelated traffic;
- bucket only approximate counters;
- serialize scarce writes instead of pretending they can be cached away.

Avoid adding a complex global routing layer before proving that one named key is
the bottleneck.
