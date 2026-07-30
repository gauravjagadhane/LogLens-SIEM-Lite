"""Streaming Apache and Nginx access-log parser.

Both Apache Common/Combined and the usual Nginx access format use the same
request/status core. The final quoted user-agent field is optional, allowing
Common Log Format lines to be parsed as well.
"""

import re
from collections.abc import Generator, Iterable
from typing import Any


LOG_LINE_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+(?P<protocol>[^"\s]+)"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\S+)'
    r'(?:\s+"[^"]*"\s+"(?P<user_agent>[^"]*)")?\s*$'
)


class LogParseError(ValueError):
    """Raised when a file does not resemble a supported access log."""


def parse_log_line(line: str) -> dict[str, Any] | None:
    """Parse one access-log line, returning ``None`` for malformed lines.

    Keeping malformed rows non-fatal makes an analysis resilient to partially
    corrupted files while the caller still records their count.
    """
    match = LOG_LINE_PATTERN.match(line)
    if not match:
        return None

    fields = match.groupdict()
    size_text = fields["size"]
    return {
        "ip": fields["ip"],
        "timestamp": fields["timestamp"],
        "method": fields["method"],
        "path": fields["path"],
        "protocol": fields["protocol"],
        "status": int(fields["status"]),
        "size": 0 if size_text == "-" else int(size_text),
        "user_agent": fields["user_agent"] or "",
    }


def parse_access_log(lines: Iterable[str]) -> Generator[dict[str, Any], None, None]:
    """Yield parsed records one at a time from an iterable of text lines.

    The generator deliberately keeps no list of entries, so callers can handle
    files that are much larger than the server's available memory.
    """
    for line in lines:
        if not line.strip():
            continue
        entry = parse_log_line(line)
        if entry is not None:
            yield entry
