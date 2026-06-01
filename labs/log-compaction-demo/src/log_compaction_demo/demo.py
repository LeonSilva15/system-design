"""Command-line demo for the log compaction lab."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import (
    AppendOnlyLog,
    Consumer,
    OffsetOutOfRange,
    format_offsets,
    format_projection,
    format_records,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demonstrate append-only logs, latest-value compaction, consumers, offsets, and retention."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=3,
        help="Maximum records a consumer reads per poll.",
    )
    parser.add_argument(
        "--retention-records",
        type=int,
        default=5,
        help="Number of latest records retained in the hot log.",
    )
    return parser


def seed_inventory_log() -> AppendOnlyLog:
    log = AppendOnlyLog()
    log.append("item:tent", "available=3")
    log.append("item:lamp", "available=5")
    log.append("item:tent", "available=2")
    log.append("item:stove", "available=1")
    log.append("item:lamp", "available=4")
    log.append("item:tent", "available=3")
    log.tombstone("item:stove")
    return log


def _validate_args(args: argparse.Namespace) -> None:
    if args.batch_size < 1:
        raise SystemExit("--batch-size must be at least 1")
    if args.retention_records < 1:
        raise SystemExit("--retention-records must be at least 1")


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    _validate_args(args)

    log = seed_inventory_log()
    search = Consumer("search-projection")
    lines = [
        (
            f"config batch_size={args.batch_size} "
            f"retention_records={args.retention_records}"
        ),
        (
            f"01 append-only log: records={len(log.records)} "
            f"offsets={format_offsets(log.records)} "
            f"high_watermark={log.high_watermark}"
        ),
        f"   history: {format_records(log.records)}",
    ]

    first = search.poll(log, max_records=args.batch_size)
    lines.append(
        (
            f"02 consumer poll: name={first.consumer} "
            f"read_offsets={format_offsets(first.records)} "
            f"start_offset={first.start_offset} next_offset={first.next_offset} "
            f"lag={first.lag} projection={format_projection(search.projection)}"
        )
    )

    tent_history = tuple(record for record in log.records if record.key == "item:tent")
    lines.append(
        (
            f"03 append-only key history: key=item:tent "
            f"versions={format_records(tent_history)}"
        )
    )

    compacted = log.compact_latest()
    lines.append(
        (
            f"04 latest-value compaction: before={compacted.before_count} "
            f"after={compacted.after_count} removed={compacted.removed_count} "
            f"kept_offsets={format_offsets(compacted.records)} "
            f"latest={format_projection(compacted.live_values)} "
            f"tombstones={','.join(compacted.tombstone_keys) or 'none'}"
        )
    )

    retained = log.retain_last(args.retention_records)
    lines.append(
        (
            f"05 retention: retain_last={args.retention_records} "
            f"removed_offsets={format_offsets(retained.removed_records)} "
            f"earliest_offset={log.earliest_offset} "
            f"retained_offsets={format_offsets(retained.retained_records)}"
        )
    )

    try:
        second = search.poll(log, max_records=args.batch_size)
        lines.append(
            (
                f"06 consumer catch-up: name={second.consumer} "
                f"read_offsets={format_offsets(second.records)} "
                f"next_offset={second.next_offset} lag={second.lag} "
                f"projection={format_projection(search.projection)}"
            )
        )
    except OffsetOutOfRange as exc:
        lines.append(
            (
                f"06 consumer catch-up gap: name={search.name} "
                f"requested_offset={search.next_offset} "
                f"earliest_offset={log.earliest_offset} action=load_compacted_snapshot "
                f"message={exc}"
            )
        )
        search.projection = dict(compacted.live_values)
        search.next_offset = log.high_watermark
        lines.append(
            (
                f"06b snapshot recovery: name={search.name} "
                f"next_offset={search.next_offset} lag=0 "
                f"projection={format_projection(search.projection)}"
            )
        )

    slow = Consumer("analytics-backfill")
    try:
        slow.poll(log, max_records=args.batch_size)
    except OffsetOutOfRange as exc:
        lines.append(
            (
                f"07 retention gap: consumer={slow.name} "
                f"requested_offset={slow.next_offset} "
                f"earliest_offset={log.earliest_offset} action=rebuild_or_snapshot "
                f"message={exc}"
            )
        )

    final = search.poll(log, max_records=args.batch_size)
    lines.append(
        (
            f"08 final consumer poll: name={final.consumer} "
            f"read_offsets={format_offsets(final.records)} "
            f"next_offset={final.next_offset} lag={final.lag} "
            f"projection={format_projection(search.projection)}"
        )
    )
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
