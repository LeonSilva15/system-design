# Expected Output

The default demo:

```bash
python -m retry_idempotency_demo.demo
```

prints output similar to:

```text
scenario=unsafe_requests attempts=3
attempt=1 status=created reservation=res-001 duplicate=false email_sent=true
attempt=2 status=created reservation=res-002 duplicate=false email_sent=true
attempt=3 status=created reservation=res-003 duplicate=false email_sent=true
summary mode=unsafe reservations=3 emails=3
---
scenario=safe_requests attempts=3 key=reserve-2026-05
attempt=1 status=created reservation=res-001 duplicate=false email_sent=true
attempt=2 status=duplicate reservation=res-001 duplicate=true email_sent=false
attempt=3 status=duplicate reservation=res-001 duplicate=true email_sent=false
summary mode=safe reservations=1 emails=1 key_conflicts=0 duplicate_requests=2
scenario=duplicate_events deliveries=2 reservation=res-001
delivery=1 status=sent duplicate=false email_sent=true
delivery=2 status=duplicate_event duplicate=true email_sent=false
summary mode=events event_side_effects=1 total_emails=2 duplicate_events=1
```

What this proves:

- unsafe retries create one reservation and one email per attempt;
- safe retries reuse the first reservation result;
- duplicate requests do not repeat the confirmation side effect;
- duplicate event delivery is observable and does not resend the event side
  effect.

Small formatting differences are acceptable if the behavior is the same.
