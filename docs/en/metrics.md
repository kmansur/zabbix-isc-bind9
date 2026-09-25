# Metrics

[Português (Brasil)](../pt-BR/metrics.md)

Version 0.1.0 separates raw endpoint acquisition from metrics whose semantics have already been validated.

## Parsed in 0.1.0

- BIND version and JSON statistics version;
- server uptime and time since the last configuration;
- IPv4 and IPv6 request rates;
- dropped-query, SERVFAIL and recursive-query rates;
- low-level discovery of `nsstats`, `qtypes`, `rcodes` and `sockstats`;
- zone discovery across views, including zone type, SOA serial and loaded age;
- aggregate UDP/TCP request and response rates derived from BIND traffic histograms.

## Collected raw for staged implementation

- `/json/v1/mem`;
- `/json/v1/net`.

These blocks are intentionally collected without production triggers until their exact fields and semantics are validated across the supported BIND branches.

## Retention model

Raw JSON master items use short history and no trends. Derived numeric items keep normal history/trends so the raw payload does not unnecessarily increase the Zabbix database footprint.
