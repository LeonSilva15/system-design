# What To Observe

## Cache Miss And Fill

The first read is a cache miss. The application reads the database, stores the
record in the cache, and returns the database value. Watch `db_reads` increase.

Question to ask: Can the source database absorb the miss rate if many keys miss
at the same time?

## Cache Hit

The second read is a cache hit. The returned value is the same version as the
first read, and `db_reads` does not increase.

Question to ask: Is this read repeated enough to justify cache operational
complexity?

## Stale Data Before TTL

The demo updates the database without invalidating the cache. The next read
still returns the old cached version because the TTL has not expired.

The `fallback_stale` field remains `no` in this step because the cache entry is
still fresh by TTL. The staleness is visible through the older record version.

Question to ask: Is this stale window safe for the product behavior, or should
the write path invalidate the affected key?

## TTL Refresh

After the clock advances beyond the TTL, the cached value expires. The next
read goes back to the database and refreshes the cache with the newer version.

Question to ask: Does the TTL match a user-facing freshness promise, or was it
chosen only because it felt reasonable?

## Targeted Invalidation

The demo then updates the database and invalidates the exact cache key. The
next read is a miss and returns the fresh source value before the old TTL would
have expired.

Question to ask: Can the write path reliably name every cache key that changed?

## Cache Outage Database Fallback

When the cache is unavailable, the application reads the database directly.
That keeps the read path working, but it also shifts traffic back to the source.

Question to ask: Should the system rate-limit fallback traffic to protect the
database during a cache outage?

## Database Outage Stale Fallback

When the cached value is expired and the database is unavailable, the demo can
serve the expired value if `stale_if_error` is enabled. This is useful for
public browsing data, but unsafe for permissions, payments, inventory commits,
or final booking decisions.

Question to ask: Is stale data better than no data for this exact read path?
