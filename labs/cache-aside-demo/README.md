# Cache-Aside Demo

This lab demonstrates cache-aside behavior with a small deterministic Python
model. It shows how a read path moves through cache miss, cache hit, TTL expiry,
stale data, targeted invalidation, cache outage fallback to the database, and
optional stale fallback when the database is down.

The example is a public class catalog. The database is the source of truth for
available seats, and the cache accelerates repeated reads of the same class
detail page.

## Goal

Use this lab to learn:

- how cache-aside fills the cache on demand after a miss;
- why cached reads can return stale data until TTL expiry or invalidation;
- how targeted invalidation gives fresher reads when the write path knows the
  affected key;
- why cache outages often fall back to the database and can increase source
  load;
- when serving stale data during a database outage is safer than failing and
  when it is not.

## Quick Start

Run commands from this lab directory. Use Python 3.11 or newer.

```bash
cd labs/cache-aside-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install ".[test]"
python -m pytest
python -m cache_aside_demo.demo
```

You can also run the tests with standard library discovery after installation:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Try changing the cache policy:

```bash
python -m cache_aside_demo.demo --ttl 2
python -m cache_aside_demo.demo --ttl 10 --updated-seats 4
python -m cache_aside_demo.demo --no-stale-if-error
```

## Files

- [design.md](design.md) explains the simplified model and assumptions.
- [how-to-run.md](how-to-run.md) lists setup, commands, parameters, and
  troubleshooting.
- [expected-output.md](expected-output.md) shows representative default output.
- [what-to-observe.md](what-to-observe.md) explains what to change and what to
  watch.
- [tradeoffs.md](tradeoffs.md) connects cache-aside behavior to design
  trade-offs.

## Related Cookbook Pages

- [Caching strategies](../../docs/scalability/caching-strategies.md)
- [Cache component](../../docs/components/cache.md)
- [Capacity estimation](../../docs/scalability/capacity-estimation.md)
- [Metrics](../../docs/operations/metrics.md)

Return to the [labs README](../README.md).
