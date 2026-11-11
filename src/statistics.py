from __future__ import annotations

from collections import Counter

from src.models import EnrichedLogEntry


class StatisticsAggregator:
    """Aggregates request counts by reporting dimensions."""

    def __init__(self) -> None:
        self._country_counts: Counter[str] = Counter()
        self._browser_counts: Counter[str] = Counter()
        self._operating_system_counts: Counter[str] = Counter()
        self._total_requests = 0

    def add(self, entry: EnrichedLogEntry) -> None:
        self._country_counts[entry.country] += 1
        self._browser_counts[entry.browser] += 1
        self._operating_system_counts[entry.operating_system] += 1
        self._total_requests += 1

    @property
    def total_requests(self) -> int:
        return self._total_requests

    @property
    def country_counts(self) -> dict[str, int]:
        return dict(self._country_counts)

    @property
    def browser_counts(self) -> dict[str, int]:
        return dict(self._browser_counts)

    @property
    def operating_system_counts(self) -> dict[str, int]:
        return dict(self._operating_system_counts)
