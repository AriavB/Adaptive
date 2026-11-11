from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from src.parser import InvalidLogEntry


class LogProcessor:
    """Coordinates the log processing pipeline."""

    def __init__(self, parser, enricher, statistics, report_generator=None):
        self._parser = parser
        self._enricher = enricher
        self._statistics = statistics
        self._report_generator = report_generator

    def process(self, log_source: str | Path | Iterable[str]) -> str:
        invalid_lines = 0

        if isinstance(log_source, (str, Path)):
            with open(log_source, encoding="utf-8") as file:
                lines = file
                report = self._process_lines(lines, invalid_lines)
                return report

        report = self._process_lines(log_source, invalid_lines)
        return report

    def _process_lines(self, lines: Iterable[str], invalid_lines: int) -> str:
        for line in lines:
            try:
                entry = self._parser.parse(line)
            except InvalidLogEntry:
                invalid_lines += 1
                continue

            enriched = self._enricher.enrich(entry)
            self._statistics.add(enriched)

        if self._report_generator is None:
            return ""

        report = self._report_generator.generate(self._statistics)
        if invalid_lines:
            report += f"\n\nInvalid log entries skipped: {invalid_lines}"
        return report
