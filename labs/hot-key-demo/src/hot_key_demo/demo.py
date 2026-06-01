"""Command-line demo for the hot-key lab."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import (
    analyze_partition_load,
    bucket_hot_writes,
    format_loads,
    make_skewed_traffic,
    replicated_hot_key_load,
    simulate_refresh_storm,
    yes_no,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demonstrate skewed traffic, overloaded hot keys, and mitigation strategies."
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=1000,
        help="Total read requests in the skewed traffic scenario.",
    )
    parser.add_argument(
        "--hot-fraction",
        type=float,
        default=0.62,
        help="Fraction of read requests sent to the hot key.",
    )
    parser.add_argument(
        "--normal-keys",
        type=int,
        default=40,
        help="Number of ordinary keys sharing the remaining traffic.",
    )
    parser.add_argument(
        "--partitions",
        type=int,
        default=6,
        help="Number of partitions or cache owners.",
    )
    parser.add_argument(
        "--capacity",
        type=int,
        default=260,
        help="Capacity per partition or cache owner for this toy model.",
    )
    parser.add_argument(
        "--hot-key",
        default="post:city-marathon",
        help="Name of the hot key.",
    )
    parser.add_argument(
        "--replicas",
        type=int,
        default=4,
        help="Number of cache owners that hold replicas of the hot read key.",
    )
    parser.add_argument(
        "--origin-callers",
        type=int,
        default=80,
        help="Concurrent callers after a hot cache key expires.",
    )
    parser.add_argument(
        "--origin-capacity",
        type=int,
        default=10,
        help="Origin refresh capacity for the expired hot key.",
    )
    parser.add_argument(
        "--hot-writes",
        type=int,
        default=320,
        help="Writes to a single hot counter before bucketing.",
    )
    parser.add_argument(
        "--write-buckets",
        type=int,
        default=8,
        help="Number of buckets for hot counter writes.",
    )
    parser.add_argument(
        "--write-capacity",
        type=int,
        default=80,
        help="Capacity per counter bucket for this toy model.",
    )
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    if args.requests < 2:
        raise SystemExit("--requests must be at least 2")
    if not 0.0 < args.hot_fraction < 1.0:
        raise SystemExit("--hot-fraction must be between 0 and 1")
    if args.normal_keys < 1:
        raise SystemExit("--normal-keys must be at least 1")
    if args.partitions < 1:
        raise SystemExit("--partitions must be at least 1")
    if args.capacity < 1:
        raise SystemExit("--capacity must be at least 1")
    if args.replicas < 1:
        raise SystemExit("--replicas must be at least 1")
    if args.replicas > args.partitions:
        raise SystemExit("--replicas cannot exceed --partitions")
    if args.origin_callers < 1:
        raise SystemExit("--origin-callers must be at least 1")
    if args.origin_capacity < 1:
        raise SystemExit("--origin-capacity must be at least 1")
    if args.hot_writes < 1:
        raise SystemExit("--hot-writes must be at least 1")
    if args.write_buckets < 1:
        raise SystemExit("--write-buckets must be at least 1")
    if args.write_capacity < 1:
        raise SystemExit("--write-capacity must be at least 1")


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    _validate_args(args)

    events = make_skewed_traffic(
        total_requests=args.requests,
        hot_key=args.hot_key,
        hot_fraction=args.hot_fraction,
        normal_key_count=args.normal_keys,
    )
    partition_report = analyze_partition_load(
        events,
        node_count=args.partitions,
        capacity_per_node=args.capacity,
        node_prefix="partition",
    )
    cache_report = analyze_partition_load(
        events,
        node_count=args.partitions,
        capacity_per_node=args.capacity,
        node_prefix="cache",
    )
    replicated_report = replicated_hot_key_load(
        partition_report.key_counts,
        hot_key=partition_report.hot_key,
        node_count=args.partitions,
        replica_count=args.replicas,
        capacity_per_node=args.capacity,
        node_prefix="cache",
    )
    refresh_without = simulate_refresh_storm(
        callers=args.origin_callers,
        origin_capacity=args.origin_capacity,
        coalescing=False,
    )
    refresh_with = simulate_refresh_storm(
        callers=args.origin_callers,
        origin_capacity=args.origin_capacity,
        coalescing=True,
        fallback_limit=args.origin_capacity,
    )
    unbucketed = bucket_hot_writes(
        total_writes=args.hot_writes,
        bucket_count=1,
        capacity_per_bucket=args.write_capacity,
    )
    bucketed = bucket_hot_writes(
        total_writes=args.hot_writes,
        bucket_count=args.write_buckets,
        capacity_per_bucket=args.write_capacity,
    )

    normal_requests = args.requests - partition_report.hot_key_count
    lines = [
        (
            f"config requests={args.requests} hot_fraction={args.hot_fraction:.2f} "
            f"partitions={args.partitions} capacity={args.capacity}"
        ),
        (
            f"01 skewed traffic: hot_key={partition_report.hot_key} "
            f"hot_key_requests={partition_report.hot_key_count} "
            f"share={partition_report.hot_key_share:.2f} "
            f"normal_requests={normal_requests} normal_keys={args.normal_keys}"
        ),
        (
            f"02 overloaded partition: node={partition_report.hottest_node} "
            f"load={partition_report.hottest_node_load} capacity={args.capacity} "
            f"overloaded={yes_no(partition_report.overloaded)} "
            f"loads={format_loads(partition_report.node_loads)}"
        ),
        (
            f"03 overloaded cache key owner: owner={cache_report.hottest_node} "
            f"load={cache_report.hottest_node_load} capacity={args.capacity} "
            f"overloaded={yes_no(cache_report.overloaded)} "
            f"loads={format_loads(cache_report.node_loads)}"
        ),
        (
            f"04 mitigation read replication: replicas={args.replicas} "
            f"max_owner={replicated_report.hottest_node} "
            f"max_load={replicated_report.hottest_node_load} "
            f"overloaded={yes_no(replicated_report.overloaded)} "
            f"loads={format_loads(replicated_report.node_loads)}"
        ),
        (
            f"05 mitigation request coalescing: callers={args.origin_callers} "
            f"origin_without={refresh_without.origin_requests} "
            f"overloaded_without={yes_no(refresh_without.overloaded)} "
            f"origin_with={refresh_with.origin_requests} "
            f"protected_callers={refresh_with.protected_callers} "
            f"overloaded_with={yes_no(refresh_with.overloaded)}"
        ),
        (
            f"06 mitigation bucketed writes: single_counter_max={unbucketed.max_bucket_load} "
            f"single_overloaded={yes_no(unbucketed.overloaded)} "
            f"buckets={args.write_buckets} bucketed_max={bucketed.max_bucket_load} "
            f"bucketed_overloaded={yes_no(bucketed.overloaded)}"
        ),
        (
            "07 mitigation strategies: replicate hot reads, coalesce refreshes, "
            "cap origin fallback, serve stale when safe, bucket approximate writes"
        ),
    ]
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
