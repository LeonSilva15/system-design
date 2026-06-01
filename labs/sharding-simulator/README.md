# Sharding Simulator

This lab demonstrates partitioning and sharding behavior with a deterministic
Python model. It shows hash sharding, range sharding, resharding movement, hot
partitions, and cross-shard query limitations.

The example is a community task system. Each task has a record ID, tenant ID,
day, and value. Different shard keys make different workflows local or
cross-shard.

## Goal

Use this lab to learn:

- how hash sharding spreads exact-key records across shards;
- why hashing by record ID makes tenant reports scatter across shards;
- how tenant-key routing can keep tenant queries local;
- why range sharding can create a hot current partition;
- how resharding can move many records;
- why cross-shard reports multiply query work.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/sharding-simulator
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m sharding_simulator.demo
```

You can also run the tests with the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing the shape:

```bash
python -m sharding_simulator.demo --records 30 --shards 4 --new-shards 6
python -m sharding_simulator.demo --hot-writes 30
python -m sharding_simulator.demo --records 12 --shards 2 --new-shards 3
```

## Files

- [design.md](design.md) explains the simplified sharding model and assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects sharding behavior to design trade-offs.

## Related Cookbook Pages

- [Sharding strategies](../../docs/scalability/sharding-strategies.md)
- [Partitioning and sharding](../../docs/data/partitioning-and-sharding.md)
- [Hot key mitigation](../../docs/scalability/hot-key-mitigation.md)
- [Capacity estimation](../../docs/scalability/capacity-estimation.md)

Return to the [labs README](../README.md).
