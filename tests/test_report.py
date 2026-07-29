import unittest

from src.models import EnrichedLogEntry
from src.report_generator import ReportGenerator
from src.statistics import StatisticsAggregator


class TestReportGenerator(unittest.TestCase):

    def test_generate_report(self):
        stats = StatisticsAggregator()

        stats.add(
            EnrichedLogEntry(
                country="Israel",
                browser="Chrome",
                operating_system="Mac OS X",
            )
        )

        stats.add(
            EnrichedLogEntry(
                country="Israel",
                browser="Chrome",
                operating_system="Mac OS X",
            )
        )

        stats.add(
            EnrichedLogEntry(
                country="United States",
                browser="Firefox",
                operating_system="Windows",
            )
        )

        report = ReportGenerator().generate(stats)

        self.assertIn("Countries", report)
        self.assertIn("Operating Systems", report)
        self.assertIn("Browsers", report)

        self.assertIn("Israel: 66.67%", report)
        self.assertIn("United States: 33.33%", report)

        self.assertIn("Chrome: 66.67%", report)
        self.assertIn("Firefox: 33.33%", report)

        self.assertIn("Mac OS X: 66.67%", report)
        self.assertIn("Windows: 33.33%", report)


if __name__ == "__main__":
    unittest.main()