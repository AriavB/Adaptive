from __future__ import annotations

from pathlib import Path

from src.parser import InvalidLogEntry


class LogProcessor:
    """Coordinates the log-processing pipeline while keeping memory bounded."""

    def __init__(self, parser, enricher, statistics, report_generator) -> None:
        self._parser = parser
        self._enricher = enricher
        self._statistics = statistics
        self._report_generator = report_generator

    def process(self, log_file: str | Path) -> str:
        invalid_lines = 0

        with Path(log_file).open("r", encoding="utf-8") as file:
            for line in file:
                try:
                    entry = self._parser.parse(line)
                except InvalidLogEntry:
                    invalid_lines += 1
                    continue

                enriched = self._enricher.enrich(entry)
                self._statistics.add(enriched)

        report = self._report_generator.generate(self._statistics)
        if invalid_lines:
            report += f"\n\nInvalid log entries skipped: {invalid_lines}"
        return report
