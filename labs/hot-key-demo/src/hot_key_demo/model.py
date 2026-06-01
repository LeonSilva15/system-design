"""Deterministic hot-key load model used by the lab."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class TrafficEvent:
    key: str
    operation: str = "read"


@dataclass(frozen=True)
class LoadReport:
    key_counts: dict[str, int]
    node_loads: dict[str, int]
    capacity_per_node: int

    @property
    def total_requests(self) -> int:
        return sum(self.key_counts.values())

    @property
    def hot_key(self) -> str:
        return max(self.key_counts, key=lambda key: (self.key_counts[key], key))

    @property
    def hot_key_count(self) -> int:
        return self.key_counts[self.hot_key]

    @property
    def hot_key_share(self) -> float:
        total = self.total_requests
        return 0.0 if total == 0 else self.hot_key_count / total

    @property
    def hottest_node(self) -> str:
        return max(self.node_loads, key=lambda node: (self.node_loads[node], node))

    @property
    def hottest_node_load(self) -> int:
        return self.node_loads[self.hottest_node]

    @property
    def overloaded(self) -> bool:
        return self.hottest_node_load > self.capacity_per_node


@dataclass(frozen=True)
class RefreshReport:
    callers: int
    origin_requests: int
    protected_callers: int
    origin_capacity: int
    strategy: str

    @property
    def overloaded(self) -> bool:
        return self.origin_requests > self.origin_capacity


@dataclass(frozen=True)
class BucketReport:
    bucket_loads: dict[str, int]
    capacity_per_bucket: int

    @property
    def total_writes(self) -> int:
        return sum(self.bucket_loads.values())

    @property
    def max_bucket(self) -> str:
        return max(self.bucket_loads, key=lambda bucket: (self.bucket_loads[bucket], bucket))

    @property
    def max_bucket_load(self) -> int:
        return self.bucket_loads[self.max_bucket]

    @property
    def overloaded(self) -> bool:
        return self.max_bucket_load > self.capacity_per_bucket


def stable_index(value: str, modulo: int) -> int:
    if modulo < 1:
        raise ValueError("modulo must be at least 1")
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % modulo


def make_skewed_traffic(
    *,
    total_requests: int,
    hot_key: str,
    hot_fraction: float,
    normal_key_count: int,
) -> list[TrafficEvent]:
    if total_requests < 1:
        raise ValueError("total_requests must be at least 1")
    if not 0.0 < hot_fraction < 1.0:
        raise ValueError("hot_fraction must be between 0 and 1")
    if normal_key_count < 1:
        raise ValueError("normal_key_count must be at least 1")

    hot_requests = round(total_requests * hot_fraction)
    hot_requests = max(1, min(total_requests - 1, hot_requests))
    normal_requests = total_requests - hot_requests
    events = [TrafficEvent(hot_key) for _ in range(hot_requests)]
    normal_keys = [f"item:{index:03d}" for index in range(normal_key_count)]
    for index in range(normal_requests):
        events.append(TrafficEvent(normal_keys[index % normal_key_count]))
    return events


def analyze_partition_load(
    events: list[TrafficEvent],
    *,
    node_count: int,
    capacity_per_node: int,
    node_prefix: str = "partition",
) -> LoadReport:
    if node_count < 1:
        raise ValueError("node_count must be at least 1")
    if capacity_per_node < 1:
        raise ValueError("capacity_per_node must be at least 1")

    key_counts = dict(Counter(event.key for event in events))
    node_loads = {f"{node_prefix}-{index}": 0 for index in range(node_count)}
    for event in events:
        node_name = f"{node_prefix}-{stable_index(event.key, node_count)}"
        node_loads[node_name] += 1
    return LoadReport(
        key_counts=key_counts,
        node_loads=node_loads,
        capacity_per_node=capacity_per_node,
    )


def replicated_hot_key_load(
    key_counts: dict[str, int],
    *,
    hot_key: str,
    node_count: int,
    replica_count: int,
    capacity_per_node: int,
    node_prefix: str = "cache",
) -> LoadReport:
    if node_count < 1:
        raise ValueError("node_count must be at least 1")
    if replica_count < 1:
        raise ValueError("replica_count must be at least 1")
    if replica_count > node_count:
        raise ValueError("replica_count cannot exceed node_count")
    if capacity_per_node < 1:
        raise ValueError("capacity_per_node must be at least 1")
    if hot_key not in key_counts:
        raise ValueError("hot_key must exist in key_counts")

    node_loads = {f"{node_prefix}-{index}": 0 for index in range(node_count)}
    start = stable_index(hot_key, node_count)
    replica_nodes = [
        f"{node_prefix}-{(start + offset) % node_count}"
        for offset in range(replica_count)
    ]
    for key, count in key_counts.items():
        if key != hot_key:
            node_name = f"{node_prefix}-{stable_index(key, node_count)}"
            node_loads[node_name] += count
            continue

        base = count // replica_count
        remainder = count % replica_count
        for index, node_name in enumerate(replica_nodes):
            node_loads[node_name] += base + (1 if index < remainder else 0)

    return LoadReport(
        key_counts=dict(key_counts),
        node_loads=node_loads,
        capacity_per_node=capacity_per_node,
    )


def simulate_refresh_storm(
    *,
    callers: int,
    origin_capacity: int,
    coalescing: bool,
    fallback_limit: int | None = None,
) -> RefreshReport:
    if callers < 1:
        raise ValueError("callers must be at least 1")
    if origin_capacity < 1:
        raise ValueError("origin_capacity must be at least 1")
    if fallback_limit is not None and fallback_limit < 1:
        raise ValueError("fallback_limit must be at least 1 when provided")

    if coalescing:
        origin_requests = 1
        strategy = "coalesced refresh"
    else:
        origin_requests = callers
        strategy = "every caller refreshes"

    if fallback_limit is not None:
        origin_requests = min(origin_requests, fallback_limit)
        strategy = f"{strategy} with fallback cap"

    return RefreshReport(
        callers=callers,
        origin_requests=origin_requests,
        protected_callers=callers - origin_requests,
        origin_capacity=origin_capacity,
        strategy=strategy,
    )


def bucket_hot_writes(
    *,
    total_writes: int,
    bucket_count: int,
    capacity_per_bucket: int,
    prefix: str = "counter-bucket",
) -> BucketReport:
    if total_writes < 1:
        raise ValueError("total_writes must be at least 1")
    if bucket_count < 1:
        raise ValueError("bucket_count must be at least 1")
    if capacity_per_bucket < 1:
        raise ValueError("capacity_per_bucket must be at least 1")

    bucket_loads = {f"{prefix}-{index}": 0 for index in range(bucket_count)}
    for index in range(total_writes):
        bucket_loads[f"{prefix}-{index % bucket_count}"] += 1
    return BucketReport(
        bucket_loads=bucket_loads,
        capacity_per_bucket=capacity_per_bucket,
    )


def format_loads(loads: dict[str, int]) -> str:
    return ",".join(f"{name}:{count}" for name, count in sorted(loads.items()))


def yes_no(value: bool) -> str:
    return "yes" if value else "no"
