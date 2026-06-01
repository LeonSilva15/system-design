# Expected Output

The default command:

```bash
python -m queue_worker_demo.demo
```

prints output similar to:

```text
config visibility_timeout=5.0s retry_delay=3.0s max_attempts=3
01 enqueue success job: job=job-001 kind=thumbnail
02 after enqueue: queued=1 visible=1 inflight=0 completed=0 dead_lettered=0 retries=0 expired_leases=0 oldest_visible_age=0.0s
03 worker completes: job=job-001 worker=worker-a outcome=success status=completed attempts=1 message=job completed
04 after completion: queued=0 visible=0 inflight=0 completed=1 dead_lettered=0 retries=0 expired_leases=0 oldest_visible_age=none
05 enqueue retry job: job=job-002 kind=email
06 first attempt fails: job=job-002 worker=worker-a outcome=retry_scheduled status=retrying attempts=1 message=temporary dependency timeout
07 retry scheduled: queued=1 visible=0 inflight=0 completed=1 dead_lettered=0 retries=1 expired_leases=0 oldest_visible_age=none
08 retry succeeds: job=job-002 worker=worker-b outcome=success status=completed attempts=2 message=job completed
09 enqueue failing job: job=job-003 kind=webhook
10.1 retryable failure: job=job-003 worker=worker-a outcome=retry_scheduled status=retrying attempts=1 message=provider timeout
10.2 retryable failure: job=job-003 worker=worker-a outcome=retry_scheduled status=retrying attempts=2 message=provider timeout
10.3 retryable failure: job=job-003 worker=worker-a outcome=dead_lettered status=dead_lettered attempts=3 message=provider timeout
11 enqueue visibility-timeout job: job=job-004 kind=report
12 worker crashes before ack: job=job-004 worker=worker-a outcome=crashed status=inflight attempts=1 message=worker stopped before ack
13 after visibility timeout: queued=1 visible=1 inflight=0 completed=2 dead_lettered=1 retries=3 expired_leases=1 oldest_visible_age=5.1s
14 redelivered to another worker: job=job-004 worker=worker-b outcome=success status=completed attempts=2 message=job completed
15 final metrics: queued=0 visible=0 inflight=0 completed=3 dead_lettered=1 retries=3 expired_leases=1 oldest_visible_age=none
```

The important fields are `status`, `attempts`, `retries`, `expired_leases`,
`dead_lettered`, and `oldest_visible_age`.
