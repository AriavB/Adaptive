from user_agents import parse


class UserAgentParser:

    def parse(self, user_agent: str) -> tuple[str, str]:
        ua = parse(user_agent)

        browser = ua.browser.family
        operating_system = ua.os.family

        return browser, operating_system