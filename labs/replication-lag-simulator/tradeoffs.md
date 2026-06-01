# Replication Lag Trade-Offs

## What Replicas Buy

Read replicas can reduce leader read load, isolate reporting queries, and serve
some users from a closer copy. They are valuable when the product can name
which reads are allowed to be stale.

## What They Cost

Replica-backed reads need extra rules:

- followers can be missing a recent write;
- followers can return an older version after a newer leader write;
- read-your-writes can fail without session routing or version tokens;
- lag spikes can push important reads back to the leader;
- dashboards must show lag before users report inconsistent behavior.

## When Follower Reads Fit

Follower reads fit browse pages, reports, dashboards, and search-like views
when stale data is safe and the final write path rechecks the leader.

For the reservation example, browsing room availability may tolerate lag if the
final reserve command checks the leader. A confirmation page after approval
should not use a lagging follower.

## When To Avoid Follower Reads

Avoid follower reads for final booking, payment, permission, quota, inventory,
and confirmation flows that need the latest authoritative state.

The safe rule is "stale view, fresh decision." A follower can help someone
explore options; the leader should decide scarce-resource changes.

## Production Differences

A production design would usually add:

- replication lag metrics based on log position, timestamp, or version;
- read routing with minimum observed version or session affinity;
- leader fallback when lag exceeds a path budget;
- stale or pending labels for replica-backed pages;
- failover rules for promotion and fencing;
- reconciliation for lag, failed replication streams, and stale promotions.

The lab keeps one leader, one follower, and one key so the stale-read behavior
is visible.
