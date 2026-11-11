from __future__ import annotations

import argparse
from pathlib import Path

from src.country_resolver import CountryResolver
from src.enricher import LogEnricher
from src.parser import LogParser
from src.processor import LogProcessor
from src.report_generator import ReportGenerator
from src.statistics import StatisticsAggregator
from src.user_agent_parser import UserAgentParser


ROOT = Path(__file__).resolve().parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate request statistics from an Apache access log."
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=ROOT / "input" / "apache_log.txt",
        help="Path to the Apache log file to analyze.",
    )
    parser.add_argument(
        "--geoip-database",
        type=Path,
        default=ROOT / "data" / "GeoLite2-Country.mmdb",
        help="Path to the MaxMind GeoLite2 Country database.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    processor = LogProcessor(
        parser=LogParser(),
        enricher=LogEnricher(CountryResolver(args.geoip_database), UserAgentParser()),
        statistics=StatisticsAggregator(),
        report_generator=ReportGenerator(),
    )

    print(processor.process(args.log_file))


if __name__ == "__main__":
    main()
