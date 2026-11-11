from __future__ import annotations

from src.statistics import StatisticsAggregator


class ReportGenerator:
    """Generates a statistical report from aggregated request counts."""

    def generate(self, statistics: StatisticsAggregator) -> str:
        sections = [
            self._generate_section(
                statistics.dimension_title(name),
                statistics.counts_for(name),
                statistics.total_requests,
            )
            for name in statistics.dimension_names
        ]
        return "\n\n".join(sections)

    def _generate_section(self, title: str, counts: dict[str, int], total: int) -> str:
        lines = [title, "-" * len(title)]

        for name, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
            percentage = (count / total) * 100 if total else 0
            lines.append(f"{name}: {percentage:.2f}%")

        return "\n".join(lines)
