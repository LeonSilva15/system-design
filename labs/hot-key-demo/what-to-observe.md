# What To Observe

## Skewed Traffic

Start with the default output and compare the hot key's request share with the
per-partition load. The hot key is only one key, but it dominates the hottest
partition.

Question to ask: Are dashboards grouped by node hiding the fact that one key is
causing most of the pressure?

## Overloaded Partition

Line `02` shows the partition that receives the hot key. The other partitions
may be comfortably below capacity while one partition is far above it.

Question to ask: Would adding more application instances help if all reads for
the hot key still route to the same partition?

## Overloaded Cache Key Owner

Line `03` shows the same problem as a cache-owner issue. A high average cache
hit rate would not protect the cache owner responsible for the hot key if every
caller still lands there.

Question to ask: Do cache metrics expose top keys and owner load, or only fleet
averages?

## Read Replication

Line `04` spreads the hot read key across several cache owners. Increase or
decrease `--replicas` and watch the maximum owner load.

Question to ask: Is the data safe to replicate, or does the key need tenant,
user, role, locale, or permission state embedded in it?

## Request Coalescing

Line `05` models an expired hot cache key. Without coalescing, every caller
refreshes from the origin. With coalescing, one origin request refreshes the key
while the other callers wait or receive a safe stale value.

Question to ask: What response should callers receive while the refresh is in
progress: wait, stale data, partial data, or a controlled rejection?

## Bucketed Writes

Line `06` splits a hot counter into several buckets. That improves write
throughput but means reads must aggregate buckets or accept a delayed snapshot.

Question to ask: Is an approximate or slightly stale counter acceptable for this
product behavior?

## Capacity Sensitivity

Lower `--capacity` or raise `--hot-fraction` to make the system fail harder.
Then raise `--replicas`, add write buckets, or reduce origin callers to see
which mitigation addresses which bottleneck.

Question to ask: Which metric proves the mitigation worked: top key share, max
owner load, origin fallback requests, write conflicts, queue age, or
user-visible latency?
