# How To Run

Run commands from this lab directory.

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
python -m lab_template.demo
```

## Parameters

Replace this table with the variables the learner should change.

| Parameter | Default | What It Changes |
| --- | --- | --- |
| `--example` | `baseline` | `[Observable behavior]` |

## Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError` | Package was not installed in the active environment | Run `python -m pip install ".[test]"` |
| `pytest` is missing | Test dependency was not installed | Re-run setup command |
