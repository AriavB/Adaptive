# Apache Log Statistics

A small, streaming Python application that analyzes Apache access logs and reports the percentage of requests by country, browser, and operating system.

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Then run the application against a log file and a GeoIP database:

```bash
python main.py --log-file input/apache_log.txt --geoip-database data/GeoLite2-Country.mmdb
```

The flags default to repository-relative locations, but both paths are configurable for production usage and CI pipelines.

## Overview

The workflow is intentionally modular:

- Log parsing
- Client IP enrichment via GeoIP lookup
- User-Agent classification
- Aggregation of counts
- Final report generation

Entries with malformed log lines are skipped and counted as invalid. Unknown countries and unsupported user agents are normalized to `Other` instead of failing the entire pipeline.

## Testing

Run the full test suite with:

```bash
python -m unittest discover -s tests
```
