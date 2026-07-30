"""Orchestration service for streaming log analysis."""

from collections import Counter
from pathlib import Path
from uuid import uuid4

from app.detector.threat_detector import create_detector
from app.models.job import AnalysisJob
from app.parser.access_log_parser import parse_access_log, parse_log_line


def analyze_log_file(file_path: Path, source_name: str, config: dict) -> AnalysisJob:
    """Analyze a log file in one streaming pass and return its completed job."""
    job = AnalysisJob(id=str(uuid4()), source_name=source_name)
    detector = create_detector(
        config["BRUTE_FORCE_THRESHOLD"], config["BRUTE_FORCE_WINDOW_SECONDS"]
    )
    statuses: Counter[str] = Counter()
    timelines: Counter[str] = Counter()
    attackers: Counter[str] = Counter()
    categories: Counter[str] = Counter()

    try:
        with file_path.open("r", encoding="utf-8", errors="replace") as log_file:
            for raw_line in log_file:
                if not raw_line.strip():
                    continue
                entry = parse_log_line(raw_line)
                if entry is None:
                    job.malformed_lines += 1
                    continue
                job.total_requests += 1
                statuses[str(entry["status"])] += 1
                for threat in detector.inspect(entry):
                    job.threats.append(threat)
                    timelines[_timeline_bucket(threat["timestamp"])] += 1
                    attackers[threat["ip"]] += 1
                    categories[threat["type"]] += 1
    except OSError as error:
        job.status = "failed"
        job.error = f"Could not read log file: {error}"
        return job

    if job.total_requests == 0:
        job.status = "failed"
        job.error = "Unsupported format or no valid access-log records found."
        return job

    job.status_distribution = dict(statuses)
    job.attack_timeline = dict(sorted(timelines.items()))
    job.top_attackers = dict(attackers.most_common(10))
    job.attack_categories = dict(categories)
    job.status = "completed"
    return job


def _timeline_bucket(timestamp: str) -> str:
    """Create a readable minute bucket without relying on client-side parsing."""
    return timestamp[:17]
