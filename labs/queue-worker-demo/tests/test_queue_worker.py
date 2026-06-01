from __future__ import annotations

import unittest

from queue_worker_demo import InMemoryQueue, JobNotInflight, ManualClock, Worker
from queue_worker_demo.demo import run_demo


class QueueWorkerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = ManualClock()
        self.queue = InMemoryQueue(self.clock)

    def test_enqueue_claim_and_complete_job(self) -> None:
        job = self.queue.enqueue("email", "request-1")
        worker = Worker("worker-a", self.queue, visibility_timeout=5.0)

        claimed = worker.claim()
        result = self.queue.complete(job.job_id, "worker-a")
        metrics = self.queue.metrics()

        self.assertEqual(claimed, job)
        self.assertEqual(result.outcome, "success")
        self.assertEqual(job.status, "completed")
        self.assertEqual(job.attempts, 1)
        self.assertEqual(metrics.completed, 1)
        self.assertEqual(metrics.inflight, 0)

    def test_retryable_failure_is_hidden_until_retry_delay(self) -> None:
        self.queue.enqueue("email", "request-2", max_attempts=3)
        worker = Worker("worker-a", self.queue, visibility_timeout=5.0)

        failed = worker.run_once(outcome="retryable", retry_delay=3.0)
        immediately_visible = worker.claim()
        self.clock.advance(3.0)
        retried = worker.claim()

        self.assertIsNotNone(failed)
        self.assertEqual(failed.outcome, "retry_scheduled")
        self.assertIsNone(immediately_visible)
        self.assertIsNotNone(retried)
        self.assertEqual(retried.attempts, 2)

    def test_retry_exhaustion_dead_letters_job(self) -> None:
        self.queue.enqueue("webhook", "bad-payload", max_attempts=2)
        worker = Worker("worker-a", self.queue, visibility_timeout=5.0)

        first = worker.run_once(outcome="retryable", retry_delay=1.0)
        self.clock.advance(1.0)
        second = worker.run_once(outcome="retryable", retry_delay=1.0)
        metrics = self.queue.metrics()

        self.assertIsNotNone(first)
        self.assertEqual(first.outcome, "retry_scheduled")
        self.assertIsNotNone(second)
        self.assertEqual(second.outcome, "dead_lettered")
        self.assertEqual(metrics.dead_lettered, 1)
        self.assertEqual(metrics.visible, 0)

    def test_visibility_timeout_redelivers_unacked_job(self) -> None:
        job = self.queue.enqueue("report", "report-1")
        worker_a = Worker("worker-a", self.queue, visibility_timeout=5.0)
        worker_b = Worker("worker-b", self.queue, visibility_timeout=5.0)

        crashed = worker_a.run_once(outcome="crash")
        self.clock.advance(5.1)
        expired = self.queue.reap_expired_leases()
        redelivered = worker_b.claim()

        self.assertIsNotNone(crashed)
        self.assertEqual(crashed.outcome, "crashed")
        self.assertEqual(expired, [job])
        self.assertEqual(redelivered, job)
        self.assertEqual(job.attempts, 2)
        self.assertEqual(job.worker_id, "worker-b")
        self.assertEqual(self.queue.metrics().expired_leases, 1)

    def test_old_worker_cannot_ack_after_lease_expires(self) -> None:
        job = self.queue.enqueue("report", "report-2")
        worker_a = Worker("worker-a", self.queue, visibility_timeout=5.0)
        worker_b = Worker("worker-b", self.queue, visibility_timeout=5.0)

        worker_a.run_once(outcome="crash")
        self.clock.advance(5.1)
        worker_b.claim()

        with self.assertRaises(JobNotInflight):
            self.queue.complete(job.job_id, "worker-a")

    def test_worker_cannot_ack_after_timeout_before_another_claim(self) -> None:
        job = self.queue.enqueue("report", "report-3")
        worker = Worker("worker-a", self.queue, visibility_timeout=5.0)

        worker.claim()
        self.clock.advance(5.1)

        with self.assertRaises(JobNotInflight):
            self.queue.complete(job.job_id, "worker-a")

        self.assertEqual(job.status, "retrying")
        self.assertIsNone(job.worker_id)
        self.assertEqual(self.queue.expired_leases, 1)

    def test_demo_rejects_max_attempts_below_two(self) -> None:
        with self.assertRaises(SystemExit):
            run_demo(["--max-attempts", "1"])

    def test_metrics_report_basic_observability(self) -> None:
        self.queue.enqueue("email", "request-3")
        metrics = self.queue.metrics()

        self.assertEqual(metrics.queued, 1)
        self.assertEqual(metrics.visible, 1)
        self.assertEqual(metrics.inflight, 0)
        self.assertEqual(metrics.completed, 0)
        self.assertEqual(metrics.dead_lettered, 0)
        self.assertEqual(metrics.oldest_visible_age, 0.0)

    def test_demo_smoke_output(self) -> None:
        lines = run_demo(["--max-attempts", "2"])

        self.assertTrue(any("worker completes" in line for line in lines))
        self.assertTrue(any("retry succeeds" in line for line in lines))
        self.assertTrue(any("dead_lettered" in line for line in lines))
        self.assertTrue(any("redelivered to another worker" in line for line in lines))
        self.assertTrue(lines[-1].startswith("15 final metrics:"))


if __name__ == "__main__":
    unittest.main()
