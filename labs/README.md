# Labs

Runnable labs live here. Labs are separate from documentation pages so examples
can include code, tests, demo scripts, and expected output without mixing them
with the MkDocs content tree.

Labs should be small, runnable, and focused on observable system behavior. A lab
is ready when a learner can run it locally, change one or two inputs, observe
the result, and connect that behavior back to an architecture decision.

## Purpose

Use labs to make system design behavior visible:

- rate limiting under bursts;
- cache hits, misses, staleness, and invalidation;
- queue retries, retry exhaustion, and dead-letter handling;
- idempotency under duplicate requests or duplicate events;
- replica lag, stale reads, quorum behavior, sharding, and hot keys;
- batching, backpressure, retention, and compaction trade-offs.

Labs are not production frameworks. Prefer a clear toy implementation over a
large service that hides the behavior being taught.

## Current Labs

| Lab | Focus |
| --- | --- |
| [Token bucket rate limiter](rate-limiter/) | burst capacity, refill rate, retry hints, and limiter behavior tests |
| [Cache-aside demo](cache-aside-demo/) | cache miss, hit, TTL, stale data, invalidation, database fallback, and failure-mode tests |
| [Retry and idempotency demo](retry-idempotency-demo/) | duplicate requests, idempotency keys, duplicate events, and guarded side effects |

## Runtime Expectations

Default runtime:

- Python 3.11 or newer.
- `pytest` for automated tests.
- Standard library first; add dependencies only when the lab needs them to
  demonstrate the concept.
- No required network access, cloud account, database server, broker, or
  container runtime unless the ticket explicitly requires it.
- Deterministic tests. Use fixed seeds or controlled clocks when randomness or
  time affects the result.
- Small data sets that run quickly on a laptop.
- Clear command-line parameters for the variables the learner is expected to
  change.

Every lab should run from its own directory:

```bash
cd labs/<lab-slug>
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m <lab_package>.demo
```

If a lab has no package yet, it may start with a single script, but it should
still document the exact run command and provide either tests or a demo script.

## Folder Structure

Use this structure unless the ticket gives a stronger reason to differ:

```text
labs/<lab-slug>/
  README.md
  design.md
  how-to-run.md
  expected-output.md
  what-to-observe.md
  tradeoffs.md
  pyproject.toml
  src/
    <lab_package>/
      __init__.py
      demo.py
      ...
  tests/
    test_<behavior>.py
```

Required files:

| File | Purpose |
| --- | --- |
| `README.md` | Learner-facing overview, goal, quick start, and links to lab docs |
| `design.md` | Problem, model, assumptions, core behavior, and why the lab is simplified |
| `how-to-run.md` | Setup, commands, parameters, and troubleshooting |
| `expected-output.md` | Representative output for the default scenario |
| `what-to-observe.md` | Variables to change, signals to watch, and questions to answer |
| `tradeoffs.md` | What the lab teaches, what it omits, and how production systems differ |
| `pyproject.toml` | Local package metadata, Python version, and test dependencies |
| `src/` | Implementation code for the lab |
| `tests/` | Pytest tests for behavior and edge cases |

## Harness Expectations

Each lab should expose:

- a default demo command that prints observable behavior;
- pytest tests for the core behavior or a documented reason tests are not
  useful for that specific lab;
- parameters for the important design variables, such as rate limit, queue
  retry count, TTL, replica lag, shard count, or hot-key distribution;
- expected output for the default scenario;
- a short "what to observe" guide that tells the learner what changed and why.

Tests should check behavior, not implementation details. For example, a token
bucket lab should test refill and burst behavior; it should not depend on a
specific private helper name.

## Documentation Expectations

Every lab should answer:

- What behavior is this lab demonstrating?
- Which requirement or failure mode makes the behavior matter?
- Which variable should the learner change first?
- What output proves the behavior happened?
- What trade-off would change in a production design?
- Which cookbook pages explain the related design decision?

Keep lab prose practical. Do not copy external exercises, diagrams, examples,
or teaching sequences.

## Template

Use [`templates/lab-template/`](../templates/lab-template/) as the starting
point for new labs. Copy the folder into `labs/<lab-slug>/`, rename the package,
replace placeholder prose, and keep the standard commands working.
