from __future__ import annotations

import unittest

from cache_aside_demo import (
    CacheAsideCatalog,
    CatalogRecord,
    DatabaseUnavailable,
    ManualClock,
    SourceDatabase,
    TTLCache,
)
from cache_aside_demo.demo import run_demo


KEY = "class:composting-101"


def build_catalog(*, ttl: float = 5.0, stale_if_error: bool = True) -> CacheAsideCatalog:
    clock = ManualClock()
    database = SourceDatabase(
        {
            KEY: CatalogRecord(
                key=KEY,
                title="Composting 101",
                available_seats=12,
                version=1,
            )
        }
    )
    cache = TTLCache(ttl_seconds=ttl)
    return CacheAsideCatalog(
        database=database,
        cache=cache,
        clock=clock,
        stale_if_error=stale_if_error,
    )


class CacheAsideTests(unittest.TestCase):
    def test_cache_miss_fills_cache_and_next_read_hits(self) -> None:
        catalog = build_catalog()

        first = catalog.get_class(KEY)
        second = catalog.get_class(KEY)

        self.assertEqual(first.source, "database_miss_fill")
        self.assertEqual(first.cache_event, "miss")
        self.assertEqual(second.source, "cache")
        self.assertEqual(second.cache_event, "hit")
        self.assertEqual(second.value, first.value)
        self.assertEqual(catalog.database.read_count, 1)
        self.assertEqual(catalog.cache.hits, 1)

    def test_source_change_is_stale_until_ttl_expires(self) -> None:
        catalog = build_catalog(ttl=5.0)
        catalog.get_class(KEY)

        catalog.clock.advance(1.0)
        catalog.update_database_seats(KEY, available_seats=2)
        stale_read = catalog.get_class(KEY)

        catalog.clock.advance(5.0)
        refreshed = catalog.get_class(KEY)

        self.assertEqual(stale_read.source, "cache")
        self.assertEqual(stale_read.value.available_seats, 12)
        self.assertEqual(stale_read.value.version, 1)
        self.assertEqual(refreshed.source, "database_refresh_after_ttl")
        self.assertEqual(refreshed.cache_event, "expired")
        self.assertEqual(refreshed.value.available_seats, 2)
        self.assertEqual(refreshed.value.version, 2)

    def test_invalidation_forces_fresh_read_before_ttl(self) -> None:
        catalog = build_catalog(ttl=60.0)
        catalog.get_class(KEY)

        catalog.clock.advance(1.0)
        catalog.update_database_seats(KEY, available_seats=3)
        invalidated = catalog.invalidate(KEY)
        read_after_invalidation = catalog.get_class(KEY)

        self.assertIs(invalidated, True)
        self.assertEqual(read_after_invalidation.source, "database_miss_fill")
        self.assertEqual(read_after_invalidation.cache_event, "miss")
        self.assertEqual(read_after_invalidation.value.available_seats, 3)
        self.assertEqual(read_after_invalidation.value.version, 2)

    def test_cache_unavailable_falls_back_to_database(self) -> None:
        catalog = build_catalog()
        catalog.cache.available = False

        result = catalog.get_class(KEY)

        self.assertEqual(result.source, "database_cache_unavailable")
        self.assertEqual(result.cache_event, "cache_unavailable")
        self.assertEqual(result.value.available_seats, 12)
        self.assertIs(result.stale, False)
        self.assertEqual(catalog.database.read_count, 1)

    def test_expired_value_can_be_served_when_database_is_down(self) -> None:
        catalog = build_catalog(ttl=2.0, stale_if_error=True)
        catalog.get_class(KEY)

        catalog.clock.advance(3.0)
        catalog.database.available = False
        result = catalog.get_class(KEY)

        self.assertEqual(result.source, "stale_cache_database_unavailable")
        self.assertEqual(result.cache_event, "expired")
        self.assertEqual(result.value.version, 1)
        self.assertIs(result.stale, True)

    def test_database_down_after_expiry_can_fail_closed_without_stale_fallback(
        self,
    ) -> None:
        catalog = build_catalog(ttl=2.0, stale_if_error=False)
        catalog.get_class(KEY)

        catalog.clock.advance(3.0)
        catalog.database.available = False

        with self.assertRaises(DatabaseUnavailable):
            catalog.get_class(KEY)

    def test_demo_no_stale_if_error_prints_database_outage_error(self) -> None:
        lines = run_demo(["--no-stale-if-error"])

        self.assertTrue(
            any("09 database outage: error=DatabaseUnavailable" in line for line in lines)
        )
        self.assertTrue(any(line.startswith("summary ") for line in lines))


if __name__ == "__main__":
    unittest.main()
