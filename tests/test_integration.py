import unittest

from src.country_resolver import CountryResolver
from src.enricher import LogEnricher
from src.parser import LogParser
from src.user_agent_parser import UserAgentParser


class TestPipelineIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        resolver = CountryResolver("data/GeoLite2-Country.mmdb")
        ua_parser = UserAgentParser()

        cls.enricher = LogEnricher(resolver, ua_parser)
        cls.parser = LogParser()

    def test_raw_log_to_enriched_entry(self):
        line = (
            '83.149.9.216 - - [17/May/2015:10:05:03 +0000] '
            '"GET /presentations/logstash.pdf HTTP/1.1" '
            '200 3478 '
            '"http://semicomplete.com/" '
            '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/32.0.1700.77 Safari/537.36"'
        )

        log_entry = self.parser.parse(line)
        enriched = self.enricher.enrich(log_entry)
        
        self.assertEqual(enriched.browser, "Chrome")
        self.assertEqual(enriched.operating_system, "Mac OS X")
        self.assertNotEqual(enriched.country, "Other")


if __name__ == "__main__":
    unittest.main()