from __future__ import annotations

import re

from src.models import LogEntry


class InvalidLogEntry(ValueError):
    """Raised when a log line cannot be parsed."""


class LogParser:
    """Parses Apache Combined Log Format entries."""

    _APACHE_COMBINED_RE = re.compile(
        r'^(?P<ip>\S+)\s+\S+\s+\S+\s+\[[^\]]+\]\s+'
        r'"(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+(?P<protocol>[^"]+)"\s+'
        r'(?P<status>\d{3})\s+\S+\s+'
        r'"(?P<referer>[^"]*)"\s+'
        r'"(?P<user_agent>[^"]*)"\s*$'
    )

    def parse(self, line: str) -> LogEntry:
        cleaned = line.strip()
        if not cleaned:
            raise InvalidLogEntry("Empty log line")

        match = self._APACHE_COMBINED_RE.match(cleaned)
        if match is None:
            raise InvalidLogEntry(f"Invalid Apache log format: {line!r}")

        return LogEntry(
            ip=match.group("ip"),
            user_agent=match.group("user_agent"),
        )
