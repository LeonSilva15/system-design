"""Command-line demo for the dead-letter queue lab."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import (
    DeadLetterQueue,
    ManualClock,
    ReplayNotAllowed,
    WorkQueue,
    WorkResult,
    Worker,
    format_alerts,
    format_dead_letters,
    yes_no,
)


OWNER = "member_notifications"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demonstrate poison messages, retry exhaustion, DLQ inspection, replay, and alerting."
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=3,
        help="Retryable attempts before retry exhaustion moves a job to the DLQ.",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=2.0,
        help="Seconds before a retryable failure becomes visible again.",
    )
    parser.add_argument(
        "--alert-age",
        type=float,
        default=10.0,
        help="Oldest open dead-letter age that should alert.",
    )
    parser.add_argument(
        "--alert-count",
        type=int,
        default=2,
        help="Open dead-letter count that should alert.",
    )
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    if args.max_attempts < 2:
        raise SystemExit("--max-attempts must be at least 2")
    if args.retry_delay < 0:
        raise SystemExit("--retry-delay cannot be negative")
    if args.alert_age <= 0:
        raise SystemExit("--alert-age must be greater than 0")
    if args.alert_count < 1:
        raise SystemExit("--alert-count must be at least 1")


def _format_result(label: str, result: WorkResult) -> str:
    category = result.error_category or "none"
    dead_letter = result.dead_letter_id or "none"
    replayable = "unknown" if result.replayable is None else yes_no(result.replayable)
    return (
        f"{label}: job={result.job_id} outcome={result.outcome} "
        f"status={result.status} attempts={result.attempts} "
        f"category={category} dlq={dead_letter} replayable={replayable}"
    )


def _claim_required(worker: Worker) -> object:
    job = worker.claim()
    if job is None:
        raise RuntimeError("expected a visible job")
    return job


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    _validate_args(args)

    clock = ManualClock()
    dead_letters = DeadLetterQueue()
    queue = WorkQueue(clock, dead_letters)
    worker = Worker("worker-a", queue)
    lines = [
        (
            f"config max_attempts={args.max_attempts} "
            f"retry_delay={args.retry_delay:.1f}s alert_age={args.alert_age:.1f}s "
            f"alert_count={args.alert_count}"
        )
    ]

    normal = queue.enqueue(
        "pickup_reminder",
        "reservation=res-100,email=ok",
        owner=OWNER,
        max_attempts=args.max_attempts,
        idempotency_key="res-100:pickup-reminder",
    )
    normal_claim = _claim_required(worker)
    normal_result = worker.complete(normal_claim)
    lines.append(f"01 completed normal job: job={normal.job_id} outcome={normal_result.outcome}")

    poison = queue.enqueue(
        "pickup_reminder",
        "reservation=res-101,email=missing",
        owner=OWNER,
        max_attempts=args.max_attempts,
        idempotency_key="res-101:pickup-reminder",
    )
    poison_claim = _claim_required(worker)
    poison_result = worker.fail(
        poison_claim,
        error_category="invalid_recipient",
        safe_message="provider_rejected_address",
        retryable=False,
        replayable=False,
        retry_delay=args.retry_delay,
    )
    lines.append(_format_result("02 poison message dead-lettered", poison_result))

    retrying = queue.enqueue(
        "pickup_reminder",
        "reservation=res-102,template=bad-locale",
        owner=OWNER,
        max_attempts=args.max_attempts,
        idempotency_key="res-102:pickup-reminder",
    )
    for attempt in range(1, args.max_attempts + 1):
        claimed = _claim_required(worker)
        result = worker.fail(
            claimed,
            error_category="handler_bug",
            safe_message="template_render_error",
            retryable=True,
            replayable=True,
            retry_delay=args.retry_delay,
        )
        label = "03 retry exhausted" if result.outcome == "dead_lettered" else f"03.{attempt} retry scheduled"
        lines.append(_format_result(label, result))
        if result.outcome != "dead_lettered":
            clock.advance(args.retry_delay)
    lines.append(f"   retry subject: job={retrying.job_id} final_status={retrying.status}")

    open_records = dead_letters.open_records()
    lines.append(
        (
            f"04 dlq inspection: open={len(open_records)} "
            f"records={format_dead_letters(open_records)}"
        )
    )

    clock.advance(args.alert_age + 1.0)
    alerts = dead_letters.alerts(
        now=clock.now,
        oldest_age_threshold=args.alert_age,
        count_threshold=args.alert_count,
    )
    lines.append(
        (
            f"05 alerting: alerts={len(alerts)} "
            f"signals={format_alerts(alerts)}"
        )
    )

    replayable = next(record for record in open_records if record.replayable)
    replay_job = queue.replay_dead_letter(
        replayable.dead_letter_id,
        reason="template handler patched",
        payload="reservation=res-102,template=fixed",
    )
    replay_claim = _claim_required(worker)
    replay_result = worker.complete(replay_claim)
    dead_letters.mark_resolved(
        replayable.dead_letter_id,
        action="replayed",
        reason="replay job completed",
        now=clock.now,
    )
    lines.append(
        (
            f"06 replay: dlq={replayable.dead_letter_id} replay_job={replay_job.job_id} "
            f"idempotency_key={replay_job.idempotency_key} outcome={replay_result.outcome} "
            f"dlq_status={dead_letters.inspect(replayable.dead_letter_id).status}"
        )
    )

    non_replayable = next(record for record in dead_letters.open_records() if not record.replayable)
    try:
        queue.replay_dead_letter(
            non_replayable.dead_letter_id,
            reason="operator clicked replay",
        )
    except ReplayNotAllowed as exc:
        lines.append(
            (
                f"07 unsafe replay blocked: dlq={non_replayable.dead_letter_id} "
                f"category={non_replayable.last_error_category} "
                f"action=correct_input_or_cancel message={exc}"
            )
        )

    final_open = dead_letters.open_records()
    replayed = dead_letters.records_by_status("replayed")
    lines.append(
        (
            f"08 final dlq state: open={len(final_open)} replayed={len(replayed)} "
            f"records={format_dead_letters(final_open)}"
        )
    )
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
