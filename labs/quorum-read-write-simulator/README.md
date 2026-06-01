# Quorum Read/Write Simulator

This lab demonstrates quorum read/write trade-offs with a small deterministic
Python model. It shows read quorum, write quorum, unavailable replicas, stale
reads, read repair, and latency trade-offs.

The example is a replicated reservation status record. The cluster stores one
key on multiple replicas, and reads or writes return after the fastest quorum
responds.

## Goal

Use this lab to learn:

- how write quorum controls how many replicas acknowledge a new version;
- how read quorum controls how many replicas are consulted;
- why unavailable replicas can make an operation fail even when some copies are
  healthy;
- how a small read quorum can return stale data;
- why larger quorums usually increase latency;
- how read repair can update stale responders after a read.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/quorum-read-write-simulator
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m quorum_read_write_simulator.demo
```

You can also run the tests with the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing quorum sizes and latency:

```bash
python -m quorum_read_write_simulator.demo --read-quorum 1 --write-quorum 2
python -m quorum_read_write_simulator.demo --read-quorum 3 --write-quorum 1
python -m quorum_read_write_simulator.demo --latencies 5,80,120
```

## Files

- [design.md](design.md) explains the simplified quorum model and assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects quorum behavior to design trade-offs.

## Related Cookbook Pages

- [Consistency models](../../docs/data/consistency-models.md)
- [Replication](../../docs/data/replication.md)
- [Read and write patterns](../../docs/data/read-write-patterns.md)
- [Metrics](../../docs/operations/metrics.md)

Return to the [labs README](../README.md).
