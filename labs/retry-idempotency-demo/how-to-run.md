# How To Run

Run commands from this lab directory.

Use Python 3.11 or newer. If `python` points to an older interpreter, use
`python3.11` in the commands below.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
```

## Run Tests

```bash
python -m pytest
```

The tests are also runnable with the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Run Demo

```bash
python -m retry_idempotency_demo.demo
```

## Parameters

| Parameter | Default | What It Changes |
| --- | --- | --- |
| `--mode` | `both` | Runs `unsafe`, `safe`, or both request flows |
| `--attempts` | `3` | Number of duplicate client attempts |
| `--event-deliveries` | `2` | Number of duplicate event deliveries |
| `--member` | `member-7` | Member identity used in the request fingerprint |
| `--workshop` | `workshop-python` | Workshop identity used in the request fingerprint |
| `--idempotency-key` | `reserve-2026-05` | Stable key reused across request retries |
| `--show-conflict` | `false` | Reuses the same key with a different workshop to show conflict handling |

## Example Commands

Only show the unsafe retry behavior:

```bash
python -m retry_idempotency_demo.demo --mode unsafe --attempts 3
```

Only show the safe idempotency behavior:

```bash
python -m retry_idempotency_demo.demo --mode safe --attempts 4
```

Show key conflict handling:

```bash
python -m retry_idempotency_demo.demo --mode safe --show-conflict
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError` | Package was not installed in the active environment | Run `python -m pip install ".[test]"`, or prefix commands with `PYTHONPATH=src` |
| `pytest` is missing | Test dependency was not installed | Re-run setup command or use the `unittest` command |
| `python` uses an older version | Local shell points to an older interpreter | Use `python3.11` for setup and commands |
