import tempfile
import unittest

from src.models import EnrichedLogEntry, LogEntry
from src.parser import InvalidLogEntry
from src.processor import LogProcessor
from src.statistics import StatisticsAggregator
from src.report_generator import ReportGenerator


class FakeParser:

    def parse(self, line):
        if line.startswith("INVALID"):
            raise InvalidLogEntry()

        return LogEntry(
            ip="1.1.1.1",
            user_agent="ua",
        )


class FakeEnricher:

    def enrich(self, entry):
        return EnrichedLogEntry(
            country="Israel",
            browser="Chrome",
            operating_system="Mac OS X",
        )


class TestProcessor(unittest.TestCase):

    def test_process_file(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
            file.write("line1\n")
            file.write("line2\n")
            path = file.name

        processor = LogProcessor(
            parser=FakeParser(),
            enricher=FakeEnricher(),
            statistics=StatisticsAggregator(),
            report_generator=ReportGenerator(),
        )

        report = processor.process(path)

        self.assertIn("Countries", report)
        self.assertIn("Israel: 100.00%", report)
        self.assertIn("Chrome: 100.00%", report)

    def test_skips_invalid_lines(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
            file.write("line1\n")
            file.write("INVALID\n")
            path = file.name

        processor = LogProcessor(
            parser=FakeParser(),
            enricher=FakeEnricher(),
            statistics=StatisticsAggregator(),
            report_generator=ReportGenerator(),
        )

        report = processor.process(path)

        self.assertIn("Invalid log entries skipped: 1", report)


if __name__ == "__main__":
    unittest.main()