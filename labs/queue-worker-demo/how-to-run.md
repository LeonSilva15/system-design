# How To Run The Queue Worker Demo

## Setup

Use Python 3.11 or newer.

```bash
cd labs/queue-worker-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
```

## Run Tests

```bash
python -m pytest
```

The tests cover enqueue and completion, retry delay, retry exhaustion,
visibility timeout redelivery, stale acknowledgement rejection, metrics, and
the learner-facing demo.

If `pytest` is not installed, run the same behavior tests with the standard
library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Run The Demo

```bash
python -m queue_worker_demo.demo
```

Useful parameters:

| Parameter | Default | What It Changes |
| --- | --- | --- |
| `--visibility-timeout` | `5.0` | How long a claimed job stays hidden before redelivery |
| `--retry-delay` | `3.0` | How long retryable failures wait before becoming visible |
| `--max-attempts` | `3` | How many attempts a retryable job gets before dead-lettering |

Examples:

```bash
python -m queue_worker_demo.demo --visibility-timeout 2
python -m queue_worker_demo.demo --retry-delay 1 --max-attempts 2
python -m queue_worker_demo.demo --visibility-timeout 8 --retry-delay 4
```

## Troubleshooting

- If imports fail, confirm that commands are run from `labs/queue-worker-demo`
  after installing the package.
- If `pytest` is missing, rerun `python -m pip install ".[test]"` or use the
  `unittest` command above.
- If output timing looks different, check the CLI parameters. The lab uses a
  manual clock, so the only time changes come from the demo steps.
