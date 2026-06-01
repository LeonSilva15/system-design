"""Small deterministic cache-aside model used by the lab."""

from __future__ import annotations

from dataclasses import dataclass


class CacheUnavailable(RuntimeError):
    """Raised when the cache cannot serve reads or writes."""


class DatabaseUnavailable(RuntimeError):
    """Raised when the source database cannot serve reads."""


@dataclass(frozen=True)
class CatalogRecord:
    """A tiny source record that is safe to cache for a bounded window."""

    key: str
    title: str
    available_seats: int
    version: int


@dataclass(frozen=True)
class CacheEntry:
    value: CatalogRecord
    cached_at: float
    expires_at: float

    def is_fresh(self, now: float) -> bool:
        return now < self.expires_at


@dataclass(frozen=True)
class CacheLookup:
    event: str
    value: CatalogRecord | None = None
    expired_entry: CacheEntry | None = None


@dataclass(frozen=True)
class ReadResult:
    key: str
    value: CatalogRecord
    source: str
    cache_event: str
    now: float
    stale: bool
    database_reads: int
    note: str


class ManualClock:
    """A controlled clock so TTL behavior is deterministic in tests."""

    def __init__(self, now: float = 0.0) -> None:
        self._now = now

    @property
    def now(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("cannot move time backwards")
        self._now += seconds


class SourceDatabase:
    """In-memory source of truth for catalog records."""

    def __init__(self, records: dict[str, CatalogRecord]) -> None:
        self._records = dict(records)
        self.available = True
        self.read_count = 0
        self.write_count = 0

    def read(self, key: str) -> CatalogRecord:
        if not self.available:
            raise DatabaseUnavailable("source database is unavailable")
        self.read_count += 1
        return self._records[key]

    def update_seats(self, key: str, available_seats: int) -> CatalogRecord:
        current = self._records[key]
        updated = CatalogRecord(
            key=current.key,
            title=current.title,
            available_seats=available_seats,
            version=current.version + 1,
        )
        self._records[key] = updated
        self.write_count += 1
        return updated

    def peek(self, key: str) -> CatalogRecord:
        return self._records[key]


class TTLCache:
    """A minimal TTL cache with injectable failure for learning scenarios."""

    def __init__(self, ttl_seconds: float) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.ttl_seconds = ttl_seconds
        self.available = True
        self.entries: dict[str, CacheEntry] = {}
        self.hits = 0
        self.misses = 0
        self.expired = 0
        self.writes = 0
        self.invalidations = 0

    def get(self, key: str, now: float) -> CacheLookup:
        if not self.available:
            raise CacheUnavailable("cache is unavailable")

        entry = self.entries.get(key)
        if entry is None:
            self.misses += 1
            return CacheLookup(event="miss")

        if not entry.is_fresh(now):
            self.expired += 1
            return CacheLookup(event="expired", expired_entry=entry)

        self.hits += 1
        return CacheLookup(event="hit", value=entry.value)

    def set(self, key: str, value: CatalogRecord, now: float) -> None:
        if not self.available:
            raise CacheUnavailable("cache is unavailable")
        self.entries[key] = CacheEntry(
            value=value,
            cached_at=now,
            expires_at=now + self.ttl_seconds,
        )
        self.writes += 1

    def delete(self, key: str) -> bool:
        if not self.available:
            raise CacheUnavailable("cache is unavailable")
        existed = key in self.entries
        self.entries.pop(key, None)
        if existed:
            self.invalidations += 1
        return existed


class CacheAsideCatalog:
    """Read-through application logic using the cache-aside pattern."""

    def __init__(
        self,
        database: SourceDatabase,
        cache: TTLCache,
        clock: ManualClock,
        *,
        stale_if_error: bool = True,
    ) -> None:
        self.database = database
        self.cache = cache
        self.clock = clock
        self.stale_if_error = stale_if_error

    def get_class(self, key: str) -> ReadResult:
        now = self.clock.now

        try:
            lookup = self.cache.get(key, now)
        except CacheUnavailable:
            value = self.database.read(key)
            return ReadResult(
                key=key,
                value=value,
                source="database_cache_unavailable",
                cache_event="cache_unavailable",
                now=now,
                stale=False,
                database_reads=self.database.read_count,
                note="cache failed open to the source database",
            )

        if lookup.event == "hit" and lookup.value is not None:
            return ReadResult(
                key=key,
                value=lookup.value,
                source="cache",
                cache_event="hit",
                now=now,
                stale=False,
                database_reads=self.database.read_count,
                note="fresh cached value reused",
            )

        try:
            value = self.database.read(key)
        except DatabaseUnavailable:
            if self.stale_if_error and lookup.expired_entry is not None:
                return ReadResult(
                    key=key,
                    value=lookup.expired_entry.value,
                    source="stale_cache_database_unavailable",
                    cache_event="expired",
                    now=now,
                    stale=True,
                    database_reads=self.database.read_count,
                    note="expired value served because the source was down",
                )
            raise

        self.cache.set(key, value, now)
        source = "database_miss_fill"
        note = "cache miss read from source and filled cache"
        if lookup.event == "expired":
            source = "database_refresh_after_ttl"
            note = "expired cache entry refreshed from source"

        return ReadResult(
            key=key,
            value=value,
            source=source,
            cache_event=lookup.event,
            now=now,
            stale=False,
            database_reads=self.database.read_count,
            note=note,
        )

    def update_database_seats(self, key: str, available_seats: int) -> CatalogRecord:
        return self.database.update_seats(key, available_seats)

    def invalidate(self, key: str) -> bool:
        return self.cache.delete(key)
