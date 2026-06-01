# Hot-Key Demo

This lab demonstrates how one popular key can overload a partition, cache owner,
or source system even when the rest of the fleet has spare capacity. The demo
uses a public city marathon post as the hot read key and a popularity counter as
the hot write key.

The model is deterministic so learners can change one input at a time and see
how skew, capacity, replication, request coalescing, and write bucketing affect
the outcome.

## Goal

Use this lab to learn:

- how skewed traffic hides behind healthy-looking averages;
- why a hash partition or cache owner can still overload when one key is hot;
- how replicating a hot read key spreads load across cache owners;
- how request coalescing protects the origin during cache refresh storms;
- how bucketed counters reduce pressure on one hot write key;
- which correctness and freshness trade-offs each mitigation introduces.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/hot-key-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m hot_key_demo.demo
```

You can also run the tests with the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing the shape:

```bash
python -m hot_key_demo.demo --hot-fraction 0.75
python -m hot_key_demo.demo --replicas 2 --capacity 260
python -m hot_key_demo.demo --origin-callers 200 --origin-capacity 15
python -m hot_key_demo.demo --hot-writes 900 --write-buckets 12
```

## Files

- [design.md](design.md) explains the simplified hot-key model and assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects the behavior to design trade-offs.

## Related Cookbook Pages

- [Hot key mitigation](../../docs/scalability/hot-key-mitigation.md)
- [Caching strategies](../../docs/scalability/caching-strategies.md)
- [Sharding strategies](../../docs/scalability/sharding-strategies.md)
- [Partitioning and sharding](../../docs/data/partitioning-and-sharding.md)
- [Capacity estimation](../../docs/scalability/capacity-estimation.md)

Return to the [labs README](../README.md).
