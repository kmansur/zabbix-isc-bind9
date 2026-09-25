# Metrics

[Português (Brasil)](../pt-BR/metrics.md)

Version 0.1.0 separates raw endpoint acquisition from metrics whose semantics have already been validated.

## Parsed in 0.1.0

- BIND version and JSON statistics version;
- server uptime and time since the last configuration;
- IPv4 and IPv6 request rates;
- dropped-query, SERVFAIL and recursive-query rates;
- low-level discovery of `nsstats`, authoritative `qtypes`, `rcodes` and network `sockstats`;
- resolver discovery by view for resolver statistics, recursive query types and ADB counters;
- resolver cache metrics per view: hits/misses, query hits/misses, LRU/TTL deletions, covering NSEC, cache nodes and cache memory;
- BIND memory in use, malloced memory and memory-context count;
- zone discovery across views, including zone type, SOA serial and loaded age;
- aggregate UDP/TCP request and response rates derived from BIND traffic histograms.

## Raw endpoint retention

The `/json/v1/mem` and `/json/v1/net` payloads remain available as short-retention master items. Stable common fields are parsed into dependent items, while version-specific fields remain unpromoted until compatibility is demonstrated.

## Retention model

Raw JSON master items use short history and no trends. Derived numeric items keep normal history/trends so the raw payload does not unnecessarily increase the Zabbix database footprint.
