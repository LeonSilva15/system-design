import unittest

from retry_idempotency_demo import (
    ReservationSystem,
    run_duplicate_event_deliveries,
    run_duplicate_request_attempts,
)
from retry_idempotency_demo.demo import run_demo


class RetryIdempotencyTests(unittest.TestCase):
    def test_unsafe_retries_create_duplicate_reservations_and_emails(self) -> None:
        system = ReservationSystem()

        results = run_duplicate_request_attempts(
            system=system,
            attempts=3,
            member_id="member-7",
            workshop_id="workshop-python",
        )

        self.assertEqual([result.status for result in results], ["created"] * 3)
        self.assertEqual(len(system.reservations), 3)
        self.assertEqual(len(system.emails), 3)

    def test_idempotency_key_reuses_first_result_and_sends_once(self) -> None:
        system = ReservationSystem()

        results = run_duplicate_request_attempts(
            system=system,
            attempts=3,
            member_id="member-7",
            workshop_id="workshop-python",
            idempotency_key="reserve-1",
        )

        self.assertEqual(results[0].status, "created")
        self.assertEqual(
            [result.status for result in results[1:]],
            ["duplicate", "duplicate"],
        )
        self.assertEqual({result.reservation_id for result in results}, {"res-001"})
        self.assertEqual(len(system.reservations), 1)
        self.assertEqual(len(system.emails), 1)
        self.assertEqual(system.duplicate_requests, 2)

    def test_reusing_key_for_different_operation_returns_conflict(self) -> None:
        system = ReservationSystem()
        system.reserve_with_idempotency(
            member_id="member-7",
            workshop_id="workshop-python",
            idempotency_key="reserve-1",
        )

        conflict = system.reserve_with_idempotency(
            member_id="member-7",
            workshop_id="workshop-data",
            idempotency_key="reserve-1",
        )

        self.assertEqual(conflict.status, "conflict")
        self.assertTrue(conflict.duplicate)
        self.assertFalse(conflict.email_sent)
        self.assertEqual(len(system.reservations), 1)
        self.assertEqual(system.key_conflicts, 1)

    def test_duplicate_event_delivery_sends_side_effect_once(self) -> None:
        system = ReservationSystem()
        command = system.reserve_with_idempotency(
            member_id="member-7",
            workshop_id="workshop-python",
            idempotency_key="reserve-1",
        )

        results = run_duplicate_event_deliveries(
            system=system,
            deliveries=3,
            reservation_id=command.reservation_id or "",
            recipient="member-7",
            safe=True,
        )

        self.assertEqual(
            [result.status for result in results],
            ["sent", "duplicate_event", "duplicate_event"],
        )
        self.assertEqual(sum(result.email_sent for result in results), 1)
        self.assertEqual(system.duplicate_events, 2)
        self.assertEqual(len(system.emails), 2)

    def test_equivalent_event_with_new_id_does_not_repeat_side_effect(self) -> None:
        system = ReservationSystem()
        command = system.reserve_with_idempotency(
            member_id="member-7",
            workshop_id="workshop-python",
            idempotency_key="reserve-1",
        )
        reservation_id = command.reservation_id or ""
        first = system.handle_event_with_dedupe(
            event_id="reservation.confirmed:one",
            reservation_id=reservation_id,
            recipient="member-7",
        )
        second = system.handle_event_with_dedupe(
            event_id="reservation.confirmed:two",
            reservation_id=reservation_id,
            recipient="member-7",
        )

        self.assertEqual(first.status, "sent")
        self.assertEqual(second.status, "duplicate_side_effect")
        self.assertEqual(len(system.emails), 2)

    def test_demo_prints_unsafe_and_safe_summaries(self) -> None:
        lines = run_demo(["--attempts", "2", "--event-deliveries", "2"])

        self.assertIn("summary mode=unsafe reservations=2 emails=2", lines)
        self.assertIn(
            "summary mode=safe reservations=1 emails=1 "
            "key_conflicts=0 duplicate_requests=1",
            lines,
        )
        self.assertTrue(
            any(
                line == "summary mode=events event_side_effects=1 "
                "total_emails=2 duplicate_events=1"
                for line in lines
            )
        )

    def test_demo_prints_key_conflict_scenario(self) -> None:
        lines = run_demo(["--mode", "safe", "--show-conflict"])

        self.assertIn("scenario=key_conflict", lines)
        self.assertIn(
            "attempt=1 status=conflict reservation=res-001 "
            "duplicate=true email_sent=false",
            lines,
        )
        self.assertIn(
            "summary mode=conflict reservations=1 emails=1 key_conflicts=1",
            lines,
        )


if __name__ == "__main__":
    unittest.main()
