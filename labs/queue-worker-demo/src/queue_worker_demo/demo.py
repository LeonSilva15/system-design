"""Command-line demo for the queue worker lab."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import InMemoryQueue, ManualClock, QueueMetrics, WorkResult, Worker


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demonstrate queue workers, retries, failures, and visibility timeouts."
    )
    parser.add_argument(
        "--visibility-timeout",
        type=float,
        default=5.0,
        help="Seconds a claimed job stays hidden before another worker can retry it.",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=3.0,
        help="Seconds before a retryable failure becomes visible again.",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=3,
        help="Maximum retryable attempts before a job is dead-lettered.",
    )
    return parser


def format_result(label: str, result: WorkResult | None) -> str:
    if result is None:
        return f"{label}: no visible job"
    return (
        f"{label}: job={result.job_id} worker={result.worker_id} "
        f"outcome={result.outcome} status={result.status} "
        f"attempts={result.attempts} message={result.message}"
    )


def format_metrics(label: str, metrics: QueueMetrics) -> str:
    age = "none"
    if metrics.oldest_visible_age is not None:
        age = f"{metrics.oldest_visible_age:.1f}s"
    return (
        f"{label}: queued={metrics.queued} visible={metrics.visible} "
        f"inflight={metrics.inflight} completed={metrics.completed} "
        f"dead_lettered={metrics.dead_lettered} retries={metrics.retries_scheduled} "
        f"expired_leases={metrics.expired_leases} oldest_visible_age={age}"
    )


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    if args.visibility_timeout <= 0:
        raise SystemExit("--visibility-timeout must be greater than 0")
    if args.retry_delay < 0:
        raise SystemExit("--retry-delay cannot be negative")
    if args.max_attempts < 2:
        raise SystemExit("--max-attempts must be at least 2 for this demo")

    clock = ManualClock()
    queue = InMemoryQueue(clock)
    worker_a = Worker(
        "worker-a",
        queue,
        visibility_timeout=args.visibility_timeout,
    )
    worker_b = Worker(
        "worker-b",
        queue,
        visibility_timeout=args.visibility_timeout,
    )

    lines = [
        (
            f"config visibility_timeout={args.visibility_timeout:.1f}s "
            f"retry_delay={args.retry_delay:.1f}s "
            f"max_attempts={args.max_attempts}"
        )
    ]

    success = queue.enqueue("thumbnail", "video-101", max_attempts=args.max_attempts)
    lines.append(f"01 enqueue success job: job={success.job_id} kind={success.kind}")
    lines.append(format_metrics("02 after enqueue", queue.metrics()))
    lines.append(format_result("03 worker completes", worker_a.run_once()))
    lines.append(format_metrics("04 after completion", queue.metrics()))

    retry = queue.enqueue("email", "request-202", max_attempts=args.max_attempts)
    lines.append(f"05 enqueue retry job: job={retry.job_id} kind={retry.kind}")
    lines.append(
        format_result(
            "06 first attempt fails",
            worker_a.run_once(outcome="retryable", retry_delay=args.retry_delay),
        )
    )
    lines.append(format_metrics("07 retry scheduled", queue.metrics()))
    clock.advance(args.retry_delay)
    lines.append(format_result("08 retry succeeds", worker_b.run_once()))

    poison = queue.enqueue("webhook", "bad-payload", max_attempts=args.max_attempts)
    lines.append(f"09 enqueue failing job: job={poison.job_id} kind={poison.kind}")
    for attempt in range(1, args.max_attempts + 1):
        lines.append(
            format_result(
                f"10.{attempt} retryable failure",
                worker_a.run_once(
                    outcome="retryable",
                    retry_delay=args.retry_delay,
                    error="provider timeout",
                ),
            )
        )
        clock.advance(args.retry_delay)

    stuck = queue.enqueue("report", "report-303", max_attempts=args.max_attempts)
    lines.append(f"11 enqueue visibility-timeout job: job={stuck.job_id} kind={stuck.kind}")
    crashed = worker_a.run_once(outcome="crash")
    lines.append(format_result("12 worker crashes before ack", crashed))
    clock.advance(args.visibility_timeout + 0.1)
    queue.reap_expired_leases()
    lines.append(format_metrics("13 after visibility timeout", queue.metrics()))
    lines.append(format_result("14 redelivered to another worker", worker_b.run_once()))
    lines.append(format_metrics("15 final metrics", queue.metrics()))
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
