# Retry And Idempotency Demo

This lab demonstrates how retries can duplicate business work when an operation
does not have an idempotency boundary. It compares unsafe duplicate request
handling with a safer flow that stores an idempotency key before side effects
run.

The example is a workshop reservation service. A mobile client may retry after
losing a response, and an event consumer may receive the same reservation event
more than once.

## Goal

Use this lab to learn:

- how duplicate requests can create duplicate reservations;
- why retries must reuse the same idempotency key;
- how duplicate event delivery can repeat side effects;
- how a small dedupe record makes repeated work boring and observable.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/retry-idempotency-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m retry_idempotency_demo.demo
```

You can also run the tests without third-party packages:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing the duplicate pressure:

```bash
python -m retry_idempotency_demo.demo --attempts 2
python -m retry_idempotency_demo.demo --attempts 4 --event-deliveries 3
python -m retry_idempotency_demo.demo --mode safe --show-conflict
```

## Files

- [design.md](design.md) explains the model, entities, and assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects retry and idempotency behavior to
  system design trade-offs.

## Related Cookbook Pages

- [Idempotency](../../docs/communication/idempotency.md)
- [Retries and backoff](../../docs/communication/retries-and-backoff.md)
- [Reliability retries](../../docs/reliability/retries.md)
- [Payment workflow walkthrough](../../docs/walkthroughs/payment-workflow.md)

Return to the [labs README](../README.md).
