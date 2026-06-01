from __future__ import annotations

import unittest

from replication_lag_simulator import LeaderFollowerStore, ManualClock
from replication_lag_simulator.demo import run_demo


KEY = "reservation:community-room"


class ReplicationLagTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = ManualClock()
        self.store = LeaderFollowerStore(self.clock, replication_delay=5.0)

    def test_leader_write_is_immediately_visible_on_leader(self) -> None:
        record = self.store.write(KEY, "approved")

        result = self.store.read_leader(KEY)

        self.assertEqual(result.source, "leader")
        self.assertEqual(result.value, "approved")
        self.assertEqual(result.version, record.version)
        self.assertFalse(result.stale)

    def test_follower_lags_after_leader_write(self) -> None:
        record = self.store.write(KEY, "approved")

        result = self.store.read_follower(KEY, min_version=record.version)
        status = self.store.status(KEY)

        self.assertIsNone(result.value)
        self.assertTrue(result.stale)
        self.assertFalse(result.read_your_writes_ok)
        self.assertEqual(status.versions_behind, 1)
        self.assertEqual(status.pending_events, 1)

    def test_follower_catches_up_after_lag_window(self) -> None:
        self.store.write(KEY, "approved")

        self.clock.advance(5.0)
        result = self.store.read_follower(KEY)
        status = self.store.status(KEY)

        self.assertEqual(result.value, "approved")
        self.assertFalse(result.stale)
        self.assertTrue(result.read_your_writes_ok)
        self.assertEqual(status.versions_behind, 0)
        self.assertEqual(status.pending_events, 0)

    def test_second_write_makes_follower_stale_after_first_applies(self) -> None:
        self.store.write(KEY, "approved")
        self.clock.advance(2.5)
        second = self.store.write(KEY, "approved with projector")
        self.clock.advance(2.5)

        result = self.store.read_follower(KEY, min_version=second.version)

        self.assertEqual(result.value, "approved")
        self.assertEqual(result.version, 1)
        self.assertEqual(result.leader_version, 2)
        self.assertTrue(result.stale)
        self.assertFalse(result.read_your_writes_ok)

    def test_min_version_read_falls_back_to_leader_when_follower_is_behind(self) -> None:
        record = self.store.write(KEY, "approved")

        result = self.store.read_with_min_version(KEY, min_version=record.version)

        self.assertEqual(result.source, "leader_fallback")
        self.assertEqual(result.value, "approved")
        self.assertEqual(result.version, record.version)
        self.assertTrue(result.read_your_writes_ok)

    def test_min_version_fallback_preserves_leader_read_result(self) -> None:
        self.store.write(KEY, "approved")

        result = self.store.read_with_min_version(KEY, min_version=99)

        self.assertEqual(result.source, "leader_fallback")
        self.assertFalse(result.read_your_writes_ok)

    def test_demo_scenarios_show_stale_and_caught_up_reads(self) -> None:
        lines = run_demo([])

        self.assertTrue(any("follower read is stale" in line for line in lines))
        self.assertTrue(any("read_your_writes_ok=no" in line for line in lines))
        self.assertTrue(any("min-version read routes fresh" in line for line in lines))
        self.assertTrue(any("follower read is current" in line for line in lines))

    def test_demo_rejects_negative_lag(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--lag", "-1"])

    def test_demo_zero_lag_explains_labels(self) -> None:
        lines = run_demo(["--lag", "0"])

        self.assertTrue(any(line.startswith("note zero lag:") for line in lines))


if __name__ == "__main__":
    unittest.main()
