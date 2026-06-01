import pytest

from rate_limiter_lab import TokenBucket, simulate_requests
from rate_limiter_lab.demo import run_demo


def test_initial_burst_uses_capacity_then_limits() -> None:
    bucket = TokenBucket(capacity=3, refill_rate=1)

    decisions = [bucket.allow(now=0) for _ in range(4)]

    assert [decision.allowed for decision in decisions] == [True, True, True, False]
    assert decisions[-1].retry_after == pytest.approx(1.0)


def test_refill_allows_later_request() -> None:
    bucket = TokenBucket(capacity=1, refill_rate=2)

    first = bucket.allow(now=0)
    too_soon = bucket.allow(now=0.25)
    after_refill = bucket.allow(now=0.5)

    assert first.allowed
    assert not too_soon.allowed
    assert too_soon.retry_after == pytest.approx(0.25)
    assert after_refill.allowed


def test_refill_does_not_exceed_capacity() -> None:
    bucket = TokenBucket(capacity=4, refill_rate=10, tokens=0)

    balance = bucket.refill(now=10)

    assert balance == pytest.approx(4)


def test_simulation_refill_rate_changes_allowed_count() -> None:
    slow = simulate_requests(
        TokenBucket(capacity=2, refill_rate=0.5),
        request_count=5,
        spacing=0.2,
    )
    fast = simulate_requests(
        TokenBucket(capacity=2, refill_rate=5),
        request_count=5,
        spacing=0.2,
    )

    assert sum(decision.allowed for decision in slow) < sum(
        decision.allowed for decision in fast
    )


def test_invalid_clock_direction_is_rejected() -> None:
    bucket = TokenBucket(capacity=2, refill_rate=1)
    bucket.allow(now=1)

    with pytest.raises(ValueError, match="backward"):
        bucket.allow(now=0)


def test_demo_prints_summary_and_limited_requests() -> None:
    lines = run_demo([])

    assert lines[0].startswith("config capacity=5.00")
    assert any("decision=limited" in line for line in lines)
    assert lines[-1] == "summary allowed=6 limited=4 final_tokens=0.80"
