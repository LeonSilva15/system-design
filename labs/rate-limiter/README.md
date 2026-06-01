# Token Bucket Rate Limiter Lab

This lab demonstrates token bucket rate limiting with a small deterministic
Python implementation. It shows how burst size and refill rate affect allowed
and limited requests.

The example is a workshop reservation API that wants to allow a short burst of
legitimate clicks while protecting the reservation write path from sustained
traffic.

## Goal

Use this lab to learn:

- how a token bucket separates burst capacity from sustained rate;
- why an empty bucket returns a retry hint instead of guessing;
- how burst size and refill rate change user-visible behavior;
- why tests should verify behavior, not private implementation details.

## Quick Start

Use Python 3.11 or newer. If `python` points to an older interpreter, use
`python3.11` in the commands below.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m rate_limiter_lab.demo
```

Try changing the burst size and refill rate:

```bash
python -m rate_limiter_lab.demo --capacity 3 --refill-rate 0.5
python -m rate_limiter_lab.demo --capacity 10 --refill-rate 5 --spacing 0.05
python -m rate_limiter_lab.demo --capacity 4 --refill-rate 1 --start-empty
```

## Files

- [design.md](design.md) explains the simplified model and assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects token bucket behavior to design
  trade-offs.

## Related Cookbook Pages

- [Rate limiting](../../docs/scalability/rate-limiting.md)
- [Rate limiting and abuse resistance](../../docs/security/rate-limiting-and-abuse.md)
- [Rate limiter walkthrough](../../docs/walkthroughs/rate-limiter.md)

Return to the [labs README](../README.md).
