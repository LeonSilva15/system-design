# What To Observe

## Poison Message

Line `02` classifies `invalid_recipient` as permanent and sends it to the DLQ
without retry. This protects worker capacity and shortens the repair loop.

Question to ask: Which failure categories should fail fast instead of spending
the retry budget?

## Retry Exhaustion

Lines `03.*` show a retryable `handler_bug` consuming attempts until the retry
budget is exhausted. The final state is `dead_lettered`, not an infinite loop.

Question to ask: What maximum attempts, total retry deadline, and backoff policy
match the user promise?

## DLQ Inspection

Line `04` lists open dead-letter records with safe context. The model keeps
owner, idempotency key, attempts, safe error category, and replay eligibility.

Question to ask: Can an operator decide the next action without reading raw
secrets, stack traces, or unrelated logs?

## Alerting

Line `05` fires alerts for count and age. Count catches broad spikes; oldest age
catches ignored repair work.

Question to ask: Which DLQ alerts should page immediately, and which should
create a ticket for later review?

## Replay

Line `06` replays the handler-bug record after the template handler is fixed.
The replay job uses the same idempotency key because it is the same business
action.

Question to ask: Does replay recheck current source-of-truth state before
sending user-visible side effects?

## Unsafe Replay

Line `07` blocks replay for the invalid-recipient record. That work needs input
correction, cancellation, contact with the member, or another explicit
remediation.

Question to ask: What are the allowed decisions besides replay: skip, cancel,
compensate, or escalate?

## Final State

Line `08` leaves one open dead letter and one replayed record. The goal is not
an empty DLQ at all costs; the goal is visible, owned, safe repair.

Question to ask: Who owns each remaining open record, and when does its age
violate a product or support promise?
