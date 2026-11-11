from src.country_resolver import CountryResolver
from src.enricher import LogEnricher
from src.parser import LogParser
from src.processor import LogProcessor
from src.report_generator import ReportGenerator
from src.statistics import StatisticsAggregator
from src.user_agent_parser import UserAgentParser


LOG_FILE = "input/apache_log.txt"
GEOIP_DATABASE = "data/GeoLite2-Country.mmdb"


def main() -> None:
    processor = LogProcessor(
        parser=LogParser(),
        enricher=LogEnricher(CountryResolver(GEOIP_DATABASE), UserAgentParser()),
        statistics=StatisticsAggregator(),
        report_generator=ReportGenerator(),
    )

    with open(LOG_FILE, encoding="utf-8") as handle:
        report = processor.process(handle)

    print(report)


if __name__ == "__main__":
    main()
