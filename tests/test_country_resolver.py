import unittest

from src.country_resolver import CountryResolver


class TestCountryResolver(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.resolver = CountryResolver(
            "data/GeoLite2-Country.mmdb"
        )

    def test_resolve_known_ip(self):
        country = self.resolver.resolve("83.149.9.216")

        self.assertNotEqual(country, "Other")

    def test_unknown_ip_returns_other(self):
        country = self.resolver.resolve(
            "192.0.2.1"  # TEST-NET-1 reserved range
        )

        self.assertEqual(country, "Other")

    def test_repeated_lookup_returns_same_result(self):
        first = self.resolver.resolve("83.149.9.216")
        second = self.resolver.resolve("83.149.9.216")

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()