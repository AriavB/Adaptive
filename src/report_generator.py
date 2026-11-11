from __future__ import annotations

from typing import Mapping

from src.statistics import StatisticsAggregator


class ReportGenerator:
    """Generates a statistical report from aggregated request counts."""

    def generate(self, statistics: StatisticsAggregator) -> str:
        total = statistics.total_requests
        sections = [
            self._generate_section("Countries", statistics.country_counts, total),
            self._generate_section(
                "Operating Systems",
                statistics.operating_system_counts,
                total,
            ),
            self._generate_section("Browsers", statistics.browser_counts, total),
        ]
        return "\n\n".join(sections)

    @staticmethod
    def _generate_section(title: str, counts: Mapping[str, int], total: int) -> str:
        lines = [title, "-" * len(title)]
        for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            percentage = (count / total) * 100 if total else 0
            lines.append(f"{name}: {percentage:.2f}%")
        return "\n".join(lines)
