import unittest

from src.enricher import LogEnricher
from src.models import LogEntry


class FakeCountryResolver:

    def resolve(self, ip: str):
        self.last_ip = ip
        return "Israel"


class FakeUserAgentParser:

    def parse(self, user_agent: str):
        self.last_user_agent = user_agent
        return ("Chrome", "Mac OS X")


class TestLogEnricher(unittest.TestCase):

    def setUp(self):
        self.country = FakeCountryResolver()
        self.ua = FakeUserAgentParser()

        self.enricher = LogEnricher(
            self.country,
            self.ua,
        )

    def test_enrich(self):
        entry = LogEntry(
            ip="1.2.3.4",
            user_agent="Mozilla/5.0",
        )

        enriched = self.enricher.enrich(entry)

        self.assertEqual(enriched.country, "Israel")
        self.assertEqual(enriched.browser, "Chrome")
        self.assertEqual(enriched.operating_system, "Mac OS X")

        self.assertEqual(self.country.last_ip, "1.2.3.4")
        self.assertEqual(self.ua.last_user_agent, "Mozilla/5.0")