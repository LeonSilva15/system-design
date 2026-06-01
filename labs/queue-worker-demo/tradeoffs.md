# Queue Worker Trade-Offs

## What Queues Buy

Queues let an API accept work quickly while workers process slower tasks later.
They smooth bursts, isolate slow dependencies, and give retryable work a
durable place to wait.

This is useful only when the product can honestly show pending, retrying,
failed, or completed states.

## What They Cost

Queues add operational responsibilities:

- jobs may run more than once;
- workers can crash after side effects but before acknowledgement;
- expired visibility leases are separate from explicit retryable failures;
- retries can overload an unhealthy dependency;
- poison jobs can consume worker capacity;
- queue depth can hide a broken downstream system;
- delayed work can violate user promises even when the API looks healthy.

## When This Pattern Fits

Use queued workers when:

- the user request can return accepted or pending status;
- the work is idempotent or guarded by dedupe state;
- retryable and permanent failures can be classified;
- workers can report attempts, safe error categories, and completion;
- operators have a way to inspect or repair dead-lettered work.

## When To Avoid It

Avoid queues when the caller needs final success immediately, the work cannot be
retried safely, duplicate delivery would create harmful side effects, or no
team owns backlog and dead-letter repair.

For example, queueing a confirmation email is reasonable. Queueing the final
decision for a seat reservation is risky if the user is told the reservation is
confirmed before the source of truth commits.

## Production Differences

A production design would usually add:

- durable storage for job state and idempotency keys;
- per-job and per-tenant concurrency limits;
- exponential backoff with jitter;
- heartbeat or lease renewal for long-running jobs;
- dead-letter inspection, replay, cancel, and quarantine tools;
- dashboards for oldest job age, retry rate, expired leases, and worker health;
- alerts tied to the product promise, not only worker CPU.

The lab keeps these concerns small so the main behavior is observable.
