# Expected Output

The default command:

```bash
python -m replication_lag_simulator.demo
```

prints output similar to:

```text
config lag=5.0s half_step=2.5s
01 leader write: key=reservation:community-room value=approved by coordinator version=1
02 leader read sees write: source=leader value=approved by coordinator version=1 leader_version=1 stale=no read_your_writes_ok=yes note=authoritative read
03 follower read is stale: source=follower value=None version=0 leader_version=1 stale=yes read_your_writes_ok=no note=read-your-writes violation on follower
04 lag status: leader_version=1 follower_version=0 versions_behind=1 pending_events=1 next_apply=5.0s
05 second leader write: value=approved with projector version=2
06 follower still violates read-your-writes: source=follower value=None version=0 leader_version=2 stale=yes read_your_writes_ok=no note=read-your-writes violation on follower
07 first write reaches follower: leader_version=2 follower_version=1 versions_behind=1 pending_events=1 next_apply=2.5s
08 follower stale behind second write: source=follower value=approved by coordinator version=1 leader_version=2 stale=yes read_your_writes_ok=yes note=follower is behind the leader
09 min-version read routes fresh: source=leader_fallback value=approved with projector version=2 leader_version=2 stale=no read_your_writes_ok=yes note=follower lag exceeded minimum version; routed to leader
10 follower caught up: leader_version=2 follower_version=2 versions_behind=0 pending_events=0 next_apply=none
11 follower read is current: source=follower value=approved with projector version=2 leader_version=2 stale=no read_your_writes_ok=yes note=follower is caught up
```

The important fields are `source`, `version`, `leader_version`, `stale`,
`read_your_writes_ok`, `versions_behind`, and `next_apply`.

If you run with `--lag 0`, the follower can be current immediately even though
the step labels still describe the lag scenario. Trust the output fields when
experimenting with custom parameters.
