# Cache-Aside Trade-Offs

## What Cache-Aside Buys

Cache-aside is simple to introduce because the application owns the cache key,
miss behavior, TTL, and fallback path. It can reduce repeated database reads
without changing the database write path first.

This simplicity is why cache-aside is often a good first caching pattern for
read-heavy public or stale-tolerant data.

## What It Costs

Cache-aside makes freshness an application decision:

- cached values can be stale until TTL expiry;
- missed invalidation can hide source changes;
- cache outages can push load back to the source database;
- synchronized TTL expiry can create miss storms;
- hot keys can overload a cache node or source fallback path;
- stale fallback can be helpful for browsing and dangerous for correctness.

## When It Fits

Use cache-aside when:

- reads repeat often;
- a bounded stale window is acceptable;
- misses can safely read from the source database;
- the application can define stable keys;
- the team can measure hit rate, miss rate, stale age, and fallback volume.

## When To Avoid It

Avoid cache-aside for reads that must always be fresh, authorization decisions
that could expose private data, payment outcomes, final inventory commits, or
any flow where stale data creates an unsafe side effect.

For the class catalog example, cache-aside is reasonable for browsing class
details. It is not enough for final seat reservation; that write should recheck
the source of truth.

## Production Differences

A production design would usually add:

- request coalescing so one miss fills a hot key;
- TTL jitter to avoid synchronized expiry;
- per-key and global fallback limits;
- metrics for hit rate, miss rate, stale responses, source fallback, and hot
  keys;
- cache entry versioning when stale data must be detected;
- targeted invalidation from source writes;
- explicit policy for cache write failure after a successful source read;
- runbooks for cache outage and source overload.

The lab keeps those details visible as trade-offs instead of hiding them inside
a cache client.
