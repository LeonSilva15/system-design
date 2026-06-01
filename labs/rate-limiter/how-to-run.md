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

## Run Demo

```bash
python -m rate_limiter_lab.demo
```

## Parameters

The listed flags match the demo CLI.

| Parameter | Default | What It Changes |
| --- | --- | --- |
| `--capacity` | `5` | Burst size, or maximum tokens the bucket can hold |
| `--refill-rate` | `1.0` | Sustained refill rate in tokens per second |
| `--requests` | `10` | Number of simulated requests |
| `--spacing` | `0.2` | Seconds between simulated requests |
| `--cost` | `1.0` | Tokens spent by each request |
| `--start-empty` | `false` | Starts with zero tokens instead of a full bucket |

## Example Commands

Small burst and slow refill:

```bash
python -m rate_limiter_lab.demo --capacity 3 --refill-rate 0.5
```

Large burst and fast refill:

```bash
python -m rate_limiter_lab.demo --capacity 10 --refill-rate 5 --spacing 0.05
```

Empty bucket recovery:

```bash
python -m rate_limiter_lab.demo --capacity 4 --refill-rate 1 --start-empty
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError` | Package was not installed in the active environment | Run `python -m pip install ".[test]"` |
| `pytest` is missing | Test dependency was not installed | Re-run setup command |
| `python` uses an older version | Local shell points to an older interpreter | Use `python3.11` for setup and commands |
