# Trade-Offs

## What This Lab Teaches

A dead-letter queue is a repair path for accepted work that automatic processing
cannot complete safely. It prevents poison messages from consuming workers and
prevents retry exhaustion from becoming silent data loss, but it creates an
operator workflow that must be owned.

## Poison Message Classification

Failing fast for permanent errors saves capacity and makes repair clearer.

Trade-offs:

- correct classification avoids wasted retries;
- wrong classification can stop recoverable work too early;
- safe error categories must avoid leaking secrets or personal data;
- producer and worker owners need a shared vocabulary.

Use fail-fast DLQ handling for invalid payloads, impossible state transitions,
expired business windows, and tenant-boundary violations.

## Retry Exhaustion

Bounded retries protect workers and dependencies.

Trade-offs:

- more attempts can recover from longer transient outages;
- fewer attempts shorten repair time for repeated failures;
- every retry can repeat side-effect risk unless the handler is idempotent;
- retry budgets need alerts before user promises expire.

Automatic retries should end in a named state with context, owner, and next
action.

## Inspection Context

Dead-letter records should contain enough information to decide repair.

Trade-offs:

- richer context speeds operator decisions;
- raw payloads can leak sensitive data;
- storing only an error code may force responders to search logs;
- protected payload references need retention and access rules.

Prefer stable IDs, safe categories, owners, attempts, timestamps, correlation
IDs, and idempotency keys over raw secrets or full personal data.

## Replay

Replay is useful after a handler fix, input correction, or dependency recovery.

Trade-offs:

- replay can complete accepted work without manual reconstruction;
- unsafe replay can duplicate emails, payments, grants, or partner calls;
- batch replay can overload dependencies;
- old work may be obsolete or cancelled.

Replay should be scoped, rate-limited, audited, idempotent, and guarded by a
current source-of-truth check.

## Alerting

DLQ alerts should represent repair risk, not only raw count.

Trade-offs:

- count alerts catch broad deploy or dependency failures;
- age alerts catch ignored user-visible work;
- over-sensitive alerts create fatigue;
- under-sensitive alerts let accepted work disappear from operations.

Alert thresholds should reflect job type, owner, user promise, and remediation
SLA.

## Version 1 Simplification

For a first version:

- classify retryable versus permanent failures;
- stop after a bounded retry budget;
- record safe DLQ context;
- alert on oldest age and count by job type;
- allow single-record replay only when idempotency and state checks exist;
- leave unsafe records open for correction, cancellation, skip, or escalation.

Avoid building bulk replay before single-record replay is safe and observable.
