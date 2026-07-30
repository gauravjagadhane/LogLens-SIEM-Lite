"""Thread-safe in-memory job storage for the SIEM-lite application."""

from threading import Lock

from app.models.job import AnalysisJob


class JobStore:
    """Keep completed jobs available to the dashboard process."""

    def __init__(self):
        self._jobs: dict[str, AnalysisJob] = {}
        self._lock = Lock()

    def save(self, job: AnalysisJob) -> None:
        """Insert or replace one analysis job."""
        with self._lock:
            self._jobs[job.id] = job

    def get(self, job_id: str) -> AnalysisJob | None:
        """Return a job by ID, or ``None`` when it is not present."""
        with self._lock:
            return self._jobs.get(job_id)


job_store = JobStore()
