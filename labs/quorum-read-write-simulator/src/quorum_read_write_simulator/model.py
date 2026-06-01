"""Small deterministic quorum read/write simulator."""

from __future__ import annotations

from dataclasses import dataclass


class QuorumUnavailable(RuntimeError):
    """Raised when not enough replicas can answer an operation."""


@dataclass(frozen=True)
class ValueVersion:
    value: str
    version: int


@dataclass
class Replica:
    name: str
    latency_ms: int
    value: str = "empty"
    version: int = 0
    available: bool = True

    def current(self) -> ValueVersion:
        return ValueVersion(value=self.value, version=self.version)

    def write(self, value: str, version: int) -> ValueVersion:
        if version >= self.version:
            self.value = value
            self.version = version
        return self.current()


@dataclass(frozen=True)
class Response:
    replica: str
    latency_ms: int
    value: str
    version: int


@dataclass(frozen=True)
class OperationResult:
    operation: str
    quorum: int
    available: int
    successful: int
    latency_ms: int
    value: str | None
    version: int | None
    stale: bool
    responses: tuple[Response, ...]
    note: str


class Cluster:
    """Replicated single-key register with configurable read/write quorums."""

    def __init__(self, replicas: list[Replica]) -> None:
        if not replicas:
            raise ValueError("cluster must include at least one replica")
        self.replicas = replicas
        self._next_version = max(replica.version for replica in replicas) + 1

    @classmethod
    def with_latencies(cls, latencies_ms: list[int]) -> "Cluster":
        replicas = [
            Replica(name=f"r{i + 1}", latency_ms=latency)
            for i, latency in enumerate(latencies_ms)
        ]
        return cls(replicas)

    @property
    def size(self) -> int:
        return len(self.replicas)

    @property
    def latest_version(self) -> int:
        return max(replica.version for replica in self.replicas)

    @property
    def latest_value(self) -> str:
        latest = max(self.replicas, key=lambda replica: replica.version)
        return latest.value

    def set_unavailable(self, names: set[str]) -> None:
        for replica in self.replicas:
            replica.available = replica.name not in names

    def seed_replica(self, name: str, value: str, version: int) -> None:
        replica = self._replica(name)
        replica.value = value
        replica.version = version
        self._next_version = max(self._next_version, version + 1)

    def write(self, value: str, *, write_quorum: int) -> OperationResult:
        self._validate_quorum(write_quorum)
        candidates = self._available_by_latency()
        if len(candidates) < write_quorum:
            raise QuorumUnavailable(
                f"write quorum {write_quorum} needs {write_quorum} available replicas"
            )

        version = self._next_version
        self._next_version += 1
        acknowledgements = candidates[:write_quorum]
        responses = [
            Response(
                replica=replica.name,
                latency_ms=replica.latency_ms,
                value=replica.write(value, version).value,
                version=replica.version,
            )
            for replica in acknowledgements
        ]
        return OperationResult(
            operation="write",
            quorum=write_quorum,
            available=len(candidates),
            successful=len(responses),
            latency_ms=max(response.latency_ms for response in responses),
            value=value,
            version=version,
            stale=False,
            responses=tuple(responses),
            note="write committed after fastest quorum acknowledgements",
        )

    def read(self, *, read_quorum: int) -> OperationResult:
        self._validate_quorum(read_quorum)
        candidates = self._available_by_latency()
        if len(candidates) < read_quorum:
            raise QuorumUnavailable(
                f"read quorum {read_quorum} needs {read_quorum} available replicas"
            )

        responders = candidates[:read_quorum]
        responses = [
            Response(
                replica=replica.name,
                latency_ms=replica.latency_ms,
                value=replica.value,
                version=replica.version,
            )
            for replica in responders
        ]
        chosen = max(responses, key=lambda response: response.version)
        latest_version = self.latest_version
        stale = chosen.version < latest_version
        note = "read quorum returned latest observed version"
        if stale:
            note = "read quorum missed newer version on another replica"
        return OperationResult(
            operation="read",
            quorum=read_quorum,
            available=len(candidates),
            successful=len(responses),
            latency_ms=max(response.latency_ms for response in responses),
            value=chosen.value,
            version=chosen.version,
            stale=stale,
            responses=tuple(responses),
            note=note,
        )

    def repair(self, responses: tuple[Response, ...]) -> list[str]:
        if not responses:
            return []
        latest = max(responses, key=lambda response: response.version)
        repaired: list[str] = []
        for response in responses:
            if response.version < latest.version:
                replica = self._replica(response.replica)
                replica.write(latest.value, latest.version)
                repaired.append(replica.name)
        return repaired

    def state_lines(self) -> list[str]:
        return [
            (
                f"{replica.name}:value={replica.value} "
                f"version={replica.version} available={replica.available} "
                f"latency_ms={replica.latency_ms}"
            )
            for replica in self.replicas
        ]

    def _available_by_latency(self) -> list[Replica]:
        return sorted(
            [replica for replica in self.replicas if replica.available],
            key=lambda replica: (replica.latency_ms, replica.name),
        )

    def _replica(self, name: str) -> Replica:
        for replica in self.replicas:
            if replica.name == name:
                return replica
        raise KeyError(name)

    def _validate_quorum(self, quorum: int) -> None:
        if quorum < 1:
            raise ValueError("quorum must be at least 1")
        if quorum > self.size:
            raise ValueError("quorum cannot exceed cluster size")
