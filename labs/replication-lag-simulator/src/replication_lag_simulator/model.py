"""Small deterministic leader/follower replication model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    key: str
    value: str
    version: int
    written_at: float


@dataclass(frozen=True)
class ReplicationEvent:
    key: str
    record: Record
    apply_at: float


@dataclass(frozen=True)
class ReadResult:
    key: str
    source: str
    value: str | None
    version: int
    leader_version: int
    stale: bool
    read_your_writes_ok: bool
    note: str


@dataclass(frozen=True)
class ReplicationStatus:
    key: str
    leader_version: int
    follower_version: int
    versions_behind: int
    pending_events: int
    seconds_until_next_apply: float | None


class ManualClock:
    """A controlled clock so replication lag tests do not sleep."""

    def __init__(self, now: float = 0.0) -> None:
        self._now = now

    @property
    def now(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("cannot move time backwards")
        self._now += seconds


class LeaderFollowerStore:
    """One write leader, one lagging follower, and scheduled replication."""

    def __init__(self, clock: ManualClock, *, replication_delay: float = 5.0) -> None:
        if replication_delay < 0:
            raise ValueError("replication_delay cannot be negative")
        self.clock = clock
        self.replication_delay = replication_delay
        self.leader: dict[str, Record] = {}
        self.follower: dict[str, Record] = {}
        self.pending: list[ReplicationEvent] = []
        self._next_version: dict[str, int] = {}

    def write(self, key: str, value: str) -> Record:
        version = self._next_version.get(key, 0) + 1
        self._next_version[key] = version
        record = Record(
            key=key,
            value=value,
            version=version,
            written_at=self.clock.now,
        )
        self.leader[key] = record
        self.pending.append(
            ReplicationEvent(
                key=key,
                record=record,
                apply_at=self.clock.now + self.replication_delay,
            )
        )
        self.pending.sort(key=lambda event: (event.apply_at, event.record.version))
        return record

    def apply_replication(self) -> list[Record]:
        applied: list[Record] = []
        remaining: list[ReplicationEvent] = []
        for event in self.pending:
            if event.apply_at <= self.clock.now:
                current = self.follower.get(event.key)
                if current is None or event.record.version >= current.version:
                    self.follower[event.key] = event.record
                    applied.append(event.record)
            else:
                remaining.append(event)
        self.pending = remaining
        return applied

    def read_leader(self, key: str, *, min_version: int = 0) -> ReadResult:
        record = self.leader.get(key)
        version = record.version if record else 0
        return ReadResult(
            key=key,
            source="leader",
            value=record.value if record else None,
            version=version,
            leader_version=version,
            stale=False,
            read_your_writes_ok=version >= min_version,
            note="authoritative read",
        )

    def read_follower(self, key: str, *, min_version: int = 0) -> ReadResult:
        self.apply_replication()
        leader_record = self.leader.get(key)
        follower_record = self.follower.get(key)
        leader_version = leader_record.version if leader_record else 0
        follower_version = follower_record.version if follower_record else 0
        stale = follower_version < leader_version
        read_your_writes_ok = follower_version >= min_version

        note = "follower is caught up"
        if stale and follower_version == 0:
            note = "follower has not applied the write yet"
        elif stale:
            note = "follower is behind the leader"
        if min_version and not read_your_writes_ok:
            note = "read-your-writes violation on follower"

        return ReadResult(
            key=key,
            source="follower",
            value=follower_record.value if follower_record else None,
            version=follower_version,
            leader_version=leader_version,
            stale=stale,
            read_your_writes_ok=read_your_writes_ok,
            note=note,
        )

    def read_with_min_version(self, key: str, *, min_version: int) -> ReadResult:
        follower_result = self.read_follower(key, min_version=min_version)
        if follower_result.read_your_writes_ok:
            return follower_result
        leader_result = self.read_leader(key, min_version=min_version)
        return ReadResult(
            key=leader_result.key,
            source="leader_fallback",
            value=leader_result.value,
            version=leader_result.version,
            leader_version=leader_result.leader_version,
            stale=False,
            read_your_writes_ok=leader_result.read_your_writes_ok,
            note="follower lag exceeded minimum version; routed to leader",
        )

    def status(self, key: str) -> ReplicationStatus:
        self.apply_replication()
        leader_record = self.leader.get(key)
        follower_record = self.follower.get(key)
        leader_version = leader_record.version if leader_record else 0
        follower_version = follower_record.version if follower_record else 0
        key_events = [event for event in self.pending if event.key == key]
        seconds_until_next_apply = None
        if key_events:
            seconds_until_next_apply = max(0.0, key_events[0].apply_at - self.clock.now)
        return ReplicationStatus(
            key=key,
            leader_version=leader_version,
            follower_version=follower_version,
            versions_behind=leader_version - follower_version,
            pending_events=len(key_events),
            seconds_until_next_apply=seconds_until_next_apply,
        )
