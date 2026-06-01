# How To Run

## Setup

Use Python 3.11 or newer.

```bash
cd labs/hot-key-demo
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
python -m hot_key_demo.demo
```

Without installing the package:

```bash
PYTHONPATH=src python -m hot_key_demo.demo
```

## Parameters

| Parameter | Default | Meaning |
| --- | ---: | --- |
| `--requests` | `1000` | Total read requests in the skewed traffic scenario |
| `--hot-fraction` | `0.62` | Share of read requests sent to the hot key |
| `--normal-keys` | `40` | Number of ordinary keys sharing the remaining reads |
| `--partitions` | `6` | Number of partitions or cache owners |
| `--capacity` | `260` | Capacity per partition or cache owner |
| `--hot-key` | `post:city-marathon` | Name of the hot read key |
| `--replicas` | `4` | Cache owners that hold replicas of the hot read key |
| `--origin-callers` | `80` | Concurrent callers after the hot cache key expires |
| `--origin-capacity` | `10` | Origin refresh capacity for the expired key |
| `--hot-writes` | `320` | Writes to a single hot counter before bucketing |
| `--write-buckets` | `8` | Number of buckets for hot counter writes |
| `--write-capacity` | `80` | Capacity per counter bucket |

## Example Changes

Increase read skew:

```bash
python -m hot_key_demo.demo --hot-fraction 0.75
```

Use too few read replicas:

```bash
python -m hot_key_demo.demo --replicas 2
```

Compare line `04` with the default output; with too few replicas, the hot cache
owner should remain overloaded.

Stress cache refresh:

```bash
python -m hot_key_demo.demo --origin-callers 200 --origin-capacity 15
```

Stress a hot counter:

```bash
python -m hot_key_demo.demo --hot-writes 900 --write-buckets 12
```

## Troubleshooting

- If `ModuleNotFoundError: No module named 'hot_key_demo'` appears, run from
  `labs/hot-key-demo` and use `PYTHONPATH=src`.
- If `pytest` is not installed, either install the test extra or use the
  standard-library unittest command.
- If the demo exits with a parameter error, check that fractions are between
  `0` and `1`, counts are positive, and replicas do not exceed partitions.
