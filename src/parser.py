import ipaddress
import re

from src.models import LogEntry


class InvalidLogEntry(ValueError):
    """Raised when a log line cannot be parsed into a valid entry."""


_LOG_PATTERN = re.compile(
    r'^\s*(?P<ip>\S+)\s+\S+\s+\S+\s+\[[^\]]+\]\s+\"(?:\\.|[^"\\])*\"\s+\S+\s+\S+\s+\"(?:\\.|[^"\\])*\"\s+\"(?P<user_agent>(?:\\.|[^"\\])*)\"\s*$'
)


def _normalize_user_agent(raw_user_agent: str) -> str:
    """Unescape backslash-escaped quotes within the User-Agent field."""
    return re.sub(r'\\([\\"])', r'\1', raw_user_agent)


class LogParser:
    """Parses Apache Combined Log Format entries."""

    def parse(self, line: str) -> LogEntry:
        text = line.strip()
        if not text:
            raise InvalidLogEntry("Empty log line")

        match = _LOG_PATTERN.fullmatch(text)
        if match is None:
            raise InvalidLogEntry("Invalid Apache log format")

        ip = match.group("ip")
        try:
            ipaddress.ip_address(ip)
        except ValueError as exc:
            raise InvalidLogEntry(f"Invalid client IP address: {ip!r}") from exc

        return LogEntry(
            ip=ip,
            user_agent=_normalize_user_agent(match.group("user_agent")),
        )
