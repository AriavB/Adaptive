from src.statistics import StatisticsAggregator


class ReportGenerator:
    """Generates a statistical report from aggregated request counts."""

    def generate(self, statistics: StatisticsAggregator) -> str:
        sections = [
            self._generate_section("Countries", statistics.country_counts, statistics.total_requests),
            self._generate_section("Operating Systems", statistics.operating_system_counts, statistics.total_requests),
            self._generate_section("Browsers", statistics.browser_counts, statistics.total_requests),
        ]

        return "\n\n".join(sections)

    def _generate_section(self, title: str, counts: dict[str, int], total: int) -> str:
        lines = [title, "-" * len(title)]

        for name, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
            percentage = (count / total) * 100 if total else 0
            lines.append(f"{name}: {percentage:.2f}%")

        return "\n".join(lines)