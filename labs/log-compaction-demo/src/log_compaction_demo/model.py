"""Deterministic append-only log and compaction model used by the lab."""

from __future__ import annotations

from dataclasses import dataclass, field


class OffsetOutOfRange(RuntimeError):
    """Raised when a consumer asks for an offset outside retained history."""


@dataclass(frozen=True)
class LogRecord:
    offset: int
    key: str
    value: str | None
    timestamp: int

    @property
    def is_tombstone(self) -> bool:
        return self.value is None

    @property
    def display_value(self) -> str:
        return "<deleted>" if self.value is None else self.value


@dataclass(frozen=True)
class ReadBatch:
    consumer: str
    records: tuple[LogRecord, ...]
    start_offset: int
    next_offset: int
    high_watermark: int

    @property
    def lag(self) -> int:
        return self.high_watermark - self.next_offset


@dataclass(frozen=True)
class CompactionResult:
    before_count: int
    records: tuple[LogRecord, ...]

    @property
    def after_count(self) -> int:
        return len(self.records)

    @property
    def removed_count(self) -> int:
        return self.before_count - self.after_count

    @property
    def live_values(self) -> dict[str, str]:
        return {
            record.key: record.value
            for record in self.records
            if record.value is not None
        }

    @property
    def tombstone_keys(self) -> tuple[str, ...]:
        return tuple(record.key for record in self.records if record.is_tombstone)


@dataclass(frozen=True)
class RetentionResult:
    removed_records: tuple[LogRecord, ...]
    retained_records: tuple[LogRecord, ...]

    @property
    def earliest_offset(self) -> int:
        if self.retained_records:
            return self.retained_records[0].offset
        if self.removed_records:
            return self.removed_records[-1].offset + 1
        return 0


@dataclass
class AppendOnlyLog:
    """A small event log with retained records and monotonically increasing offsets."""

    records: list[LogRecord] = field(default_factory=list)
    _next_offset: int = 0
    _next_timestamp: int = 0

    @property
    def high_watermark(self) -> int:
        return self._next_offset

    @property
    def earliest_offset(self) -> int:
        if self.records:
            return self.records[0].offset
        return self.high_watermark

    def append(self, key: str, value: str | None) -> LogRecord:
        if not key:
            raise ValueError("key cannot be empty")
        record = LogRecord(
            offset=self._next_offset,
            key=key,
            value=value,
            timestamp=self._next_timestamp,
        )
        self.records.append(record)
        self._next_offset += 1
        self._next_timestamp += 1
        return record

    def tombstone(self, key: str) -> LogRecord:
        return self.append(key, None)

    def read_from(self, offset: int, *, max_records: int | None = None) -> tuple[LogRecord, ...]:
        if max_records is not None and max_records < 1:
            raise ValueError("max_records must be at least 1 when provided")
        if offset < self.earliest_offset:
            raise OffsetOutOfRange(
                f"requested offset {offset} is before earliest retained offset {self.earliest_offset}"
            )
        if offset > self.high_watermark:
            raise OffsetOutOfRange(
                f"requested offset {offset} is after high watermark {self.high_watermark}"
            )
        selected = [record for record in self.records if record.offset >= offset]
        if max_records is not None:
            selected = selected[:max_records]
        return tuple(selected)

    def compact_latest(self) -> CompactionResult:
        latest_by_key: dict[str, LogRecord] = {}
        for record in self.records:
            latest_by_key[record.key] = record
        compacted = tuple(
            sorted(latest_by_key.values(), key=lambda record: record.offset)
        )
        return CompactionResult(before_count=len(self.records), records=compacted)

    def retain_last(self, count: int) -> RetentionResult:
        if count < 1:
            raise ValueError("count must be at least 1")
        removed = tuple(self.records[:-count])
        retained = tuple(self.records[-count:])
        self.records = list(retained)
        return RetentionResult(
            removed_records=removed,
            retained_records=retained,
        )


@dataclass
class Consumer:
    name: str
    next_offset: int = 0
    projection: dict[str, str] = field(default_factory=dict)
    processed_offsets: list[int] = field(default_factory=list)

    def poll(self, log: AppendOnlyLog, *, max_records: int) -> ReadBatch:
        records = log.read_from(self.next_offset, max_records=max_records)
        start_offset = self.next_offset
        for record in records:
            self.apply(record)
        if records:
            self.next_offset = records[-1].offset + 1
        return ReadBatch(
            consumer=self.name,
            records=records,
            start_offset=start_offset,
            next_offset=self.next_offset,
            high_watermark=log.high_watermark,
        )

    def apply(self, record: LogRecord) -> None:
        if record.value is None:
            self.projection.pop(record.key, None)
        else:
            self.projection[record.key] = record.value
        self.processed_offsets.append(record.offset)


def format_offsets(records: tuple[LogRecord, ...] | list[LogRecord]) -> str:
    if not records:
        return "none"
    return ",".join(str(record.offset) for record in records)


def format_records(records: tuple[LogRecord, ...] | list[LogRecord]) -> str:
    if not records:
        return "none"
    return ",".join(
        f"{record.offset}:{record.key}={record.display_value}"
        for record in records
    )


def format_projection(values: dict[str, str]) -> str:
    if not values:
        return "empty"
    return ",".join(f"{key}={value}" for key, value in sorted(values.items()))
