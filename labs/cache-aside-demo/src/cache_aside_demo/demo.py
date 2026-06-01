"""Command-line demo for the cache-aside lab."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import (
    CacheAsideCatalog,
    CatalogRecord,
    ManualClock,
    ReadResult,
    SourceDatabase,
    TTLCache,
)


DEFAULT_KEY = "class:composting-101"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demonstrate cache-aside hits, misses, TTL, staleness, and fallback."
    )
    parser.add_argument(
        "--ttl",
        type=float,
        default=5.0,
        help="Seconds a cached value remains fresh.",
    )
    parser.add_argument(
        "--initial-seats",
        type=int,
        default=12,
        help="Initial source value for the example class.",
    )
    parser.add_argument(
        "--updated-seats",
        type=int,
        default=2,
        help="Source value written while the cache is still fresh.",
    )
    parser.add_argument(
        "--final-seats",
        type=int,
        default=1,
        help="Source value written before targeted invalidation.",
    )
    parser.add_argument(
        "--no-stale-if-error",
        action="store_true",
        help="Disable serving an expired cached value when the database is down.",
    )
    return parser


def format_result(step: str, read: ReadResult) -> str:
    value = read.value
    fallback_stale = "yes" if read.stale else "no"
    return (
        f"{step}: t={read.now:.1f}s "
        f"source={read.source} cache={read.cache_event} "
        f"value=seats:{value.available_seats} version:{value.version} "
        f"fallback_stale={fallback_stale} "
        f"db_reads={read.database_reads} note={read.note}"
    )


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    clock = ManualClock()
    database = SourceDatabase(
        {
            DEFAULT_KEY: CatalogRecord(
                key=DEFAULT_KEY,
                title="Composting 101",
                available_seats=args.initial_seats,
                version=1,
            )
        }
    )
    cache = TTLCache(ttl_seconds=args.ttl)
    catalog = CacheAsideCatalog(
        database=database,
        cache=cache,
        clock=clock,
        stale_if_error=not args.no_stale_if_error,
    )

    lines = [
        (
            f"config ttl={args.ttl:.1f}s "
            f"initial_seats={args.initial_seats} "
            f"updated_seats={args.updated_seats} "
            f"final_seats={args.final_seats}"
        )
    ]

    lines.append(format_result("01 miss fills cache", catalog.get_class(DEFAULT_KEY)))

    clock.advance(1.0)
    lines.append(format_result("02 hit reuses cache", catalog.get_class(DEFAULT_KEY)))

    clock.advance(1.0)
    updated = catalog.update_database_seats(DEFAULT_KEY, args.updated_seats)
    lines.append(
        (
            "03 source changes without invalidation: "
            f"database=seats:{updated.available_seats} version:{updated.version}"
        )
    )
    lines.append(
        format_result("04 stale until ttl or invalidation", catalog.get_class(DEFAULT_KEY))
    )

    clock.advance(args.ttl)
    lines.append(
        format_result("05 ttl expiry refreshes", catalog.get_class(DEFAULT_KEY))
    )

    clock.advance(1.0)
    final = catalog.update_database_seats(DEFAULT_KEY, args.final_seats)
    invalidated = catalog.invalidate(DEFAULT_KEY)
    lines.append(
        (
            "06 source changes with invalidation: "
            f"database=seats:{final.available_seats} version:{final.version} "
            f"invalidated={invalidated}"
        )
    )
    lines.append(format_result("07 invalidation forces miss", catalog.get_class(DEFAULT_KEY)))

    clock.advance(1.0)
    cache.available = False
    lines.append(
        format_result("08 cache outage uses database", catalog.get_class(DEFAULT_KEY))
    )

    cache.available = True
    clock.advance(args.ttl)
    database.available = False
    try:
        stale_result = catalog.get_class(DEFAULT_KEY)
    except Exception as exc:  # pragma: no cover - only used for CLI display.
        lines.append(f"09 database outage: error={type(exc).__name__} {exc}")
    else:
        lines.append(format_result("09 database outage uses stale", stale_result))

    lines.append(
        (
            "summary "
            f"cache_hits={cache.hits} cache_misses={cache.misses} "
            f"cache_expired={cache.expired} cache_writes={cache.writes} "
            f"invalidations={cache.invalidations} db_reads={database.read_count}"
        )
    )
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
