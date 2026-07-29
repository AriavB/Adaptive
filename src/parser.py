import re

from src.models import LogEntry


class InvalidLogEntry(Exception):
    """Raised when a log line cannot be parsed."""


class LogParser:
    """Parses Apache Combined Log Format entries."""

    def parse(self, line: str) -> LogEntry:
        line = line.strip()

        if not line:
            raise InvalidLogEntry("Empty log line")

        # First token is always the client IP.
        ip = line.split(maxsplit=1)[0]

        # Combined Log Format contains: "request" "referer" "user-agent"
        quoted_fields = re.findall(r'"([^"]*)"', line)

        if len(quoted_fields) != 3:
            raise InvalidLogEntry("Invalid Apache log format")

        user_agent = quoted_fields[2]

        return LogEntry(
            ip=ip,
            user_agent=user_agent,
        )