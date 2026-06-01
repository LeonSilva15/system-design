# What To Observe

## Hash Sharding

Hash sharding spreads exact-key records across shards. The distribution is not
perfect on a tiny sample, but ordinary keys are less likely to concentrate than
a low-cardinality key.

Question to ask: Is the main request an exact-key lookup, or does it need a
group of related records?

## Cross-Shard Tenant Query

The demo hashes by `record_id`, then asks for all records for one tenant. Since
tenant ID is not the routing key, the query touches every hash shard.

Question to ask: Would tenant-scoped pages, exports, deletes, or support tools
become scatter-gather operations?

## Resharding

Changing a modulo hash shard count from 3 to 4 moves many records in the toy
model. Production systems often use an indirection layer to reduce or control
movement, but movement still needs copy, verify, cutover, and rollback.

Question to ask: How would the system route old and new writes while records
move?

## Range Hot Partition

The range-sharded example puts current-day writes into the `current` shard.
That makes time-window routing simple, but the newest range becomes hot.

Question to ask: Is the current range likely to receive most writes during
normal traffic or launches?

## Cross-Shard Reports

The range report touches every shard in this simplified model. A production
range router could prune shards for narrower ranges, but broad reports still
need fanout, merge, retry, and partial-failure handling.

Question to ask: Should reporting move to a derived store instead of querying
operational shards?

## Range Pruning

The narrow range query touches only the `recent` shard. This is the routing
upside of range sharding when the query range aligns with shard boundaries.

Question to ask: Are your most common ranges narrow enough to benefit from this
pruning?
