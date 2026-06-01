# Expected Output

The default command:

```bash
PYTHONPATH=src python -m hot_key_demo.demo
```

prints deterministic output similar to:

```text
config requests=1000 hot_fraction=0.62 partitions=6 capacity=260
01 skewed traffic: hot_key=post:city-marathon hot_key_requests=620 share=0.62 normal_requests=380 normal_keys=40
02 overloaded partition: node=partition-3 load=716 capacity=260 overloaded=yes loads=partition-0:48,partition-1:114,partition-2:38,partition-3:716,partition-4:19,partition-5:65
03 overloaded cache key owner: owner=cache-3 load=716 capacity=260 overloaded=yes loads=cache-0:48,cache-1:114,cache-2:38,cache-3:716,cache-4:19,cache-5:65
04 mitigation read replication: replicas=4 max_owner=cache-3 max_load=251 overloaded=no loads=cache-0:203,cache-1:114,cache-2:38,cache-3:251,cache-4:174,cache-5:220
05 mitigation request coalescing: callers=80 origin_without=80 overloaded_without=yes origin_with=1 protected_callers=79 overloaded_with=no
06 mitigation bucketed writes: single_counter_max=320 single_overloaded=yes buckets=8 bucketed_max=40 bucketed_overloaded=no
07 mitigation strategies: replicate hot reads, coalesce refreshes, cap origin fallback, serve stale when safe, bucket approximate writes
```

## How To Read It

- Line `01` shows traffic skew by key. One key receives 62% of reads.
- Lines `02` and `03` show that ordinary hash routing still sends the hot key to
  one overloaded partition and cache owner.
- Line `04` shows hot-read replication spreading the key across four cache
  owners so the maximum owner load falls below the toy threshold.
- Line `05` shows request coalescing reducing 80 concurrent refresh attempts to
  one origin request.
- Line `06` shows write bucketing reducing the maximum counter bucket from 320
  writes to 40 writes.

Different parameters will change the exact loads, but the important comparison
is baseline maximum load versus mitigated maximum load.
