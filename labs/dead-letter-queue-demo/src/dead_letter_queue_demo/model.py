"""Deterministic dead-letter queue model used by the lab."""

from __future__ import annotations

from dataclasses import dataclass, field


class JobNotInflight(RuntimeError):
    """Raised when a worker tries to finish a job it does not own."""


class ReplayNotAllowed(RuntimeError):
    """Raised when an operator tries to replay an unsafe dead letter."""


@dataclass
class Job:
    job_id: str
    kind: str
    payload: str
    owner: str
    idempotency_key: str
    max_attempts: int
    created_at: float
    visible_at: float
    attempts: int = 0
    status: str = "queued"
    worker_id: str | None = None
    first_error_category: str | None = None
    last_error_category: str | None = None
    last_safe_message: str | None = None
    dead_letter_id: str | None = None
    history: list[str] = field(default_factory=list)

    def is_visible(self, now: float) -> bool:
        return self.status in {"queued", "retrying"} and self.visible_at <= now


@dataclass(frozen=True)
class WorkResult:
    job_id: str
    outcome: str
    status: str
    attempts: int
    error_category: str | None = None
    safe_message: str | None = None
    dead_letter_id: str | None = None
    replayable: bool | None = None


@dataclass
class DeadLetterRecord:
    dead_letter_id: str
    job_id: str
    kind: str
    payload_summary: str
    owner: str
    idempotency_key: str
    attempts: int
    first_error_category: str
    last_error_category: str
    safe_message: str
    replayable: bool
    created_at: float
    status: str = "open"
    replay_job_id: str | None = None
    decisions: list[str] = field(default_factory=list)

    def age(self, now: float) -> float:
        return max(0.0, now - self.created_at)


@dataclass(frozen=True)
class Alert:
    name: str
    severity: str
    message: str
    open_count: int
    oldest_age: float


class ManualClock:
    """A controlled clock so alert-age behavior is deterministic."""

    def __init__(self, now: float = 0.0) -> None:
        self._now = now

    @property
    def now(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("cannot move time backwards")
        self._now += seconds


class DeadLetterQueue:
    """Stores failed accepted work with safe inspection and repair context."""

    def __init__(self) -> None:
        self.records: dict[str, DeadLetterRecord] = {}
        self._sequence = 0

    def add(
        self,
        job: Job,
        *,
        error_category: str,
        safe_message: str,
        replayable: bool,
        now: float,
    ) -> DeadLetterRecord:
        self._sequence += 1
        record = DeadLetterRecord(
            dead_letter_id=f"dlq-{self._sequence:03d}",
            job_id=job.job_id,
            kind=job.kind,
            payload_summary=job.payload,
            owner=job.owner,
            idempotency_key=job.idempotency_key,
            attempts=job.attempts,
            first_error_category=job.first_error_category or error_category,
            last_error_category=error_category,
            safe_message=safe_message,
            replayable=replayable,
            created_at=now,
        )
        record.decisions.append(f"{now:.1f}s opened category={error_category}")
        self.records[record.dead_letter_id] = record
        return record

    def inspect(self, dead_letter_id: str) -> DeadLetterRecord:
        return self.records[dead_letter_id]

    def open_records(self) -> tuple[DeadLetterRecord, ...]:
        return tuple(
            record
            for record in sorted(self.records.values(), key=lambda item: item.dead_letter_id)
            if record.status == "open"
        )

    def records_by_status(self, status: str) -> tuple[DeadLetterRecord, ...]:
        return tuple(
            record
            for record in sorted(self.records.values(), key=lambda item: item.dead_letter_id)
            if record.status == status
        )

    def mark_resolved(self, dead_letter_id: str, *, action: str, reason: str, now: float) -> None:
        record = self.inspect(dead_letter_id)
        record.status = action
        record.decisions.append(f"{now:.1f}s {action} reason={reason}")

    def alerts(
        self,
        *,
        now: float,
        oldest_age_threshold: float,
        count_threshold: int,
    ) -> tuple[Alert, ...]:
        if oldest_age_threshold <= 0:
            raise ValueError("oldest_age_threshold must be positive")
        if count_threshold < 1:
            raise ValueError("count_threshold must be at least 1")

        open_records = self.open_records()
        open_count = len(open_records)
        oldest_age = max((record.age(now) for record in open_records), default=0.0)
        alerts: list[Alert] = []
        if open_count >= count_threshold:
            alerts.append(
                Alert(
                    name="dlq_open_count",
                    severity="page",
                    message=f"open_dead_letters={open_count} threshold={count_threshold}",
                    open_count=open_count,
                    oldest_age=oldest_age,
                )
            )
        if oldest_age >= oldest_age_threshold:
            alerts.append(
                Alert(
                    name="dlq_oldest_age",
                    severity="page",
                    message=f"oldest_age={oldest_age:.1f}s threshold={oldest_age_threshold:.1f}s",
                    open_count=open_count,
                    oldest_age=oldest_age,
                )
            )
        return tuple(alerts)


class WorkQueue:
    """A small queue that moves exhausted or permanent failures into a DLQ."""

    def __init__(self, clock: ManualClock, dead_letters: DeadLetterQueue) -> None:
        self.clock = clock
        self.dead_letters = dead_letters
        self.jobs: dict[str, Job] = {}
        self._sequence = 0

    def enqueue(
        self,
        kind: str,
        payload: str,
        *,
        owner: str,
        max_attempts: int = 3,
        idempotency_key: str | None = None,
        delay_seconds: float = 0.0,
    ) -> Job:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if delay_seconds < 0:
            raise ValueError("delay_seconds cannot be negative")
        if not owner:
            raise ValueError("owner cannot be empty")

        self._sequence += 1
        job_id = f"job-{self._sequence:03d}"
        job = Job(
            job_id=job_id,
            kind=kind,
            payload=payload,
            owner=owner,
            idempotency_key=idempotency_key or f"{kind}:{job_id}",
            max_attempts=max_attempts,
            created_at=self.clock.now,
            visible_at=self.clock.now + delay_seconds,
        )
        job.history.append(f"{self.clock.now:.1f}s enqueued")
        self.jobs[job.job_id] = job
        return job

    def claim(self, worker_id: str) -> Job | None:
        visible_jobs = [
            job
            for job in self.jobs.values()
            if job.is_visible(self.clock.now)
        ]
        visible_jobs.sort(key=lambda job: (job.visible_at, job.created_at, job.job_id))
        if not visible_jobs:
            return None
        job = visible_jobs[0]
        job.status = "inflight"
        job.worker_id = worker_id
        job.attempts += 1
        job.history.append(f"{self.clock.now:.1f}s claimed by {worker_id} attempt={job.attempts}")
        return job

    def complete(self, job_id: str, worker_id: str) -> WorkResult:
        job = self._require_owned_job(job_id, worker_id)
        job.status = "completed"
        job.worker_id = None
        job.history.append(f"{self.clock.now:.1f}s completed by {worker_id}")
        return WorkResult(
            job_id=job.job_id,
            outcome="success",
            status=job.status,
            attempts=job.attempts,
        )

    def fail(
        self,
        job_id: str,
        worker_id: str,
        *,
        error_category: str,
        safe_message: str,
        retryable: bool,
        replayable: bool,
        retry_delay: float,
    ) -> WorkResult:
        if retry_delay < 0:
            raise ValueError("retry_delay cannot be negative")
        job = self._require_owned_job(job_id, worker_id)
        if job.first_error_category is None:
            job.first_error_category = error_category
        job.last_error_category = error_category
        job.last_safe_message = safe_message
        job.worker_id = None

        if retryable and job.attempts < job.max_attempts:
            job.status = "retrying"
            job.visible_at = self.clock.now + retry_delay
            job.history.append(
                f"{self.clock.now:.1f}s retry scheduled category={error_category}"
            )
            return WorkResult(
                job_id=job.job_id,
                outcome="retry_scheduled",
                status=job.status,
                attempts=job.attempts,
                error_category=error_category,
                safe_message=safe_message,
            )

        job.status = "dead_lettered"
        record = self.dead_letters.add(
            job,
            error_category=error_category,
            safe_message=safe_message,
            replayable=replayable,
            now=self.clock.now,
        )
        job.dead_letter_id = record.dead_letter_id
        job.history.append(
            f"{self.clock.now:.1f}s dead-lettered id={record.dead_letter_id}"
        )
        return WorkResult(
            job_id=job.job_id,
            outcome="dead_lettered",
            status=job.status,
            attempts=job.attempts,
            error_category=error_category,
            safe_message=safe_message,
            dead_letter_id=record.dead_letter_id,
            replayable=replayable,
        )

    def replay_dead_letter(
        self,
        dead_letter_id: str,
        *,
        reason: str,
        payload: str | None = None,
    ) -> Job:
        record = self.dead_letters.inspect(dead_letter_id)
        if record.status != "open":
            raise ReplayNotAllowed(f"{dead_letter_id} is not open")
        if not record.replayable:
            raise ReplayNotAllowed(f"{dead_letter_id} is not replayable")
        if record.replay_job_id is not None:
            raise ReplayNotAllowed(f"{dead_letter_id} already has replay job {record.replay_job_id}")

        replay_job = self.enqueue(
            record.kind,
            payload or record.payload_summary,
            owner=record.owner,
            max_attempts=2,
            idempotency_key=record.idempotency_key,
        )
        record.replay_job_id = replay_job.job_id
        record.decisions.append(f"{self.clock.now:.1f}s replay_enqueued reason={reason}")
        return replay_job

    def _require_owned_job(self, job_id: str, worker_id: str) -> Job:
        job = self.jobs[job_id]
        if job.status != "inflight" or job.worker_id != worker_id:
            raise JobNotInflight(f"{job_id} is not owned by {worker_id}")
        return job


class Worker:
    """A worker that claims one job and records the chosen outcome."""

    def __init__(self, worker_id: str, queue: WorkQueue) -> None:
        self.worker_id = worker_id
        self.queue = queue

    def claim(self) -> Job | None:
        return self.queue.claim(self.worker_id)

    def complete(self, job: Job) -> WorkResult:
        return self.queue.complete(job.job_id, self.worker_id)

    def fail(
        self,
        job: Job,
        *,
        error_category: str,
        safe_message: str,
        retryable: bool,
        replayable: bool,
        retry_delay: float,
    ) -> WorkResult:
        return self.queue.fail(
            job.job_id,
            self.worker_id,
            error_category=error_category,
            safe_message=safe_message,
            retryable=retryable,
            replayable=replayable,
            retry_delay=retry_delay,
        )


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def format_dead_letters(records: tuple[DeadLetterRecord, ...]) -> str:
    if not records:
        return "none"
    return ",".join(
        (
            f"{record.dead_letter_id}:{record.last_error_category}:"
            f"attempts={record.attempts}:replayable={yes_no(record.replayable)}:"
            f"status={record.status}"
        )
        for record in records
    )


def format_alerts(alerts: tuple[Alert, ...]) -> str:
    if not alerts:
        return "none"
    return ",".join(f"{alert.name}:{alert.message}" for alert in alerts)
