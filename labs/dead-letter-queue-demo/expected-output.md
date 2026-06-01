# Expected Output

The default command:

```bash
PYTHONPATH=src python -m dead_letter_queue_demo.demo
```

prints deterministic output similar to:

```text
config max_attempts=3 retry_delay=2.0s alert_age=10.0s alert_count=2
01 completed normal job: job=job-001 outcome=success
02 poison message dead-lettered: job=job-002 outcome=dead_lettered status=dead_lettered attempts=1 category=invalid_recipient dlq=dlq-001 replayable=no
03.1 retry scheduled: job=job-003 outcome=retry_scheduled status=retrying attempts=1 category=handler_bug dlq=none replayable=unknown
03.2 retry scheduled: job=job-003 outcome=retry_scheduled status=retrying attempts=2 category=handler_bug dlq=none replayable=unknown
03 retry exhausted: job=job-003 outcome=dead_lettered status=dead_lettered attempts=3 category=handler_bug dlq=dlq-002 replayable=yes
   retry subject: job=job-003 final_status=dead_lettered
04 dlq inspection: open=2 records=dlq-001:invalid_recipient:attempts=1:replayable=no:status=open,dlq-002:handler_bug:attempts=3:replayable=yes:status=open
05 alerting: alerts=2 signals=dlq_open_count:open_dead_letters=2 threshold=2,dlq_oldest_age:oldest_age=15.0s threshold=10.0s
06 replay: dlq=dlq-002 replay_job=job-004 idempotency_key=res-102:pickup-reminder outcome=success dlq_status=replayed
07 unsafe replay blocked: dlq=dlq-001 category=invalid_recipient action=correct_input_or_cancel message=dlq-001 is not replayable
08 final dlq state: open=1 replayed=1 records=dlq-001:invalid_recipient:attempts=1:replayable=no:status=open
```

## How To Read It

- Line `02` shows a poison message. It is dead-lettered after one attempt
  because retrying an invalid recipient would waste capacity.
- Lines `03.*` show retry exhaustion. The handler bug is retryable at first,
  but automatic retries stop at the configured attempt limit.
- Line `04` shows DLQ inspection context: category, attempts, replayability, and
  status.
- Line `05` shows two alert signals: open dead-letter count and oldest age.
- Line `06` shows a safe replay after the handler is fixed. It reuses the same
  idempotency key because the business action is the same reminder.
- Line `07` blocks unsafe replay for the invalid-recipient record.
