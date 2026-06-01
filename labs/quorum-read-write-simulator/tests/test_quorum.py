from __future__ import annotations

import unittest

from quorum_read_write_simulator import Cluster, QuorumUnavailable
from quorum_read_write_simulator.demo import parse_latencies, run_demo


class QuorumTests(unittest.TestCase):
    def test_write_quorum_updates_fastest_acknowledging_replicas(self) -> None:
        cluster = Cluster.with_latencies([10, 30, 70])

        result = cluster.write("approved", write_quorum=2)

        self.assertEqual(result.operation, "write")
        self.assertEqual(result.successful, 2)
        self.assertEqual(result.latency_ms, 30)
        self.assertEqual(result.version, 1)
        self.assertEqual(cluster.replicas[0].value, "approved")
        self.assertEqual(cluster.replicas[1].value, "approved")
        self.assertEqual(cluster.replicas[2].version, 0)

    def test_read_quorum_returns_highest_version_seen(self) -> None:
        cluster = Cluster.with_latencies([10, 30, 70])
        cluster.seed_replica("r1", "old", 1)
        cluster.seed_replica("r2", "new", 2)
        cluster.seed_replica("r3", "new", 2)

        result = cluster.read(read_quorum=2)

        self.assertEqual(result.value, "new")
        self.assertEqual(result.version, 2)
        self.assertFalse(result.stale)

    def test_small_read_quorum_can_return_stale_value(self) -> None:
        cluster = Cluster.with_latencies([10, 30, 70])
        cluster.seed_replica("r1", "old", 1)
        cluster.seed_replica("r2", "new", 2)
        cluster.seed_replica("r3", "new", 2)

        result = cluster.read(read_quorum=1)

        self.assertEqual(result.value, "old")
        self.assertEqual(result.version, 1)
        self.assertTrue(result.stale)

    def test_unavailable_replicas_can_break_quorum(self) -> None:
        cluster = Cluster.with_latencies([10, 30, 70])
        cluster.set_unavailable({"r1", "r2"})

        with self.assertRaises(QuorumUnavailable):
            cluster.read(read_quorum=2)

    def test_unavailable_replicas_can_break_write_quorum(self) -> None:
        cluster = Cluster.with_latencies([10, 30, 70])
        cluster.set_unavailable({"r1", "r2"})

        with self.assertRaises(QuorumUnavailable):
            cluster.write("approved", write_quorum=2)

    def test_latency_tracks_slowest_member_of_fastest_quorum(self) -> None:
        cluster = Cluster.with_latencies([10, 30, 70])

        read_one = cluster.read(read_quorum=1)
        read_three = cluster.read(read_quorum=3)

        self.assertEqual(read_one.latency_ms, 10)
        self.assertEqual(read_three.latency_ms, 70)

    def test_read_repair_updates_stale_responders(self) -> None:
        cluster = Cluster.with_latencies([10, 30, 70])
        cluster.seed_replica("r1", "old", 1)
        cluster.seed_replica("r2", "new", 2)
        cluster.seed_replica("r3", "new", 2)

        result = cluster.read(read_quorum=2)
        repaired = cluster.repair(result.responses)

        self.assertEqual(repaired, ["r1"])
        self.assertEqual(cluster.replicas[0].value, "new")
        self.assertEqual(cluster.replicas[0].version, 2)

    def test_demo_smoke_output(self) -> None:
        lines = run_demo([])

        self.assertTrue(any("write quorum" in line for line in lines))
        self.assertTrue(any("read quorum" in line for line in lines))
        self.assertTrue(any("unavailable" in line for line in lines))
        self.assertTrue(any("stale=yes" in line for line in lines))
        self.assertTrue(any("latency_ms=" in line for line in lines))
        self.assertTrue(any("read repair only updates" in line for line in lines))

    def test_parse_latencies_validates_count(self) -> None:
        with self.assertRaises(SystemExit):
            parse_latencies("10,20", replicas=3)

    def test_demo_rejects_too_few_replicas(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--replicas", "2", "--latencies", "10,20"])


if __name__ == "__main__":
    unittest.main()
