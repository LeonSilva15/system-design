# How To Run The Replication Lag Simulator

## Setup

Use Python 3.11 or newer.

```bash
cd labs/replication-lag-simulator
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
```

## Run Tests

```bash
python -m pytest
```

The tests cover leader visibility, follower lag, stale reads, read-your-writes
violations, leader fallback with a minimum observed version, and demo scenarios.

If `pytest` is not installed, run the same behavior tests with the standard
library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Run The Demo

```bash
python -m replication_lag_simulator.demo
```

Useful parameters:

| Parameter | Default | What It Changes |
| --- | --- | --- |
| `--lag` | `5.0` | Seconds before a leader write reaches the follower |
| `--half-step` | `2.5` | Seconds before the second leader write |

Examples:

```bash
python -m replication_lag_simulator.demo --lag 2 --half-step 1
python -m replication_lag_simulator.demo --lag 8 --half-step 3
python -m replication_lag_simulator.demo --lag 0
```

## Troubleshooting

- If imports fail, confirm that commands are run from
  `labs/replication-lag-simulator` after installing the package.
- If `pytest` is missing, rerun `python -m pip install ".[test]"` or use the
  `unittest` command above.
- If every follower read is current, check whether `--lag 0` was used.
