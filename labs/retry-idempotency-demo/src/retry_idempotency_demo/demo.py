"""Command-line demo for retry and idempotency behavior."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import (
    CommandResult,
    EventResult,
    ReservationSystem,
    run_duplicate_event_deliveries,
    run_duplicate_request_attempts,
)


def non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return parsed


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def non_empty(value: str) -> str:
    if not value:
        raise argparse.ArgumentTypeError("must not be empty")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simulate unsafe retries and idempotency-key protected retries."
    )
    parser.add_argument(
        "--mode",
        choices=("unsafe", "safe", "both"),
        default="both",
        help="Which request flow to run.",
    )
    parser.add_argument(
        "--attempts",
        type=positive_int,
        default=3,
        help="Number of duplicate client attempts.",
    )
    parser.add_argument(
        "--event-deliveries",
        type=non_negative_int,
        default=2,
        help="Number of duplicate event deliveries in the safe flow.",
    )
    parser.add_argument(
        "--member",
        type=non_empty,
        default="member-7",
        help="Member identity used in the request fingerprint.",
    )
    parser.add_argument(
        "--workshop",
        type=non_empty,
        default="workshop-python",
        help="Workshop identity used in the request fingerprint.",
    )
    parser.add_argument(
        "--idempotency-key",
        type=non_empty,
        default="reserve-2026-05",
        help="Stable key reused across request retries.",
    )
    parser.add_argument(
        "--show-conflict",
        action="store_true",
        help="Reuse the same idempotency key for a different workshop.",
    )
    return parser


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def format_command_result(index: int, result: CommandResult) -> str:
    reservation_id = result.reservation_id or "none"
    return (
        f"attempt={index} "
        f"status={result.status} "
        f"reservation={reservation_id} "
        f"duplicate={bool_text(result.duplicate)} "
        f"email_sent={bool_text(result.email_sent)}"
    )


def format_event_result(index: int, result: EventResult) -> str:
    return (
        f"delivery={index} "
        f"status={result.status} "
        f"duplicate={bool_text(result.duplicate)} "
        f"email_sent={bool_text(result.email_sent)}"
    )


def unsafe_lines(args: argparse.Namespace) -> list[str]:
    system = ReservationSystem()
    results = run_duplicate_request_attempts(
        system=system,
        attempts=args.attempts,
        member_id=args.member,
        workshop_id=args.workshop,
    )
    lines = [f"scenario=unsafe_requests attempts={args.attempts}"]
    lines.extend(
        format_command_result(index, result)
        for index, result in enumerate(results, 1)
    )
    lines.append(
        f"summary mode=unsafe reservations={len(system.reservations)} emails={len(system.emails)}"
    )
    return lines


def safe_lines(args: argparse.Namespace) -> list[str]:
    system = ReservationSystem()
    results = run_duplicate_request_attempts(
        system=system,
        attempts=args.attempts,
        member_id=args.member,
        workshop_id=args.workshop,
        idempotency_key=args.idempotency_key,
    )
    lines = [
        f"scenario=safe_requests attempts={args.attempts} key={args.idempotency_key}"
    ]
    lines.extend(
        format_command_result(index, result)
        for index, result in enumerate(results, 1)
    )
    lines.append(
        "summary mode=safe "
        f"reservations={len(system.reservations)} "
        f"emails={len(system.emails)} "
        f"key_conflicts={system.key_conflicts} "
        f"duplicate_requests={system.duplicate_requests}"
    )

    if args.show_conflict:
        conflict = system.reserve_with_idempotency(
            member_id=args.member,
            workshop_id=f"{args.workshop}-advanced",
            idempotency_key=args.idempotency_key,
        )
        lines.append("scenario=key_conflict")
        lines.append(format_command_result(1, conflict))
        lines.append(
            "summary mode=conflict "
            f"reservations={len(system.reservations)} "
            f"emails={len(system.emails)} "
            f"key_conflicts={system.key_conflicts}"
        )

    reservation_id = results[0].reservation_id if results else "res-none"
    event_results = run_duplicate_event_deliveries(
        system=system,
        deliveries=args.event_deliveries,
        reservation_id=reservation_id or "res-none",
        recipient=args.member,
        safe=True,
    )
    event_side_effects = sum(1 for result in event_results if result.email_sent)
    lines.append(
        f"scenario=duplicate_events deliveries={args.event_deliveries} reservation={reservation_id}"
    )
    lines.extend(
        format_event_result(index, result)
        for index, result in enumerate(event_results, 1)
    )
    lines.append(
        "summary mode=events "
        f"event_side_effects={event_side_effects} "
        f"total_emails={len(system.emails)} "
        f"duplicate_events={system.duplicate_events}"
    )
    return lines


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    lines: list[str] = []
    if args.mode in ("unsafe", "both"):
        lines.extend(unsafe_lines(args))
    if args.mode in ("safe", "both"):
        if lines:
            lines.append("---")
        lines.extend(safe_lines(args))
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
