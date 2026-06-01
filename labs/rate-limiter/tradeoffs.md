# Trade-Offs

## What This Lab Teaches

- Token bucket allows bursts while enforcing an average refill rate.
- Burst capacity and refill rate are separate design decisions.
- Retry hints come from the missing tokens and refill rate.
- Deterministic clocks make rate-limiter behavior easier to test.

## What This Lab Omits

- Distributed counters and atomic updates across several API instances.
- Clock skew between servers.
- Storage failures and fail-open or fail-closed behavior.
- Multiple limit keys, such as per user plus per tenant plus global provider
  budget.
- Metrics, logs, and dashboards for the limiter itself.
- Abuse behavior where callers rotate accounts, IPs, or API keys.

## Production Considerations

| Lab Choice | Production Question |
| --- | --- |
| One in-memory bucket | Where should shared counters live across API instances? |
| Deterministic timestamp | Which server or counter-store clock is authoritative? |
| One token per request | Should expensive actions cost more tokens? |
| Immediate denial | Should clients be rejected, queued, delayed, or challenged? |
| Local exact state | Is approximate or sharded enforcement acceptable? |

## Common Mistakes

- Setting burst capacity so high that a full bucket can overload the protected
  dependency.
- Treating token bucket as an abuse solution without choosing good limit keys.
- Retrying limited requests immediately and creating more load.
- Forgetting to emit metrics for allowed, limited, and fallback decisions.
- Testing only the happy path and not empty-bucket recovery.

## Related Pages

- [Rate limiting](../../docs/scalability/rate-limiting.md)
- [Rate limiting and abuse resistance](../../docs/security/rate-limiting-and-abuse.md)
- [Rate limiter walkthrough](../../docs/walkthroughs/rate-limiter.md)
