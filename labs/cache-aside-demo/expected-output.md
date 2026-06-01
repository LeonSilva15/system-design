# Expected Output

The default command:

```bash
python -m cache_aside_demo.demo
```

prints output similar to:

```text
config ttl=5.0s initial_seats=12 updated_seats=2 final_seats=1
01 miss fills cache: t=0.0s source=database_miss_fill cache=miss value=seats:12 version:1 fallback_stale=no db_reads=1 note=cache miss read from source and filled cache
02 hit reuses cache: t=1.0s source=cache cache=hit value=seats:12 version:1 fallback_stale=no db_reads=1 note=fresh cached value reused
03 source changes without invalidation: database=seats:2 version:2
04 stale until ttl or invalidation: t=2.0s source=cache cache=hit value=seats:12 version:1 fallback_stale=no db_reads=1 note=fresh cached value reused
05 ttl expiry refreshes: t=7.0s source=database_refresh_after_ttl cache=expired value=seats:2 version:2 fallback_stale=no db_reads=2 note=expired cache entry refreshed from source
06 source changes with invalidation: database=seats:1 version:3 invalidated=True
07 invalidation forces miss: t=8.0s source=database_miss_fill cache=miss value=seats:1 version:3 fallback_stale=no db_reads=3 note=cache miss read from source and filled cache
08 cache outage uses database: t=9.0s source=database_cache_unavailable cache=cache_unavailable value=seats:1 version:3 fallback_stale=no db_reads=4 note=cache failed open to the source database
09 database outage uses stale: t=14.0s source=stale_cache_database_unavailable cache=expired value=seats:1 version:3 fallback_stale=yes db_reads=4 note=expired value served because the source was down
summary cache_hits=2 cache_misses=2 cache_expired=2 cache_writes=3 invalidations=1 db_reads=4
```

The exact numbers change when you pass different TTL or seat-count parameters.
The important signals are the `source`, `cache`, `version`, `fallback_stale`,
and `db_reads` fields. Step 04 is stale compared with the database because the
version is older than the source version. The `fallback_stale` field is only
`yes` when the lab intentionally serves an expired cache entry because the
database is unavailable.
