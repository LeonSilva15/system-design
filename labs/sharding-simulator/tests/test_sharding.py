from __future__ import annotations

import unittest

from sharding_simulator import HashRouter, RangeRouter, Record, ShardedStore
from sharding_simulator.demo import make_records, run_demo
from sharding_simulator.model import reshard_hash


class ShardingSimulatorTests(unittest.TestCase):
    def test_hash_router_is_deterministic(self) -> None:
        router = HashRouter(3)
        record = Record("request-001", "clinic", 10, "task")

        self.assertEqual(router.route(record), router.route(record))

    def test_hash_exact_key_lookup_touches_one_shard(self) -> None:
        records = make_records(10)
        store = ShardedStore(HashRouter(3, key_field="record_id"))
        store.insert_many(records)

        result = store.query_by_record_id(records[0].record_id)

        self.assertEqual(len(result.shards_touched), 1)
        self.assertEqual(result.records, (records[0],))
        self.assertEqual(result.note, "direct shard lookup")

    def test_tenant_query_crosses_shards_when_hashing_by_record_id(self) -> None:
        records = make_records(12)
        store = ShardedStore(HashRouter(3, key_field="record_id"))
        store.insert_many(records)

        result = store.query_by_tenant("clinic")

        self.assertEqual(len(result.shards_touched), 3)
        self.assertEqual(result.note, "cross-shard fanout")
        self.assertGreater(len(result.records), 0)

    def test_tenant_hash_keeps_tenant_query_local(self) -> None:
        records = make_records(12)
        store = ShardedStore(HashRouter(3, key_field="tenant_id"))
        store.insert_many(records)

        result = store.query_by_tenant("clinic")

        self.assertEqual(len(result.shards_touched), 1)
        self.assertEqual(result.note, "tenant-local lookup")

    def test_range_router_routes_by_day(self) -> None:
        router = RangeRouter([("old", 1, 30), ("current", 31, 120)])

        self.assertEqual(router.route_day(10), "old")
        self.assertEqual(router.route_day(90), "current")

    def test_range_router_rejects_overlapping_ranges(self) -> None:
        with self.assertRaises(ValueError):
            RangeRouter([("a", 1, 10), ("b", 10, 20)])

    def test_range_router_rejects_duplicate_names(self) -> None:
        with self.assertRaises(ValueError):
            RangeRouter([("a", 1, 10), ("a", 11, 20)])

    def test_range_sharding_can_create_hot_current_partition(self) -> None:
        store = ShardedStore(RangeRouter([("old", 1, 30), ("current", 31, 120)]))
        records = [
            Record(f"current-{i}", "clinic", 90, "task")
            for i in range(10)
        ]
        store.insert_many(records)

        shard, count, share = store.hot_partition()

        self.assertEqual(shard, "current")
        self.assertEqual(count, 10)
        self.assertEqual(share, 1.0)

    def test_range_query_can_prune_shards(self) -> None:
        store = ShardedStore(
            RangeRouter([("old", 1, 30), ("recent", 31, 60), ("current", 61, 120)])
        )
        store.insert_many(
            [
                Record("old-1", "library", 10, "old"),
                Record("recent-1", "garden", 45, "recent"),
                Record("current-1", "clinic", 90, "current"),
            ]
        )

        result = store.query_day_range(31, 60)

        self.assertEqual(result.shards_touched, ("recent",))
        self.assertEqual(len(result.records), 1)
        self.assertEqual(result.note, "range router pruned shards")

    def test_resharding_moves_some_records(self) -> None:
        records = make_records(20)

        plan = reshard_hash(records, 3, 4)

        self.assertEqual(plan.total_records, 20)
        self.assertGreater(plan.moved_records, 0)
        self.assertLessEqual(plan.moved_records, 20)

    def test_demo_smoke_output(self) -> None:
        lines = run_demo([])

        self.assertTrue(any("hash sharding loads" in line for line in lines))
        self.assertTrue(any("tenant query on record-id hash" in line for line in lines))
        self.assertTrue(any("reshard hash" in line for line in lines))
        self.assertTrue(any("range hot partition" in line for line in lines))
        self.assertTrue(any("cross-shard range report" in line for line in lines))
        self.assertTrue(any("narrow range query" in line for line in lines))

    def test_demo_rejects_invalid_record_count(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--records", "0"])

    def test_demo_rejects_too_few_hot_writes(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--hot-writes", "1"])


if __name__ == "__main__":
    unittest.main()
