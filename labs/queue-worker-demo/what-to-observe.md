# What To Observe

## Enqueue And Completion

The first job is visible immediately, then a worker claims and completes it.
The completion count increases and the queue has no visible work left.

Question to ask: What source-of-truth state proves that the work was accepted
before the worker touched it?

## Retryable Failure

The second job fails once with a retryable error. It is not immediately visible
because the retry delay acts like backoff. After the clock advances, another
worker claims it and completes it.

Question to ask: Which errors should retry, and how long should the system wait
before retrying?

## Retry Exhaustion

The third job keeps failing until `max_attempts` is reached. The queue moves it
to `dead_lettered` instead of retrying forever.

Question to ask: Who owns dead-letter inspection, replay, cancellation, or
manual repair?

## Visibility Timeout

The fourth job is claimed by `worker-a`, but the worker crashes before
acknowledgement. After the visibility timeout, the job becomes visible again and
`worker-b` can claim it.

Question to ask: Are side effects idempotent if two workers attempt the same
job after a timeout?

## Basic Observability

Watch the metrics lines:

- `queued` and `visible` show available work;
- `inflight` shows claimed work;
- `completed` shows successful work;
- `dead_lettered` shows exhausted failure;
- `retries` shows retry pressure;
- `expired_leases` shows worker crashes or slow processing;
- `oldest_visible_age` shows whether user promises are being violated.

Question to ask: Which metric should alert first for your product promise:
depth, oldest age, retry rate, or dead-letter age?
