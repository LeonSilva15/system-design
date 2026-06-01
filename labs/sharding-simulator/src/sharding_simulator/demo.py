"""Command-line demo for the sharding simulator."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import HashRouter, RangeRouter, Record, ShardedStore, reshard_hash


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demonstrate hash sharding, range sharding, resharding, hot partitions, and cross-shard queries."
    )
    parser.add_argument(
        "--records",
        type=int,
        default=18,
        help="Number of normal records for hash sharding.",
    )
    parser.add_argument(
        "--shards",
        type=int,
        default=3,
        help="Number of hash shards in the first layout.",
    )
    parser.add_argument(
        "--new-shards",
        type=int,
        default=4,
        help="Number of hash shards after resharding.",
    )
    parser.add_argument(
        "--hot-writes",
        type=int,
        default=12,
        help="Number of current-day writes for the range-sharding hot partition scenario.",
    )
    return parser


def make_records(count: int) -> list[Record]:
    tenants = ["clinic", "library", "garden", "youth"]
    return [
        Record(
            record_id=f"request-{i:03d}",
            tenant_id=tenants[i % len(tenants)],
            day=1 + (i % 90),
            value=f"task-{i:03d}",
        )
        for i in range(count)
    ]


def format_loads(loads: dict[str, int]) -> str:
    return ",".join(f"{name}:{count}" for name, count in sorted(loads.items()))


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    if args.records < 1:
        raise SystemExit("--records must be at least 1")
    if args.shards < 1 or args.new_shards < 1:
        raise SystemExit("--shards and --new-shards must be at least 1")
    if args.hot_writes < 2:
        raise SystemExit("--hot-writes must be at least 2 for this demo")

    records = make_records(args.records)
    hash_store = ShardedStore(HashRouter(args.shards, key_field="record_id"))
    hash_store.insert_many(records)
    hot_shard, hot_count, hot_share = hash_store.hot_partition()
    lines = [
        (
            f"config records={args.records} shards={args.shards} "
            f"new_shards={args.new_shards} hot_writes={args.hot_writes}"
        ),
        f"01 hash sharding loads: {format_loads(hash_store.loads())}",
        (
            f"02 hash hottest shard: shard={hot_shard} count={hot_count} "
            f"share={hot_share:.2f}"
        ),
    ]

    direct = hash_store.query_by_record_id(records[0].record_id)
    tenant = hash_store.query_by_tenant("clinic")
    lines.append(
        (
            f"03 direct lookup: query={direct.query} "
            f"shards={len(direct.shards_touched)} note={direct.note}"
        )
    )
    lines.append(
        (
            f"04 tenant query on record-id hash: records={len(tenant.records)} "
            f"shards={len(tenant.shards_touched)} note={tenant.note}"
        )
    )

    plan = reshard_hash(records, args.shards, args.new_shards)
    lines.append(
        (
            f"05 reshard hash {plan.old_shards}->{plan.new_shards}: "
            f"moved={plan.moved_records}/{plan.total_records} "
            f"moved_percent={plan.moved_percent:.1f}"
        )
    )
    lines.append("   note reshard estimate uses simple modulo hashing")

    range_store = ShardedStore(
        RangeRouter(
            [
                ("old", 1, 30),
                ("recent", 31, 60),
                ("current", 61, 120),
            ]
        )
    )
    current_records = [
        Record(
            record_id=f"current-{i:03d}",
            tenant_id="clinic",
            day=90,
            value=f"current-task-{i:03d}",
        )
        for i in range(args.hot_writes)
    ]
    mixed_records = [
        Record("old-001", "library", 10, "archived-task"),
        Record("recent-001", "garden", 45, "recent-task"),
    ]
    range_store.insert_many(current_records + mixed_records)
    range_hot_shard, range_hot_count, range_hot_share = range_store.hot_partition()
    lines.append(f"06 range sharding loads: {format_loads(range_store.loads())}")
    lines.append(
        (
            f"07 range hot partition: shard={range_hot_shard} "
            f"count={range_hot_count} share={range_hot_share:.2f}"
        )
    )
    day_query = range_store.query_day_range(1, 120)
    lines.append(
        (
            f"08 cross-shard range report: records={len(day_query.records)} "
            f"shards={len(day_query.shards_touched)} note={day_query.note}"
        )
    )
    narrow = range_store.query_day_range(31, 60)
    lines.append(
        (
            f"09 narrow range query: records={len(narrow.records)} "
            f"shards={len(narrow.shards_touched)} note={narrow.note}"
        )
    )
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
