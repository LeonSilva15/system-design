# How To Run

## Setup

Use Python 3.11 or newer.

```bash
cd labs/dead-letter-queue-demo
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
python -m dead_letter_queue_demo.demo
```

Without installing the package:

```bash
PYTHONPATH=src python -m dead_letter_queue_demo.demo
```

## Parameters

| Parameter | Default | Meaning |
| --- | ---: | --- |
| `--max-attempts` | `3` | Retryable attempts before retry exhaustion moves a job to the DLQ |
| `--retry-delay` | `2.0` | Seconds before a retryable failure is visible again |
| `--alert-age` | `10.0` | Oldest open dead-letter age that should alert |
| `--alert-count` | `2` | Open dead-letter count that should alert |

## Example Changes

Exhaust retries sooner:

```bash
python -m dead_letter_queue_demo.demo --max-attempts 2
```

Increase retry delay:

```bash
python -m dead_letter_queue_demo.demo --retry-delay 5
```

Make alerting less sensitive:

```bash
python -m dead_letter_queue_demo.demo --alert-age 30 --alert-count 3
```

This suppresses the count alert in the default scenario. The age alert still
fires because the demo advances time beyond the configured age threshold.

## Troubleshooting

- If `ModuleNotFoundError: No module named 'dead_letter_queue_demo'` appears,
  run from `labs/dead-letter-queue-demo` and use `PYTHONPATH=src`.
- If `pytest` is not installed, either install the test extra or use the
  standard-library unittest command.
- If the demo exits with a parameter error, check that attempts and alert count
  are positive and that retry delay and alert age are valid.
