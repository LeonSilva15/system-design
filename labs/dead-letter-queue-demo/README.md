# Dead-Letter Queue Demo

This lab demonstrates dead-letter queue behavior with a deterministic Python
model. The example is a community tool library that sends pickup reminders
after reservations are approved.

The lab shows a normal job, a poison message that fails fast, a retryable job
that reaches retry exhaustion, DLQ inspection, alerting, safe replay, and a
blocked unsafe replay.

## Goal

Use this lab to learn:

- how poison messages differ from retryable failures;
- why retry exhaustion should move work to an explicit repair state;
- what safe inspection context a dead-letter record needs;
- how alerting can watch open count and oldest age;
- why replay needs idempotency and current-state checks;
- why some dead letters should be corrected, cancelled, or skipped instead of
  replayed.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/dead-letter-queue-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m dead_letter_queue_demo.demo
```

You can also run the tests with the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing the policy:

```bash
python -m dead_letter_queue_demo.demo --max-attempts 2
python -m dead_letter_queue_demo.demo --retry-delay 5
python -m dead_letter_queue_demo.demo --alert-age 30 --alert-count 3
```

## Files

- [design.md](design.md) explains the simplified DLQ model and assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects DLQ behavior to design trade-offs.

## Related Cookbook Pages

- [Dead-letter queues](../../docs/communication/dead-letter-queues.md)
- [Queues](../../docs/communication/queues.md)
- [Queue component](../../docs/components/queue.md)
- [Background workers](../../docs/components/background-workers.md)
- [Idempotency](../../docs/communication/idempotency.md)
- [Alerting](../../docs/operations/alerting.md)

Return to the [labs README](../README.md).
