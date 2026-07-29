import unittest

from src.parser import InvalidLogEntry, LogParser


class TestLogParser(unittest.TestCase):

    def setUp(self):
        self.parser = LogParser()

    def test_parse_valid_log_line(self):
        line = (
            '83.149.9.216 - - [17/May/2015:10:05:03 +0000] '
            '"GET /presentations/logstash.pdf HTTP/1.1" '
            '200 3478 '
            '"http://semicomplete.com/" '
            '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/32.0.1700.77 Safari/537.36"'
        )

        entry = self.parser.parse(line)

        self.assertEqual(entry.ip, "83.149.9.216")
        self.assertTrue(entry.user_agent.startswith("Mozilla/5.0"))
        self.assertIn("Chrome", entry.user_agent)

    def test_empty_line_raises(self):
        with self.assertRaises(InvalidLogEntry):
            self.parser.parse("")

    def test_malformed_line_raises(self):
        with self.assertRaises(InvalidLogEntry):
            self.parser.parse("this is not an apache log")

    def test_missing_user_agent_raises(self):
        line = (
            '83.149.9.216 - - [17/May/2015:10:05:03 +0000] '
            '"GET / HTTP/1.1" '
            '200 3478 '
            '"http://semicomplete.com/"'
        )

        with self.assertRaises(InvalidLogEntry):
            self.parser.parse(line)


if __name__ == "__main__":
    unittest.main()