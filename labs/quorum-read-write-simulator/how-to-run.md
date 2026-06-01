# How To Run The Quorum Read/Write Simulator

## Setup

Use Python 3.11 or newer.

```bash
cd labs/quorum-read-write-simulator
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
```

## Run Tests

```bash
python -m pytest
```

The tests cover write quorum, read quorum, stale reads, unavailable replicas,
latency differences, read repair, demo output, and parameter validation.

If `pytest` is not installed, run the same behavior tests with the standard
library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Run The Demo

```bash
python -m quorum_read_write_simulator.demo
```

Useful parameters:

| Parameter | Default | What It Changes |
| --- | --- | --- |
| `--replicas` | `3` | Number of replicas in the toy cluster |
| `--read-quorum` | `2` | Responses required for a read |
| `--write-quorum` | `2` | Acknowledgements required for a write |
| `--latencies` | `12,35,80` | Per-replica response latency in milliseconds |

Examples:

```bash
python -m quorum_read_write_simulator.demo --read-quorum 1 --write-quorum 2
python -m quorum_read_write_simulator.demo --read-quorum 3 --write-quorum 1
python -m quorum_read_write_simulator.demo --latencies 5,80,120
```

## Troubleshooting

- If imports fail, confirm that commands are run from
  `labs/quorum-read-write-simulator` after installing the package.
- If `pytest` is missing, rerun `python -m pip install ".[test]"` or use the
  `unittest` command above.
- If a quorum parameter is rejected, confirm it is at least 1 and no larger
  than the replica count.
- If `--replicas` is rejected, use at least 3 replicas so the demo can show a
  stale copy, an unavailable copy, and a fresh copy at the same time.
