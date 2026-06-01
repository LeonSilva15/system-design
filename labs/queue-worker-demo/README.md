# Queue Worker Demo

This lab demonstrates asynchronous queue worker behavior with a deterministic
Python model. It shows enqueue, worker processing, retry, failure, visibility
timeout redelivery, and basic observability signals.

The example is a community services platform that queues background work for
thumbnails, notification emails, webhooks, and report generation. The point is
not the specific job type; the point is what happens when work is accepted now
and completed later.

## Goal

Use this lab to learn:

- how a producer enqueues durable work for a worker to claim later;
- how workers acknowledge success separately from claiming work;
- why retryable failures need delay, attempt counts, and a maximum;
- how visibility timeout redelivers work after a worker crash;
- which queue metrics make backlog, stuck work, retries, and failures visible.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/queue-worker-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m queue_worker_demo.demo
```

You can also run the tests with the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing the worker policy:

```bash
python -m queue_worker_demo.demo --visibility-timeout 2
python -m queue_worker_demo.demo --retry-delay 1 --max-attempts 2
python -m queue_worker_demo.demo --visibility-timeout 8 --retry-delay 4
```

## Files

- [design.md](design.md) explains the simplified queue model and assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects queue worker behavior to design
  trade-offs.

## Related Cookbook Pages

- [Queues](../../docs/communication/queues.md)
- [Queue component](../../docs/components/queue.md)
- [Background workers](../../docs/components/background-workers.md)
- [Retries and backoff](../../docs/communication/retries-and-backoff.md)
- [Metrics](../../docs/operations/metrics.md)

Return to the [labs README](../README.md).
