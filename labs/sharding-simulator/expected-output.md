# Expected Output

The default command:

```bash
python -m sharding_simulator.demo
```

prints output similar to:

```text
config records=18 shards=3 new_shards=4 hot_writes=12
01 hash sharding loads: h0:5,h1:6,h2:7
02 hash hottest shard: shard=h2 count=7 share=0.39
03 direct lookup: query=record_id=request-000 shards=1 note=direct shard lookup
04 tenant query on record-id hash: records=5 shards=3 note=cross-shard fanout
05 reshard hash 3->4: moved=11/18 moved_percent=61.1
   note reshard estimate uses simple modulo hashing
06 range sharding loads: current:12,old:1,recent:1
07 range hot partition: shard=current count=12 share=0.86
08 cross-shard range report: records=14 shards=3 note=range query may fan out unless range routing can prune shards
09 narrow range query: records=1 shards=1 note=range router pruned shards
```

Exact load counts are deterministic for the default inputs. The important
signals are shard load balance, hottest shard share, shards touched per query,
and moved records during resharding. The reshard estimate intentionally uses
simple modulo hashing so movement pain is easy to see; production systems often
use placement maps or consistent-hashing-style indirection to control movement.
