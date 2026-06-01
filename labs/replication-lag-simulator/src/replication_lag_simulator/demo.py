"""Command-line demo for the replication lag simulator."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import LeaderFollowerStore, ManualClock, ReadResult, ReplicationStatus


KEY = "reservation:community-room"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demonstrate leader writes, follower lag, stale reads, and read-your-writes violations."
    )
    parser.add_argument(
        "--lag",
        type=float,
        default=5.0,
        help="Seconds before a leader write becomes visible on the follower.",
    )
    parser.add_argument(
        "--half-step",
        type=float,
        default=2.5,
        help="Seconds to advance before issuing a second leader write.",
    )
    return parser


def format_read(label: str, result: ReadResult) -> str:
    stale = "yes" if result.stale else "no"
    ryw = "yes" if result.read_your_writes_ok else "no"
    return (
        f"{label}: source={result.source} value={result.value} "
        f"version={result.version} leader_version={result.leader_version} "
        f"stale={stale} read_your_writes_ok={ryw} note={result.note}"
    )


def format_status(label: str, status: ReplicationStatus) -> str:
    next_apply = "none"
    if status.seconds_until_next_apply is not None:
        next_apply = f"{status.seconds_until_next_apply:.1f}s"
    return (
        f"{label}: leader_version={status.leader_version} "
        f"follower_version={status.follower_version} "
        f"versions_behind={status.versions_behind} "
        f"pending_events={status.pending_events} next_apply={next_apply}"
    )


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    if args.lag < 0:
        raise SystemExit("--lag cannot be negative")
    if args.half_step < 0:
        raise SystemExit("--half-step cannot be negative")

    clock = ManualClock()
    store = LeaderFollowerStore(clock, replication_delay=args.lag)
    lines = [f"config lag={args.lag:.1f}s half_step={args.half_step:.1f}s"]
    if args.lag == 0:
        lines.append(
            "note zero lag: follower reads may be current even when step labels describe the lag scenario"
        )

    first = store.write(KEY, "approved by coordinator")
    lines.append(
        f"01 leader write: key={KEY} value={first.value} version={first.version}"
    )
    lines.append(format_read("02 leader read sees write", store.read_leader(KEY)))
    lines.append(
        format_read(
            "03 follower read is stale",
            store.read_follower(KEY, min_version=first.version),
        )
    )
    lines.append(format_status("04 lag status", store.status(KEY)))

    clock.advance(args.half_step)
    second = store.write(KEY, "approved with projector")
    lines.append(
        f"05 second leader write: value={second.value} version={second.version}"
    )
    lines.append(
        format_read(
            "06 follower still violates read-your-writes",
            store.read_follower(KEY, min_version=second.version),
        )
    )

    clock.advance(max(0.0, args.lag - args.half_step))
    lines.append(format_status("07 first write reaches follower", store.status(KEY)))
    lines.append(format_read("08 follower stale behind second write", store.read_follower(KEY)))
    lines.append(
        format_read(
            "09 min-version read routes fresh",
            store.read_with_min_version(KEY, min_version=second.version),
        )
    )

    clock.advance(args.half_step)
    lines.append(format_status("10 follower caught up", store.status(KEY)))
    lines.append(format_read("11 follower read is current", store.read_follower(KEY)))
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
