"""Command-line demo for the token bucket lab."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .bucket import LimitDecision, TokenBucket, simulate_requests


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simulate token bucket rate limiting decisions."
    )
    parser.add_argument(
        "--capacity",
        type=float,
        default=5.0,
        help="Maximum tokens the bucket can hold. This is the burst size.",
    )
    parser.add_argument(
        "--refill-rate",
        type=float,
        default=1.0,
        help="Tokens added per second.",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=10,
        help="Number of requests to simulate.",
    )
    parser.add_argument(
        "--spacing",
        type=float,
        default=0.2,
        help="Seconds between simulated requests.",
    )
    parser.add_argument(
        "--cost",
        type=float,
        default=1.0,
        help="Tokens spent by each request.",
    )
    parser.add_argument(
        "--start-empty",
        action="store_true",
        help="Start with zero tokens instead of a full bucket.",
    )
    return parser


def format_decision(index: int, decision: LimitDecision) -> str:
    outcome = "allowed" if decision.allowed else "limited"
    return (
        f"request={index:02d} "
        f"at={decision.requested_at:.2f}s "
        f"decision={outcome} "
        f"tokens_before={decision.tokens_before:.2f} "
        f"tokens_after={decision.tokens_after:.2f} "
        f"retry_after={decision.retry_after:.2f}s"
    )


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    bucket = TokenBucket(
        capacity=args.capacity,
        refill_rate=args.refill_rate,
        tokens=0.0 if args.start_empty else None,
    )
    decisions = simulate_requests(
        bucket=bucket,
        request_count=args.requests,
        spacing=args.spacing,
        cost=args.cost,
    )

    lines = [
        (
            f"config capacity={args.capacity:.2f} "
            f"refill_rate={args.refill_rate:.2f} tokens/sec "
            f"cost={args.cost:.2f} "
            f"spacing={args.spacing:.2f} "
            f"requests={args.requests}"
        )
    ]
    lines.extend(
        format_decision(index, decision)
        for index, decision in enumerate(decisions, start=1)
    )

    allowed = sum(1 for decision in decisions if decision.allowed)
    limited = len(decisions) - allowed
    lines.append(
        f"summary allowed={allowed} limited={limited} final_tokens={bucket.tokens:.2f}"
    )
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
