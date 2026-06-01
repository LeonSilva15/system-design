# How To Run The Sharding Simulator

## Setup

Use Python 3.11 or newer.

```bash
cd labs/sharding-simulator
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
```

## Run Tests

```bash
python -m pytest
```

The tests cover deterministic hash routing, local exact-key lookup,
cross-shard tenant queries, tenant-local routing, range routing, hot current
partitions, reshard movement, demo output, and parameter validation.

If `pytest` is not installed, run the same behavior tests with the standard
library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Run The Demo

```bash
python -m sharding_simulator.demo
```

Useful parameters:

| Parameter | Default | What It Changes |
| --- | --- | --- |
| `--records` | `18` | Number of normal records inserted into the hash-sharded store |
| `--shards` | `3` | Original hash shard count |
| `--new-shards` | `4` | New hash shard count for the reshard estimate |
| `--hot-writes` | `12` | Current-day writes inserted into the range-sharded store; use at least `2` |

Examples:

```bash
python -m sharding_simulator.demo --records 30 --shards 4 --new-shards 6
python -m sharding_simulator.demo --hot-writes 30
python -m sharding_simulator.demo --records 12 --shards 2 --new-shards 3
```

## Troubleshooting

- If imports fail, confirm that commands are run from `labs/sharding-simulator`
  after installing the package.
- If `pytest` is missing, rerun `python -m pip install ".[test]"` or use the
  `unittest` command above.
- If a parameter is rejected, use positive counts for records and shards, and
  use at least 2 hot writes.
