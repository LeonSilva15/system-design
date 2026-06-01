# What To Observe

Use the lab to answer these questions:

- How many reservations does the unsafe flow create?
- How many emails are sent when duplicate requests are not deduped?
- What changes when retries reuse one idempotency key?
- What response does a duplicate request receive?
- What happens when the same key is reused for a different operation?
- Which side effect is protected during duplicate event delivery?

## Suggested Experiments

| Experiment | Change | Expected Observation |
| --- | --- | --- |
| Baseline | Run the default demo | Unsafe retries multiply reservations; safe retries return the stored result |
| More duplicate pressure | `--attempts 5` | Unsafe reservations and emails grow with attempts |
| Safe-only view | `--mode safe --attempts 5` | Reservation count remains `1` while duplicate count grows |
| Event redelivery | `--event-deliveries 4` | Only one event side effect is sent |
| Key conflict | `--mode safe --show-conflict` | Reusing a key for a different workshop returns `conflict` |

## Connect Back To Design

After running the lab, update your design notes:

- Who creates the idempotency key: client, API, producer, or worker?
- What request fields form the fingerprint for one intended operation?
- Where is the first response stored?
- Which downstream side effects need their own dedupe records?
- How long should duplicate suppression records be retained?
- What metric would expose duplicate requests, event redelivery, and key
  conflicts?
