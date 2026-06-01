from __future__ import annotations

import unittest

from hot_key_demo.demo import run_demo
from hot_key_demo.model import (
    analyze_partition_load,
    bucket_hot_writes,
    make_skewed_traffic,
    replicated_hot_key_load,
    simulate_refresh_storm,
)


class HotKeyDemoTests(unittest.TestCase):
    def test_skewed_traffic_creates_large_hot_key_share(self) -> None:
        events = make_skewed_traffic(
            total_requests=100,
            hot_key="post:launch",
            hot_fraction=0.70,
            normal_key_count=10,
        )

        report = analyze_partition_load(
            events,
            node_count=4,
            capacity_per_node=40,
        )

        self.assertEqual(report.hot_key, "post:launch")
        self.assertEqual(report.hot_key_count, 70)
        self.assertAlmostEqual(report.hot_key_share, 0.70)

    def test_hash_routing_concentrates_hot_key_on_one_partition(self) -> None:
        events = make_skewed_traffic(
            total_requests=100,
            hot_key="post:launch",
            hot_fraction=0.70,
            normal_key_count=10,
        )

        report = analyze_partition_load(
            events,
            node_count=4,
            capacity_per_node=40,
        )

        self.assertTrue(report.overloaded)
        self.assertGreaterEqual(report.hottest_node_load, report.hot_key_count)

    def test_replicating_hot_read_key_lowers_max_cache_owner_load(self) -> None:
        events = make_skewed_traffic(
            total_requests=1000,
            hot_key="post:launch",
            hot_fraction=0.60,
            normal_key_count=40,
        )
        cache_report = analyze_partition_load(
            events,
            node_count=6,
            capacity_per_node=260,
            node_prefix="cache",
        )

        replicated = replicated_hot_key_load(
            cache_report.key_counts,
            hot_key=cache_report.hot_key,
            node_count=6,
            replica_count=4,
            capacity_per_node=260,
            node_prefix="cache",
        )

        self.assertTrue(cache_report.overloaded)
        self.assertLess(replicated.hottest_node_load, cache_report.hottest_node_load)
        self.assertFalse(replicated.overloaded)

    def test_refresh_coalescing_reduces_origin_requests(self) -> None:
        without = simulate_refresh_storm(
            callers=80,
            origin_capacity=10,
            coalescing=False,
        )
        with_coalescing = simulate_refresh_storm(
            callers=80,
            origin_capacity=10,
            coalescing=True,
            fallback_limit=10,
        )

        self.assertTrue(without.overloaded)
        self.assertEqual(without.origin_requests, 80)
        self.assertFalse(with_coalescing.overloaded)
        self.assertEqual(with_coalescing.origin_requests, 1)
        self.assertEqual(with_coalescing.protected_callers, 79)

    def test_bucketed_writes_distribute_hot_counter_load(self) -> None:
        unbucketed = bucket_hot_writes(
            total_writes=320,
            bucket_count=1,
            capacity_per_bucket=80,
        )
        bucketed = bucket_hot_writes(
            total_writes=320,
            bucket_count=8,
            capacity_per_bucket=80,
        )

        self.assertTrue(unbucketed.overloaded)
        self.assertEqual(unbucketed.max_bucket_load, 320)
        self.assertFalse(bucketed.overloaded)
        self.assertEqual(bucketed.max_bucket_load, 40)

    def test_demo_smoke_output(self) -> None:
        lines = run_demo([])
        output = "\n".join(lines)

        self.assertTrue(any("skewed traffic" in line for line in lines))
        self.assertTrue(any("overloaded partition" in line for line in lines))
        self.assertTrue(any("overloaded cache key owner" in line for line in lines))
        self.assertTrue(any("mitigation read replication" in line for line in lines))
        self.assertTrue(any("mitigation request coalescing" in line for line in lines))
        self.assertTrue(any("mitigation bucketed writes" in line for line in lines))
        self.assertTrue(any("mitigation strategies" in line for line in lines))
        self.assertIn("02 overloaded partition:", output)
        self.assertIn("overloaded=yes", lines[2])
        self.assertIn("03 overloaded cache key owner:", output)
        self.assertIn("overloaded=yes", lines[3])
        self.assertIn("04 mitigation read replication:", output)
        self.assertIn("overloaded=no", lines[4])
        self.assertIn("05 mitigation request coalescing:", output)
        self.assertIn("overloaded_without=yes", lines[5])
        self.assertIn("overloaded_with=no", lines[5])

    def test_demo_rejects_invalid_hot_fraction(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--hot-fraction", "1.2"])

    def test_demo_rejects_replica_count_above_partition_count(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--partitions", "3", "--replicas", "4"])


if __name__ == "__main__":
    unittest.main()
