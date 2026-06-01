"""Command-line demo for the quorum read/write simulator."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .model import Cluster, OperationResult, QuorumUnavailable


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demonstrate read/write quorums, unavailable replicas, stale reads, and latency trade-offs."
    )
    parser.add_argument(
        "--replicas",
        type=int,
        default=3,
        help="Number of replicas in the toy cluster.",
    )
    parser.add_argument(
        "--read-quorum",
        type=int,
        default=2,
        help="Replica responses required for a read.",
    )
    parser.add_argument(
        "--write-quorum",
        type=int,
        default=2,
        help="Replica acknowledgements required for a write.",
    )
    parser.add_argument(
        "--latencies",
        default="12,35,80",
        help="Comma-separated replica latencies in milliseconds.",
    )
    return parser


def parse_latencies(value: str, replicas: int) -> list[int]:
    latencies = [int(part.strip()) for part in value.split(",") if part.strip()]
    if len(latencies) != replicas:
        raise SystemExit("--latencies must provide one value per replica")
    if any(latency < 0 for latency in latencies):
        raise SystemExit("--latencies cannot contain negative values")
    return latencies


def format_result(label: str, result: OperationResult) -> str:
    stale = "yes" if result.stale else "no"
    responses = ",".join(
        f"{response.replica}:v{response.version}@{response.latency_ms}ms"
        for response in result.responses
    )
    return (
        f"{label}: op={result.operation} quorum={result.quorum} "
        f"responded={result.successful} available={result.available} "
        f"latency_ms={result.latency_ms} "
        f"value={result.value} version={result.version} stale={stale} "
        f"responses=[{responses}] note={result.note}"
    )


def run_demo(argv: Sequence[str] | None = None) -> list[str]:
    args = build_parser().parse_args(argv)
    if args.replicas < 3:
        raise SystemExit("--replicas must be at least 3 for this demo")
    if args.read_quorum < 1 or args.write_quorum < 1:
        raise SystemExit("read and write quorum must be at least 1")
    if args.read_quorum > args.replicas or args.write_quorum > args.replicas:
        raise SystemExit("read and write quorum cannot exceed replica count")

    latencies = parse_latencies(args.latencies, args.replicas)
    cluster = Cluster.with_latencies(latencies)
    lines = [
        (
            f"config replicas={args.replicas} "
            f"read_quorum={args.read_quorum} write_quorum={args.write_quorum} "
            f"latencies={','.join(str(latency) for latency in latencies)}"
        )
    ]

    write = cluster.write("reservation-open", write_quorum=args.write_quorum)
    lines.append(format_result("01 write quorum", write))
    lines.append(format_result("02 read quorum", cluster.read(read_quorum=args.read_quorum)))

    slowest = max(cluster.replicas, key=lambda replica: replica.latency_ms)
    cluster.seed_replica(slowest.name, "empty", 0)
    fastest = min(cluster.replicas, key=lambda replica: replica.latency_ms)
    cluster.set_unavailable({fastest.name})
    lines.append(f"03 make {fastest.name} unavailable and leave {slowest.name} stale")
    try:
        degraded = cluster.read(read_quorum=args.read_quorum)
    except QuorumUnavailable as exc:
        lines.append(f"04 degraded read unavailable: {exc}")
    else:
        lines.append(format_result("04 degraded read quorum", degraded))

    cluster.set_unavailable(
        {replica.name for replica in cluster.replicas if replica.name != slowest.name}
    )
    stale_read = cluster.read(read_quorum=1)
    lines.append(format_result("05 low quorum stale read", stale_read))

    fresh = next(replica for replica in cluster.replicas if replica.name != slowest.name)
    cluster.set_unavailable(
        {
            replica.name
            for replica in cluster.replicas
            if replica.name not in {fresh.name, slowest.name}
        }
    )
    repair_read = cluster.read(read_quorum=2)
    repaired = cluster.repair(repair_read.responses)
    lines.append(format_result("06 repair read quorum", repair_read))
    lines.append(f"07 read repair touched={','.join(repaired) if repaired else 'none'}")
    lines.append("   note read repair only updates replicas that answered that read")

    cluster.set_unavailable(set())
    fast_read = cluster.read(read_quorum=1)
    lines.append(format_result("08 fastest read quorum=1", fast_read))
    full_read = cluster.read(read_quorum=args.replicas)
    lines.append(format_result("09 full read quorum", full_read))
    lines.append("10 final replica state")
    lines.extend(f"   {line}" for line in cluster.state_lines())
    return lines


def main() -> None:
    for line in run_demo():
        print(line)


if __name__ == "__main__":
    main()
