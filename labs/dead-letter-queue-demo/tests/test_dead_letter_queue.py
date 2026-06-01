from __future__ import annotations

import unittest

from dead_letter_queue_demo import (
    DeadLetterQueue,
    ManualClock,
    ReplayNotAllowed,
    WorkQueue,
    Worker,
)
from dead_letter_queue_demo.demo import run_demo


class DeadLetterQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = ManualClock()
        self.dead_letters = DeadLetterQueue()
        self.queue = WorkQueue(self.clock, self.dead_letters)
        self.worker = Worker("worker-a", self.queue)

    def enqueue_and_claim(self, payload: str, *, max_attempts: int = 3):
        job = self.queue.enqueue(
            "pickup_reminder",
            payload,
            owner="member_notifications",
            max_attempts=max_attempts,
            idempotency_key=f"{payload}:pickup-reminder",
        )
        claimed = self.worker.claim()
        self.assertEqual(claimed, job)
        return job

    def test_poison_message_dead_letters_without_retry(self) -> None:
        job = self.enqueue_and_claim("reservation=res-1,email=missing")

        result = self.worker.fail(
            job,
            error_category="invalid_recipient",
            safe_message="provider_rejected_address",
            retryable=False,
            replayable=False,
            retry_delay=2.0,
        )
        record = self.dead_letters.inspect(result.dead_letter_id or "")

        self.assertEqual(result.outcome, "dead_lettered")
        self.assertEqual(result.attempts, 1)
        self.assertFalse(record.replayable)
        self.assertEqual(record.last_error_category, "invalid_recipient")

    def test_retry_exhaustion_moves_to_dlq(self) -> None:
        self.enqueue_and_claim("reservation=res-2,template=bad", max_attempts=2)

        first = self.worker.fail(
            self.queue.jobs["job-001"],
            error_category="handler_bug",
            safe_message="template_render_error",
            retryable=True,
            replayable=True,
            retry_delay=1.0,
        )
        self.clock.advance(1.0)
        claimed = self.worker.claim()
        second = self.worker.fail(
            claimed,
            error_category="handler_bug",
            safe_message="template_render_error",
            retryable=True,
            replayable=True,
            retry_delay=1.0,
        )

        self.assertEqual(first.outcome, "retry_scheduled")
        self.assertEqual(second.outcome, "dead_lettered")
        self.assertEqual(second.attempts, 2)
        self.assertEqual(len(self.dead_letters.open_records()), 1)

    def test_dlq_inspection_exposes_safe_context(self) -> None:
        job = self.enqueue_and_claim("reservation=res-3,email=missing")

        result = self.worker.fail(
            job,
            error_category="invalid_recipient",
            safe_message="provider_rejected_address",
            retryable=False,
            replayable=False,
            retry_delay=2.0,
        )

        record = self.dead_letters.inspect(result.dead_letter_id or "")
        self.assertEqual(record.job_id, job.job_id)
        self.assertEqual(record.owner, "member_notifications")
        self.assertEqual(record.safe_message, "provider_rejected_address")
        self.assertEqual(record.idempotency_key, job.idempotency_key)

    def test_alerts_fire_on_open_count_and_oldest_age(self) -> None:
        for index in range(2):
            job = self.enqueue_and_claim(f"reservation=res-{index},email=missing")
            self.worker.fail(
                job,
                error_category="invalid_recipient",
                safe_message="provider_rejected_address",
                retryable=False,
                replayable=False,
                retry_delay=2.0,
            )
        self.clock.advance(11.0)

        alerts = self.dead_letters.alerts(
            now=self.clock.now,
            oldest_age_threshold=10.0,
            count_threshold=2,
        )

        self.assertEqual([alert.name for alert in alerts], ["dlq_open_count", "dlq_oldest_age"])

    def test_replay_reuses_idempotency_key_and_can_be_resolved(self) -> None:
        job = self.enqueue_and_claim("reservation=res-4,template=bad")
        result = self.worker.fail(
            job,
            error_category="handler_bug",
            safe_message="template_render_error",
            retryable=False,
            replayable=True,
            retry_delay=0.0,
        )

        replay_job = self.queue.replay_dead_letter(
            result.dead_letter_id or "",
            reason="handler patched",
            payload="reservation=res-4,template=fixed",
        )
        replay_claim = self.worker.claim()
        replay_result = self.worker.complete(replay_claim)
        self.dead_letters.mark_resolved(
            result.dead_letter_id or "",
            action="replayed",
            reason="replay completed",
            now=self.clock.now,
        )

        self.assertEqual(replay_job.idempotency_key, job.idempotency_key)
        self.assertEqual(replay_result.outcome, "success")
        self.assertEqual(len(self.dead_letters.records_by_status("replayed")), 1)

    def test_non_replayable_dead_letter_rejects_replay(self) -> None:
        job = self.enqueue_and_claim("reservation=res-5,email=missing")
        result = self.worker.fail(
            job,
            error_category="invalid_recipient",
            safe_message="provider_rejected_address",
            retryable=False,
            replayable=False,
            retry_delay=0.0,
        )

        with self.assertRaises(ReplayNotAllowed):
            self.queue.replay_dead_letter(result.dead_letter_id or "", reason="unsafe")

    def test_duplicate_replay_enqueue_is_blocked(self) -> None:
        job = self.enqueue_and_claim("reservation=res-6,template=bad")
        result = self.worker.fail(
            job,
            error_category="handler_bug",
            safe_message="template_render_error",
            retryable=False,
            replayable=True,
            retry_delay=0.0,
        )

        self.queue.replay_dead_letter(result.dead_letter_id or "", reason="handler patched")

        with self.assertRaises(ReplayNotAllowed):
            self.queue.replay_dead_letter(result.dead_letter_id or "", reason="duplicate click")

    def test_demo_smoke_output(self) -> None:
        lines = run_demo([])
        output = "\n".join(lines)

        self.assertIn("poison message dead-lettered", output)
        self.assertIn("retry exhausted", output)
        self.assertIn("dlq inspection", output)
        self.assertIn("alerting", output)
        self.assertIn("06 replay:", output)
        self.assertIn("unsafe replay blocked", output)
        self.assertIn("08 final dlq state:", output)

    def test_demo_rejects_invalid_max_attempts(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--max-attempts", "1"])

    def test_demo_rejects_invalid_alert_count(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--alert-count", "0"])


if __name__ == "__main__":
    unittest.main()
