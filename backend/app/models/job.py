"""In-memory model for a completed log analysis."""

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AnalysisJob:
    """Represent one submitted log analysis and its dashboard data."""

    id: str
    source_name: str
    status: str = "processing"
    total_requests: int = 0
    malformed_lines: int = 0
    threats: list[dict[str, str]] = field(default_factory=list)
    status_distribution: dict[str, int] = field(default_factory=dict)
    attack_timeline: dict[str, int] = field(default_factory=dict)
    top_attackers: dict[str, int] = field(default_factory=dict)
    attack_categories: dict[str, int] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation for the API."""
        return asdict(self)
