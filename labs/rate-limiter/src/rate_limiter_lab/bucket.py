"""Deterministic token bucket implementation for the lab."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LimitDecision:
    """Result of one rate-limit check."""

    allowed: bool
    requested_at: float
    tokens_before: float
    tokens_after: float
    retry_after: float
    reason: str


@dataclass
class TokenBucket:
    """Token bucket with explicit time for deterministic tests and demos."""

    capacity: float
    refill_rate: float
    tokens: float | None = None
    updated_at: float = 0.0

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be greater than zero")
        if self.refill_rate <= 0:
            raise ValueError("refill_rate must be greater than zero")

        if self.tokens is None:
            self.tokens = self.capacity
        else:
            self.tokens = min(max(self.tokens, 0.0), self.capacity)

    def refill(self, now: float) -> float:
        """Refill tokens up to capacity and return the new balance."""
        if now < self.updated_at:
            raise ValueError("now must not move backward")

        elapsed = now - self.updated_at
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.updated_at = now
        return self.tokens

    def allow(self, now: float, cost: float = 1.0) -> LimitDecision:
        """Spend tokens for one request when enough tokens are available."""
        if cost <= 0:
            raise ValueError("cost must be greater than zero")

        tokens_before = self.refill(now)

        if tokens_before >= cost:
            self.tokens -= cost
            return LimitDecision(
                allowed=True,
                requested_at=now,
                tokens_before=tokens_before,
                tokens_after=self.tokens,
                retry_after=0.0,
                reason="enough_tokens",
            )

        missing = cost - tokens_before
        return LimitDecision(
            allowed=False,
            requested_at=now,
            tokens_before=tokens_before,
            tokens_after=self.tokens,
            retry_after=missing / self.refill_rate,
            reason="not_enough_tokens",
        )


def simulate_requests(
    bucket: TokenBucket,
    request_count: int,
    spacing: float,
    cost: float = 1.0,
) -> list[LimitDecision]:
    """Run a deterministic sequence of requests against a bucket."""
    if request_count < 0:
        raise ValueError("request_count must be zero or greater")
    if spacing < 0:
        raise ValueError("spacing must be zero or greater")

    decisions: list[LimitDecision] = []
    for index in range(request_count):
        now = index * spacing
        decisions.append(bucket.allow(now=now, cost=cost))
    return decisions
