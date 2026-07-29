import unittest

from src.user_agent_parser import UserAgentParser


class TestUserAgentParser(unittest.TestCase):

    def setUp(self):
        self.parser = UserAgentParser()

    def test_parse_chrome_on_mac(self):
        user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/32.0.1700.77 Safari/537.36"
        )

        browser, operating_system = self.parser.parse(user_agent)

        self.assertEqual(browser, "Chrome")
        self.assertEqual(operating_system, "Mac OS X")

    def test_parse_firefox_on_windows(self):
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "Gecko/20100101 Firefox/115.0"
        )

        browser, operating_system = self.parser.parse(user_agent)

        self.assertEqual(browser, "Firefox")
        self.assertEqual(operating_system, "Windows")

    def test_parse_safari_on_iphone_googlebot(self):
        user_agent = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) "
            "AppleWebKit/536.26 (KHTML, like Gecko) "
            "Version/6.0 Mobile/10A5376e Safari/8536.25 "
            "(compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        )

        browser, operating_system = self.parser.parse(user_agent)

        self.assertEqual(browser, "Googlebot")
        self.assertEqual(operating_system, "iOS")

    def test_parse_feed_reader(self):
        user_agent = (
            "Tiny Tiny RSS/1.11 (http://tt-rss.org/)"
        )

        browser, operating_system = self.parser.parse(user_agent)

        self.assertEqual(browser, "Tiny Tiny RSS")
        self.assertEqual(operating_system, "Other")

    def test_parse_feed_parser(self):
        user_agent = (
            "UniversalFeedParser/4.2-pre-314-svn "
            "+http://feedparser.org/"
        )

        browser, operating_system = self.parser.parse(user_agent)

        self.assertEqual(browser, "Other")
        self.assertEqual(operating_system, "Other")

    def test_unknown_user_agent_returns_other(self):
        browser, operating_system = self.parser.parse(
            "some-random-client"
        )

        self.assertEqual(browser, "Other")
        self.assertEqual(operating_system, "Other")


if __name__ == "__main__":
    unittest.main()