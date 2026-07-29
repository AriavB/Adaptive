# Apache Log Statistics

A simple module that processes an Apache access log and generates a statistical report showing the percentage of requests by:

- Country
- Operating System
- Browser / Client

The implementation is intentionally kept small, readable, and easy to extend while focusing on the assignment requirements.

---

## MVP

The module:

- Reads an Apache log file line by line (streaming).
- Extracts the client IP address and User-Agent from each request.
- Resolves:
  - Country (using a GeoIP database)
  - Operating System
  - Browser / Client
- Aggregates request counts.
- Produces a percentage breakdown for each dimension.

The implementation processes the file synchronously and keeps only aggregated statistics in memory.

---

## Design

Each component has a single responsibility, making the pipeline easy to understand, test, and extend.
Log -> Log Reader -> Log Parser -> Country Resolver -> User Agent Parser -> Statistics Aggregator -> Report Generator
---

## Key Abstractions

### LogParser

Parses an Apache log line into a structured `LogEntry`.

Responsible for:

- extracting IP address
- extracting User-Agent
- handling malformed log lines

---

### CountryResolver

Maps an IP address to a country using a GeoIP database.

Returns `Other` when a lookup cannot be performed or the country cannot be identified.

---

### GeoIP Lookup Cache

To avoid repeated GeoIP lookups for the same client IP, the `CountryResolver` maintains a small bounded in-memory LRU cache.

This optimization takes advantage of the fact that Apache logs often contain repeated requests from the same IP addresses. Cached lookups reduce repeated GeoIP database reads while keeping memory usage bounded.

The cache is internal to the resolver and does not affect the overall processing pipeline or component responsibilities.

---

### UserAgentParser

Extracts:

- Browser / Client
- Operating System

from the User-Agent string.

Returns `Other` when the parser cannot identify the value.

The implementation relies on a User-Agent parsing library. Unsupported clients (for example custom crawlers or feed readers) are expected and categorized as `Other` when no classification is available.

---

### StatisticsAggregator

Maintains counts for each dimension.

Responsible only for aggregation—not parsing or formatting.

---

### ReportGenerator

Calculates percentages and renders the final report.

The reporting logic is isolated from the aggregation logic, allowing multiple output formats in the future.

---

## Assumptions

- Input is a single Apache access log.
- Processing is performed offline.
- A local GeoIP database is available.
- Standard User-Agent parsing libraries may be used.
- Malformed log lines are skipped.
- Unknown countries, browsers, or operating systems are grouped under `Other`.

---

## Design Decisions

- **Streaming processing** keeps memory usage low regardless of file size.
- **Synchronous execution** was chosen because the workload is sequential and does not benefit significantly from concurrency.
- **Composition over abstraction**: only components with distinct responsibilities were introduced; unnecessary interfaces and design patterns were intentionally avoided.

---

## Error Handling

The implementation distinguishes between expected data quality issues and unexpected failures.

Expected issues:

- malformed log lines
- unknown IP addresses
- unsupported User-Agent strings

These are handled gracefully:
- malformed entries are skipped
- unknown enrichment values are categorized as `Other`

Unexpected failures:

- corrupted GeoIP database
- programming errors
- invalid application state

These are surfaced rather than silently ignored.

---

## Testing Strategy

The solution uses layered testing:

### Unit tests

Cover individual components:

- Apache log parsing
- User-Agent parsing
- GeoIP resolution
- Statistics aggregation
- Report generation

### Integration test

Validates the flow from:
Raw log line -> Parser -> Enricher -> Enriched Log Model
External dependencies are tested through their boundaries to keep tests deterministic and focused.

---

## Trade-offs and Non-Goals

The solution intentionally avoids:

- Distributed processing, since the workload is a single offline file.
- Async processing, since the workflow is sequential and dominated by local parsing and aggregation.
- Persistent storage, since only aggregated statistics are required.
- Complex validation frameworks, since the input format is known.

If requirements changed to support continuous ingestion, multiple log sources, or very large-scale processing, the architecture could evolve toward a streaming pipeline with persistent aggregation.

---

## Extensibility

The pipeline separates **parsing**, **enrichment**, **aggregation**, and **report generation**, making it straightforward to extend.

### Additional dimensions

New dimensions (for example Device Type, HTTP Method, Status Code, or Referrer) can be added by:

1. extracting the new attribute during parsing or enrichment
2. adding the corresponding aggregation counter
3. including it in the report

No changes to the processing workflow are required.

### Additional output formats

The current implementation prints a text report.

Future report generators could output:

- JSON
- CSV
- HTML
- Markdown

without modifying the aggregation logic.

---

## Complexity

| Operation | Complexity |
|-----------|------------|
| Processing | O(n) |
| Memory | O(k) |

Where:

- **n** = number of log entries
- **k** = number of unique values across the reported dimensions

Since the number of countries, browsers, and operating systems is bounded, memory usage remains effectively constant relative to the input size.