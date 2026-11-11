from __future__ import annotations

from functools import lru_cache

from user_agents import parse


class UserAgentParser:
    @lru_cache(maxsize=4096)
    def parse(self, user_agent: str) -> tuple[str, str]:
        ua = parse(user_agent)
        browser = ua.browser.family or "Other"
        operating_system = ua.os.family or "Other"
        return browser, operating_system
