from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LogEntry:
    ip: str
    user_agent: str


@dataclass(frozen=True, slots=True)
class EnrichedLogEntry:
    country: str
    operating_system: str
    browser: str
