# How To Run The Cache-Aside Demo

## Setup

Use Python 3.11 or newer.

```bash
cd labs/cache-aside-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
```

## Run Tests

```bash
python -m pytest
```

The tests cover cache miss and hit behavior, TTL refresh, invalidation,
database fallback when the cache is unavailable, and stale fallback when the
database is unavailable.

If `pytest` is not installed, run the same behavior tests with the standard
library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Run The Demo

```bash
python -m cache_aside_demo.demo
```

Useful parameters:

| Parameter | Default | What It Changes |
| --- | --- | --- |
| `--ttl` | `5.0` | How long a cached value remains fresh |
| `--initial-seats` | `12` | The first source value |
| `--updated-seats` | `2` | The source value written without invalidation |
| `--final-seats` | `1` | The source value written before invalidation |
| `--no-stale-if-error` | off | Fails instead of serving an expired cached value when the database is down |

Examples:

```bash
python -m cache_aside_demo.demo --ttl 2
python -m cache_aside_demo.demo --ttl 10 --updated-seats 4
python -m cache_aside_demo.demo --no-stale-if-error
```

## Troubleshooting

- If imports fail, confirm that commands are run from `labs/cache-aside-demo`
  after installing the package.
- If `pytest` is missing, rerun `python -m pip install ".[test]"`.
- If `python` points to an older interpreter, use `python3.11` or newer in the
  commands.
