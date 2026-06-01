"""Deterministic queue and worker model used by the lab."""

from __future__ import annotations

from dataclasses import dataclass, field


class JobNotInflight(RuntimeError):
    """Raised when a worker tries to finish a job it no longer owns."""


@dataclass
class Job:
    """A durable unit of work in the toy queue."""

    job_id: str
    kind: str
    payload: str
    created_at: float
    visible_at: float
    max_attempts: int = 3
    attempts: int = 0
    status: str = "queued"
    worker_id: str | None = None
    lease_deadline: float | None = None
    completed_at: float | None = None
    last_error: str | None = None
    history: list[str] = field(default_factory=list)

    def is_visible(self, now: float) -> bool:
        return self.status in {"queued", "retrying"} and self.visible_at <= now


@dataclass(frozen=True)
class QueueMetrics:
    queued: int
    visible: int
    inflight: int
    completed: int
    dead_lettered: int
    retries_scheduled: int
    expired_leases: int
    oldest_visible_age: float | None


@dataclass(frozen=True)
class WorkResult:
    job_id: str
    worker_id: str
    outcome: str
    status: str
    attempts: int
    message: str


class ManualClock:
    """A controlled clock so visibility timeout behavior is deterministic."""

    def __init__(self, now: float = 0.0) -> None:
        self._now = now

    @property
    def now(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("cannot move time backwards")
        self._now += seconds


class InMemoryQueue:
    """A small durable queue model with retries and visibility timeouts."""

    def __init__(self, clock: ManualClock) -> None:
        self.clock = clock
        self.jobs: dict[str, Job] = {}
        self._sequence = 0
        self.retries_scheduled = 0
        self.expired_leases = 0

    def enqueue(
        self,
        kind: str,
        payload: str,
        *,
        max_attempts: int = 3,
        delay_seconds: float = 0.0,
    ) -> Job:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if delay_seconds < 0:
            raise ValueError("delay_seconds cannot be negative")

        self._sequence += 1
        job = Job(
            job_id=f"job-{self._sequence:03d}",
            kind=kind,
            payload=payload,
            created_at=self.clock.now,
            visible_at=self.clock.now + delay_seconds,
            max_attempts=max_attempts,
        )
        job.history.append(f"{self.clock.now:.1f}s enqueued")
        self.jobs[job.job_id] = job
        return job

    def claim(self, worker_id: str, *, visibility_timeout: float) -> Job | None:
        if visibility_timeout <= 0:
            raise ValueError("visibility_timeout must be positive")

        self.reap_expired_leases()
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
        job.lease_deadline = self.clock.now + visibility_timeout
        job.attempts += 1
        job.history.append(
            (
                f"{self.clock.now:.1f}s claimed by {worker_id} "
                f"attempt={job.attempts} lease_until={job.lease_deadline:.1f}s"
            )
        )
        return job

    def complete(self, job_id: str, worker_id: str) -> WorkResult:
        job = self._require_owned_job(job_id, worker_id)
        job.status = "completed"
        job.completed_at = self.clock.now
        job.worker_id = None
        job.lease_deadline = None
        job.history.append(f"{self.clock.now:.1f}s completed by {worker_id}")
        return WorkResult(
            job_id=job.job_id,
            worker_id=worker_id,
            outcome="success",
            status=job.status,
            attempts=job.attempts,
            message="job completed",
        )

    def fail_retryable(
        self,
        job_id: str,
        worker_id: str,
        *,
        error: str,
        retry_delay: float,
    ) -> WorkResult:
        if retry_delay < 0:
            raise ValueError("retry_delay cannot be negative")

        job = self._require_owned_job(job_id, worker_id)
        job.last_error = error
        job.worker_id = None
        job.lease_deadline = None

        if job.attempts >= job.max_attempts:
            job.status = "dead_lettered"
            job.history.append(
                (
                    f"{self.clock.now:.1f}s dead-lettered after "
                    f"attempt={job.attempts} error={error}"
                )
            )
            return WorkResult(
                job_id=job.job_id,
                worker_id=worker_id,
                outcome="dead_lettered",
                status=job.status,
                attempts=job.attempts,
                message=error,
            )

        job.status = "retrying"
        job.visible_at = self.clock.now + retry_delay
        self.retries_scheduled += 1
        job.history.append(
            (
                f"{self.clock.now:.1f}s retry scheduled by {worker_id} "
                f"after={retry_delay:.1f}s error={error}"
            )
        )
        return WorkResult(
            job_id=job.job_id,
            worker_id=worker_id,
            outcome="retry_scheduled",
            status=job.status,
            attempts=job.attempts,
            message=error,
        )

    def fail_permanent(self, job_id: str, worker_id: str, *, error: str) -> WorkResult:
        job = self._require_owned_job(job_id, worker_id)
        job.status = "dead_lettered"
        job.last_error = error
        job.worker_id = None
        job.lease_deadline = None
        job.history.append(f"{self.clock.now:.1f}s permanent failure error={error}")
        return WorkResult(
            job_id=job.job_id,
            worker_id=worker_id,
            outcome="dead_lettered",
            status=job.status,
            attempts=job.attempts,
            message=error,
        )

    def reap_expired_leases(self) -> list[Job]:
        expired: list[Job] = []
        for job in self.jobs.values():
            if (
                job.status == "inflight"
                and job.lease_deadline is not None
                and job.lease_deadline <= self.clock.now
            ):
                job.status = "retrying"
                job.visible_at = self.clock.now
                job.worker_id = None
                job.lease_deadline = None
                job.last_error = "visibility timeout expired"
                job.history.append(f"{self.clock.now:.1f}s lease expired")
                self.expired_leases += 1
                expired.append(job)
        return expired

    def metrics(self) -> QueueMetrics:
        self.reap_expired_leases()
        now = self.clock.now
        visible_jobs = [
            job for job in self.jobs.values() if job.is_visible(now)
        ]
        queued = sum(1 for job in self.jobs.values() if job.status in {"queued", "retrying"})
        inflight = sum(1 for job in self.jobs.values() if job.status == "inflight")
        completed = sum(1 for job in self.jobs.values() if job.status == "completed")
        dead_lettered = sum(1 for job in self.jobs.values() if job.status == "dead_lettered")
        oldest_visible_age = None
        if visible_jobs:
            oldest_visible_age = max(now - job.created_at for job in visible_jobs)
        return QueueMetrics(
            queued=queued,
            visible=len(visible_jobs),
            inflight=inflight,
            completed=completed,
            dead_lettered=dead_lettered,
            retries_scheduled=self.retries_scheduled,
            expired_leases=self.expired_leases,
            oldest_visible_age=oldest_visible_age,
        )

    def _require_owned_job(self, job_id: str, worker_id: str) -> Job:
        job = self.jobs[job_id]
        if (
            job.status == "inflight"
            and job.lease_deadline is not None
            and job.lease_deadline <= self.clock.now
        ):
            self.reap_expired_leases()
        if job.status != "inflight" or job.worker_id != worker_id:
            raise JobNotInflight(
                f"{job_id} is not currently owned by worker {worker_id}"
            )
        return job


class Worker:
    """A worker that claims one job and records the chosen outcome."""

    def __init__(
        self,
        worker_id: str,
        queue: InMemoryQueue,
        *,
        visibility_timeout: float = 5.0,
    ) -> None:
        self.worker_id = worker_id
        self.queue = queue
        self.visibility_timeout = visibility_timeout

    def claim(self) -> Job | None:
        return self.queue.claim(
            self.worker_id,
            visibility_timeout=self.visibility_timeout,
        )

    def run_once(
        self,
        *,
        outcome: str = "success",
        retry_delay: float = 2.0,
        error: str = "temporary dependency timeout",
    ) -> WorkResult | None:
        job = self.claim()
        if job is None:
            return None
        if outcome == "success":
            return self.queue.complete(job.job_id, self.worker_id)
        if outcome == "retryable":
            return self.queue.fail_retryable(
                job.job_id,
                self.worker_id,
                error=error,
                retry_delay=retry_delay,
            )
        if outcome == "permanent":
            return self.queue.fail_permanent(
                job.job_id,
                self.worker_id,
                error=error,
            )
        if outcome == "crash":
            job.history.append(f"{self.queue.clock.now:.1f}s {self.worker_id} crashed")
            return WorkResult(
                job_id=job.job_id,
                worker_id=self.worker_id,
                outcome="crashed",
                status=job.status,
                attempts=job.attempts,
                message="worker stopped before ack",
            )
        raise ValueError(f"unknown worker outcome: {outcome}")
