# Trade-Offs

## What This Lab Teaches

- Retries are unsafe when repeating the operation creates a second business
  result.
- Idempotency keys protect one intended operation, not every future action by a
  user.
- Duplicate event delivery is normal enough that consumers should be safe by
  default.
- Side effects often need their own dedupe keys even when the source command is
  idempotent.

## What This Lab Omits

- Durable database constraints and transactions.
- Expiration policies for old idempotency records.
- Privacy controls for stored request fingerprints and responses.
- Concurrent duplicate submissions racing at the same time.
- Provider-specific idempotency APIs.
- Reconciliation for ambiguous external results.

## Production Considerations

| Lab Choice | Production Question |
| --- | --- |
| In-memory key store | Which durable table or unique constraint owns the key? |
| Tuple fingerprint | Which request fields prove two attempts are the same intent? |
| Stored result | What response fields are safe and useful to retain? |
| Email list side effect | Which outbound provider calls need send records? |
| Event and side-effect dedupe | Can replay rebuild state without repeating irreversible actions? |

## Common Mistakes

- Generating a new key for every retry.
- Storing the idempotency key after the side effect already happened.
- Treating a duplicate event as impossible because the broker usually delivers
  once.
- Using a key that is too broad, such as only `member_id`.
- Using a key that is too narrow, such as a new random value per attempt.
- Deduping the API request but resending email, payment, or webhook side
  effects.

## Related Pages

- [Idempotency](../../docs/communication/idempotency.md)
- [Retries and backoff](../../docs/communication/retries-and-backoff.md)
- [Reliability retries](../../docs/reliability/retries.md)
- [Payment workflow walkthrough](../../docs/walkthroughs/payment-workflow.md)
