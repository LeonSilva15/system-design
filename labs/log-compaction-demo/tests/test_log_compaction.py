from __future__ import annotations

import unittest

from log_compaction_demo import (
    AppendOnlyLog,
    Consumer,
    OffsetOutOfRange,
)
from log_compaction_demo.demo import run_demo, seed_inventory_log


class LogCompactionTests(unittest.TestCase):
    def test_append_only_log_assigns_monotonic_offsets(self) -> None:
        log = AppendOnlyLog()

        first = log.append("item:tent", "available=3")
        second = log.append("item:tent", "available=2")

        self.assertEqual(first.offset, 0)
        self.assertEqual(second.offset, 1)
        self.assertEqual(log.high_watermark, 2)
        self.assertEqual([record.value for record in log.records], ["available=3", "available=2"])

    def test_consumer_reads_from_offset_and_advances_checkpoint(self) -> None:
        log = seed_inventory_log()
        consumer = Consumer("search")

        first = consumer.poll(log, max_records=3)
        second = consumer.poll(log, max_records=2)

        self.assertEqual([record.offset for record in first.records], [0, 1, 2])
        self.assertEqual(first.next_offset, 3)
        self.assertEqual(first.lag, 4)
        self.assertEqual([record.offset for record in second.records], [3, 4])
        self.assertEqual(consumer.next_offset, 5)
        self.assertEqual(consumer.projection["item:lamp"], "available=4")

    def test_latest_value_compaction_keeps_latest_record_per_key(self) -> None:
        log = seed_inventory_log()

        result = log.compact_latest()

        self.assertEqual(result.before_count, 7)
        self.assertEqual(result.after_count, 3)
        self.assertEqual(result.removed_count, 4)
        self.assertEqual([record.offset for record in result.records], [4, 5, 6])
        self.assertEqual(result.live_values, {"item:lamp": "available=4", "item:tent": "available=3"})
        self.assertEqual(result.tombstone_keys, ("item:stove",))

    def test_retention_removes_old_offsets(self) -> None:
        log = seed_inventory_log()

        result = log.retain_last(5)

        self.assertEqual([record.offset for record in result.removed_records], [0, 1])
        self.assertEqual(log.earliest_offset, 2)
        self.assertEqual([record.offset for record in log.records], [2, 3, 4, 5, 6])

    def test_consumer_before_retention_window_gets_offset_error(self) -> None:
        log = seed_inventory_log()
        log.retain_last(5)
        consumer = Consumer("slow")

        with self.assertRaises(OffsetOutOfRange):
            consumer.poll(log, max_records=2)

    def test_tombstone_removes_value_from_consumer_projection(self) -> None:
        log = seed_inventory_log()
        consumer = Consumer("projection")

        consumer.poll(log, max_records=10)

        self.assertEqual(consumer.projection["item:tent"], "available=3")
        self.assertEqual(consumer.projection["item:lamp"], "available=4")
        self.assertNotIn("item:stove", consumer.projection)

    def test_demo_smoke_output(self) -> None:
        lines = run_demo([])
        output = "\n".join(lines)

        self.assertTrue(any("append-only log" in line for line in lines))
        self.assertTrue(any("latest-value compaction" in line for line in lines))
        self.assertTrue(any("consumer poll" in line for line in lines))
        self.assertTrue(any("next_offset" in line for line in lines))
        self.assertTrue(any("retention:" in line for line in lines))
        self.assertTrue(any("retention gap" in line for line in lines))
        self.assertIn("07 retention gap:", output)
        self.assertIn(
            "projection=item:lamp=available=4,item:tent=available=3",
            lines[-1],
        )

    def test_documented_parameter_examples_do_not_crash(self) -> None:
        examples = [
            ["--batch-size", "2"],
            ["--retention-records", "3"],
            ["--batch-size", "1", "--retention-records", "6"],
        ]

        for example in examples:
            with self.subTest(example=example):
                lines = run_demo(example)
                self.assertTrue(lines[-1].startswith("08 final consumer poll:"))

    def test_short_retention_gap_recovers_from_compacted_snapshot(self) -> None:
        lines = run_demo(["--retention-records", "3"])
        output = "\n".join(lines)

        self.assertIn("06 consumer catch-up gap:", output)
        self.assertIn("action=load_compacted_snapshot", output)
        self.assertIn("06b snapshot recovery:", output)
        self.assertIn("projection=item:lamp=available=4,item:tent=available=3", output)

    def test_demo_rejects_invalid_retention_record_count(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--retention-records", "0"])

    def test_demo_rejects_invalid_batch_size(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--batch-size", "0"])


if __name__ == "__main__":
    unittest.main()
