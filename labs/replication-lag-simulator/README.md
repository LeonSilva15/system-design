# Replication Lag Simulator

This lab demonstrates stale reads caused by leader/follower replication lag
with a small deterministic Python model. It shows leader writes, delayed
follower application, stale reads, read-your-writes violations, and a
minimum-version read that routes to the leader when the follower is behind.

The example is a community room reservation record. A coordinator writes an
updated approval on the leader, while a browse or status page reads from a
lagging follower.

## Goal

Use this lab to learn:

- why a leader write can be durable before a follower can read it;
- how follower lag appears as missing or stale data;
- why a user can violate read-your-writes after a successful write;
- how minimum observed version routing can protect confirmation-style reads;
- which lag signals help decide when a replica-backed path is unsafe.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/replication-lag-simulator
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m replication_lag_simulator.demo
```

You can also run the tests with the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing the lag window:

```bash
python -m replication_lag_simulator.demo --lag 2 --half-step 1
python -m replication_lag_simulator.demo --lag 8 --half-step 3
python -m replication_lag_simulator.demo --lag 0
```

With `--lag 0`, the follower can be current immediately. The demo still prints
the same scenario labels so you can compare the fields against a lagging run.

## Files

- [design.md](design.md) explains the simplified replication model and
  assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects replica lag behavior to design
  trade-offs.

## Related Cookbook Pages

- [Replication](../../docs/data/replication.md)
- [Consistency models](../../docs/data/consistency-models.md)
- [Read and write patterns](../../docs/data/read-write-patterns.md)
- [Metrics](../../docs/operations/metrics.md)

Return to the [labs README](../README.md).
