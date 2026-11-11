from __future__ import annotations

from collections.abc import Callable

from src.models import EnrichedLogEntry, LogEntry


class LogEnricher:
    def __init__(self, country_resolver, user_agent_parser):
        self._country_resolver = country_resolver
        self._user_agent_parser = user_agent_parser

    def enrich(self, entry: LogEntry) -> EnrichedLogEntry:
        browser, operating_system = self._user_agent_parser.parse(entry.user_agent)
        return EnrichedLogEntry(
            country=self._country_resolver.resolve(entry.ip),
            browser=browser,
            operating_system=operating_system,
        )
