# Log Compaction Demo

This lab demonstrates append-only logs and latest-value compaction with a small
deterministic Python model. The example is a community lending inventory stream:
each event records the latest availability for an item, while consumers build
derived projections from offsets.

The lab shows why a stream can keep event history, how a compacted view keeps
only the latest value per key, how consumers track offsets, and how retention
can leave a slow consumer unable to replay from the beginning.

## Goal

Use this lab to learn:

- how append-only records preserve every committed update;
- how latest-value compaction reduces old versions for the same key;
- how consumers read from offsets and maintain their own projection state;
- why retention windows must match replay and backfill promises;
- how tombstones represent deletes in compacted logs;
- what can happen when a consumer offset falls behind retained history.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/log-compaction-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m log_compaction_demo.demo
```

You can also run the tests with the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing the shape:

```bash
python -m log_compaction_demo.demo --batch-size 2
python -m log_compaction_demo.demo --retention-records 3
python -m log_compaction_demo.demo --batch-size 1 --retention-records 6
```

## Files

- [design.md](design.md) explains the simplified log and compaction model.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects log compaction behavior to design
  trade-offs.

## Related Cookbook Pages

- [Streams](../../docs/communication/streams.md)
- [Stream component](../../docs/components/stream.md)
- [Queue component](../../docs/components/queue.md)
- [Idempotency](../../docs/communication/idempotency.md)
- [Capacity estimation](../../docs/scalability/capacity-estimation.md)

Return to the [labs README](../README.md).
