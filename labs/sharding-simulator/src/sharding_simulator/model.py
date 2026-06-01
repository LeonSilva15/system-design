"""Deterministic sharding model used by the lab."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Protocol


@dataclass(frozen=True)
class Record:
    record_id: str
    tenant_id: str
    day: int
    value: str


@dataclass(frozen=True)
class QueryResult:
    query: str
    shards_touched: tuple[str, ...]
    records: tuple[Record, ...]
    note: str


@dataclass(frozen=True)
class ReshardPlan:
    old_shards: int
    new_shards: int
    total_records: int
    moved_records: int

    @property
    def moved_percent(self) -> float:
        if self.total_records == 0:
            return 0.0
        return 100.0 * self.moved_records / self.total_records


class Router(Protocol):
    shard_names: tuple[str, ...]

    def route(self, record: Record) -> str:
        ...

    def route_query(self, *, record_id: str | None, tenant_id: str | None) -> tuple[str, ...]:
        ...


class HashRouter:
    """Hash a stable record field to a shard."""

    def __init__(self, shard_count: int, *, key_field: str = "record_id") -> None:
        if shard_count < 1:
            raise ValueError("shard_count must be at least 1")
        if key_field not in {"record_id", "tenant_id"}:
            raise ValueError("key_field must be record_id or tenant_id")
        self.shard_count = shard_count
        self.key_field = key_field
        self.shard_names = tuple(f"h{i}" for i in range(shard_count))

    def route_key(self, key: str) -> str:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        index = int(digest[:8], 16) % self.shard_count
        return self.shard_names[index]

    def route(self, record: Record) -> str:
        return self.route_key(getattr(record, self.key_field))

    def route_query(
        self,
        *,
        record_id: str | None,
        tenant_id: str | None,
    ) -> tuple[str, ...]:
        if self.key_field == "record_id" and record_id is not None:
            return (self.route_key(record_id),)
        if self.key_field == "tenant_id" and tenant_id is not None:
            return (self.route_key(tenant_id),)
        return self.shard_names


class RangeRouter:
    """Route records by inclusive day ranges."""

    def __init__(self, ranges: list[tuple[str, int, int]]) -> None:
        if not ranges:
            raise ValueError("ranges cannot be empty")
        names = [name for name, _start, _end in ranges]
        if len(set(names)) != len(names):
            raise ValueError("range shard names must be unique")
        ordered = sorted(ranges, key=lambda item: item[1])
        previous_end: int | None = None
        for name, start, end in ordered:
            if start > end:
                raise ValueError(f"range {name} start must be <= end")
            if previous_end is not None and start <= previous_end:
                raise ValueError("ranges must not overlap")
            previous_end = end
        self.ranges = tuple(ranges)
        self.shard_names = tuple(name for name, _start, _end in self.ranges)

    def route_day(self, day: int) -> str:
        for name, start, end in self.ranges:
            if start <= day <= end:
                return name
        raise ValueError(f"day {day} is outside configured ranges")

    def route(self, record: Record) -> str:
        return self.route_day(record.day)

    def route_query(
        self,
        *,
        record_id: str | None,
        tenant_id: str | None,
    ) -> tuple[str, ...]:
        return self.shard_names

    def route_day_range(self, start_day: int, end_day: int) -> tuple[str, ...]:
        if start_day > end_day:
            raise ValueError("start_day must be <= end_day")
        return tuple(
            name
            for name, start, end in self.ranges
            if start <= end_day and end >= start_day
        )


class ShardedStore:
    """A small in-memory store that routes records to named shards."""

    def __init__(self, router: Router) -> None:
        self.router = router
        self.shards: dict[str, list[Record]] = {
            shard_name: [] for shard_name in router.shard_names
        }

    def insert(self, record: Record) -> str:
        shard = self.router.route(record)
        self.shards[shard].append(record)
        return shard

    def insert_many(self, records: list[Record]) -> None:
        for record in records:
            self.insert(record)

    def loads(self) -> dict[str, int]:
        return {name: len(records) for name, records in self.shards.items()}

    def hot_partition(self) -> tuple[str, int, float]:
        loads = self.loads()
        total = sum(loads.values())
        shard, count = max(loads.items(), key=lambda item: (item[1], item[0]))
        share = 0.0 if total == 0 else count / total
        return shard, count, share

    def query_by_record_id(self, record_id: str) -> QueryResult:
        shard_names = self.router.route_query(record_id=record_id, tenant_id=None)
        records = tuple(
            record
            for shard in shard_names
            for record in self.shards[shard]
            if record.record_id == record_id
        )
        note = "direct shard lookup" if len(shard_names) == 1 else "scatter query"
        return QueryResult(
            query=f"record_id={record_id}",
            shards_touched=shard_names,
            records=records,
            note=note,
        )

    def query_by_tenant(self, tenant_id: str) -> QueryResult:
        shard_names = self.router.route_query(record_id=None, tenant_id=tenant_id)
        records = tuple(
            record
            for shard in shard_names
            for record in self.shards[shard]
            if record.tenant_id == tenant_id
        )
        note = "tenant-local lookup" if len(shard_names) == 1 else "cross-shard fanout"
        return QueryResult(
            query=f"tenant_id={tenant_id}",
            shards_touched=shard_names,
            records=records,
            note=note,
        )

    def query_day_range(self, start_day: int, end_day: int) -> QueryResult:
        if isinstance(self.router, RangeRouter):
            shard_names = self.router.route_day_range(start_day, end_day)
        else:
            shard_names = tuple(self.shards.keys())
        records = tuple(
            record
            for shard in shard_names
            for record in self.shards[shard]
            if start_day <= record.day <= end_day
        )
        note = "range router pruned shards"
        if len(shard_names) == len(self.shards):
            note = "range query may fan out unless range routing can prune shards"
        return QueryResult(
            query=f"day between {start_day} and {end_day}",
            shards_touched=shard_names,
            records=records,
            note=note,
        )


def reshard_hash(records: list[Record], old_count: int, new_count: int) -> ReshardPlan:
    old_router = HashRouter(old_count)
    new_router = HashRouter(new_count)
    moved = sum(
        1 for record in records if old_router.route(record) != new_router.route(record)
    )
    return ReshardPlan(
        old_shards=old_count,
        new_shards=new_count,
        total_records=len(records),
        moved_records=moved,
    )
