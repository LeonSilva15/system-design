# How To Run

## Setup

Use Python 3.11 or newer.

```bash
cd labs/log-compaction-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
```

## Run Tests

```bash
python -m pytest
```

Standard-library fallback:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Run The Demo

```bash
python -m log_compaction_demo.demo
```

Without installing the package:

```bash
PYTHONPATH=src python -m log_compaction_demo.demo
```

## Parameters

| Parameter | Default | Meaning |
| --- | ---: | --- |
| `--batch-size` | `3` | Maximum records a consumer reads per poll |
| `--retention-records` | `5` | Number of latest records retained in the hot log |

## Example Changes

Make the consumer progress more slowly:

```bash
python -m log_compaction_demo.demo --batch-size 1
```

Shorten retention:

```bash
python -m log_compaction_demo.demo --retention-records 3
```

This should report a `consumer catch-up gap` for the existing projection and a
separate `retention gap` for the new backfill consumer.

Keep more history:

```bash
python -m log_compaction_demo.demo --retention-records 6
```

## Troubleshooting

- If `ModuleNotFoundError: No module named 'log_compaction_demo'` appears, run
  from `labs/log-compaction-demo` and use `PYTHONPATH=src`.
- If `pytest` is not installed, either install the test extra or use the
  standard-library unittest command.
- If the demo exits with a parameter error, check that `--batch-size` and
  `--retention-records` are positive integers.
