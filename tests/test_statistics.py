import unittest

from src.models import EnrichedLogEntry
from src.statistics import StatisticsAggregator


class TestStatisticsAggregator(unittest.TestCase):

    def test_aggregate_counts(self):
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

        self.assertEqual(stats.total_requests, 3)

        self.assertEqual(stats.country_counts["Israel"], 2)
        self.assertEqual(stats.country_counts["United States"], 1)

        self.assertEqual(stats.browser_counts["Chrome"], 2)
        self.assertEqual(stats.browser_counts["Firefox"], 1)

        self.assertEqual(stats.operating_system_counts["Mac OS X"], 2)
        self.assertEqual(stats.operating_system_counts["Windows"], 1)


if __name__ == "__main__":
    unittest.main()