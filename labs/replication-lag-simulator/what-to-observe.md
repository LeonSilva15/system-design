# What To Observe

## Leader Writes

The first write appears on the leader immediately. This is the authoritative
copy and the place to read when a workflow needs current state.

Question to ask: Which system paths must use the leader after a write?

## Follower Lag

The first follower read returns no value because the replication event has not
reached the follower yet. The leader has version 1 while the follower has
version 0.

Question to ask: Is a missing or old follower value acceptable for this product
path?

## Stale Reads

After the first event applies, the follower shows version 1 while the leader is
already at version 2. The follower has data, but it is stale.

Question to ask: Can the UI label this state, or should the read route away
from the follower?

## Read-Your-Writes Violations

The demo passes `min_version` after a write. A follower read that returns an
older version fails the read-your-writes check.

Question to ask: Does the write response need to carry a version, timestamp, or
token that later reads can use?

## Leader Fallback

The minimum-version read routes to the leader when the follower is behind. This
preserves user trust for confirmation-style reads, but it also sends more load
to the leader during lag spikes.

Question to ask: Which reads deserve fallback, and which can show stale or
pending data instead?

## Lag Observability

Watch `versions_behind`, `pending_events`, and `next_apply`. These signals show
whether the follower is safe for replica-backed paths.

Question to ask: Should an alert fire on raw lag, oldest pending event age, or a
user-facing stale-read budget?
