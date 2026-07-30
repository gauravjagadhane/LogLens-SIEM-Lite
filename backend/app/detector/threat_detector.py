"""Detection engine that consumes already-parsed log entries."""

import json
import re
from collections import defaultdict, deque
from collections.abc import Generator, Iterable
from datetime import datetime
from pathlib import Path
from typing import Any


APACHE_TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


class ThreatDetector:
    """Run regex signatures and brute-force heuristics against log records."""

    def __init__(self, signatures_path: Path, threshold: int = 5, window_seconds: int = 300):
        """Load signatures and configure the failed-login behaviour rule."""
        with signatures_path.open(encoding="utf-8") as signature_file:
            raw_signatures = json.load(signature_file)
        self.signatures = [
            {**signature, "compiled_pattern": re.compile(signature["pattern"])}
            for signature in raw_signatures
        ]
        self.threshold = threshold
        self.window_seconds = window_seconds
        self.failed_attempts: dict[str, deque[datetime]] = defaultdict(deque)
        self.reported_windows: dict[str, datetime] = {}

    def inspect(self, entry: dict[str, Any]) -> Generator[dict[str, str], None, None]:
        """Yield all threats identified for one parsed entry.

        This layer accepts dictionaries only; it has no knowledge of raw log
        syntax and therefore remains independent of the parser.
        """
        for signature in self.signatures:
            if signature["compiled_pattern"].search(entry["path"]):
                yield self._create_event(entry, signature)
        brute_force_event = self._detect_brute_force(entry)
        if brute_force_event:
            yield brute_force_event

    @staticmethod
    def _create_event(entry: dict[str, Any], signature: dict[str, Any]) -> dict[str, str]:
        """Build the public detection schema shared by all detection types."""
        return {
            "type": signature["type"],
            "severity": signature["severity"],
            "description": signature["description"],
            "ip": entry["ip"],
            "timestamp": entry["timestamp"],
            "path": entry["path"],
        }

    def _detect_brute_force(self, entry: dict[str, Any]) -> dict[str, str] | None:
        """Detect repeated 401 responses for one IP within the configured window."""
        if entry["status"] != 401:
            return None
        try:
            attempt_time = datetime.strptime(entry["timestamp"], APACHE_TIMESTAMP_FORMAT)
        except ValueError:
            return None

        attempts = self.failed_attempts[entry["ip"]]
        cutoff = attempt_time.timestamp() - self.window_seconds
        while attempts and attempts[0].timestamp() < cutoff:
            attempts.popleft()
        attempts.append(attempt_time)

        previous_report = self.reported_windows.get(entry["ip"])
        if len(attempts) < self.threshold or previous_report == attempts[0]:
            return None
        self.reported_windows[entry["ip"]] = attempts[0]
        return {
            "type": "Brute Force",
            "severity": "high",
            "description": f"{len(attempts)} failed authentication attempts within {self.window_seconds} seconds.",
            "ip": entry["ip"],
            "timestamp": entry["timestamp"],
            "path": entry["path"],
        }


def create_detector(threshold: int, window_seconds: int) -> ThreatDetector:
    """Create a detector using the application-maintained signature file."""
    signatures_path = Path(__file__).with_name("signatures.json")
    return ThreatDetector(signatures_path, threshold, window_seconds)
