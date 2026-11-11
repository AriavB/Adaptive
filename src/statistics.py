from __future__ import annotations

from collections import Counter
from collections.abc import Callable

from src.models import EnrichedLogEntry


class DimensionSpec:
    def __init__(self, name: str, value_getter: Callable[[EnrichedLogEntry], str]):
        self.name = name
        self.value_getter = value_getter


class StatisticsAggregator:
    """Aggregates request counts for any registered reporting dimension."""

    def __init__(self):
        self._dimension_specs: dict[str, DimensionSpec] = {}
        self._counts: dict[str, Counter[str]] = {}
        self._total_requests = 0

        self.register_dimension("country", lambda entry: entry.country)
        self.register_dimension("browser", lambda entry: entry.browser)
        self.register_dimension("operating_system", lambda entry: entry.operating_system)

    def register_dimension(self, name: str, value_getter: Callable[[EnrichedLogEntry], str]) -> None:
        spec = DimensionSpec(name=name, value_getter=value_getter)
        self._dimension_specs[name] = spec
        self._counts.setdefault(name, Counter())

    @property
    def total_requests(self) -> int:
        return self._total_requests

    @property
    def dimension_names(self) -> tuple[str, ...]:
        return tuple(self._dimension_specs)

    def counts_for(self, name: str) -> Counter[str]:
        return self._counts[name]

    def add(self, entry: EnrichedLogEntry) -> None:
        self._total_requests += 1
        for name, spec in self._dimension_specs.items():
            self._counts[name][spec.value_getter(entry)] += 1

    @property
    def country_counts(self):
        return self._counts["country"]

    @property
    def browser_counts(self):
        return self._counts["browser"]

    @property
    def operating_system_counts(self):
        return self._counts["operating_system"]

    def as_dict(self) -> dict[str, dict[str, int]]:
        return {name: dict(counter) for name, counter in self._counts.items()}

    def dimension_title(self, name: str) -> str:
        aliases = {
            "country": "Countries",
            "browser": "Browsers",
            "operating_system": "Operating Systems",
        }
        if name in aliases:
            return aliases[name]
        return name.replace("_", " ").title()
