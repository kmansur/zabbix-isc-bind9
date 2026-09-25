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
- aggregate zone counts (total, primary and secondary) without creating an item for every zone;
- secondary-zone refresh/expiry timers with expiry warning/expired trigger prototypes;
- DNSSEC signing and refresh counters discovered only for zones that actually export `dnssec-sign`/`dnssec-refresh` statistics;
- aggregate UDP/TCP request and response rates derived from BIND traffic histograms.

## Raw endpoint retention

The `/json/v1/mem` and `/json/v1/net` payloads remain available as short-retention master items. Stable common fields are parsed into dependent items, while version-specific fields remain unpromoted until compatibility is demonstrated.

## Retention model

Raw JSON master items use short history and no trends. Derived numeric items keep normal history/trends so the raw payload does not unnecessarily increase the Zabbix database footprint.

## Zone statistics level

Basic zone identity, serial and timer data are available without enabling full per-zone counters. DNSSEC per-zone counters require BIND zone statistics at the `full` level for the relevant zones. The DNSSEC discovery rule remains empty when those blocks are absent, so the common template does not create unsupported DNSSEC items.

## Incoming transfer monitoring

BIND 9.20 exposes the JSON `/json/v1/xfrins` endpoint. The common template polls this endpoint without forcing 9.18 hosts into an unsupported state. On versions without the endpoint, `bind.xfrins.supported` reports `0` and the transfer gauges remain zero. On BIND 9.20, the template collects active/queued transfer count, deferred transfers, current transfer bytes and aggregate transfer rate.

## Per-zone detail policy

The base template intentionally avoids discovering SOA serial and loaded age for every zone. On authoritative servers with hundreds or thousands of zones, those items add substantial cardinality while providing little standalone health information. Secondary-zone expiry monitoring remains available per-zone because an individual secondary can expire independently, but it is opt-in through `{$BIND.ZONE.SECONDARY.MATCHES}` to keep the default template low-cardinality. Per-zone DNSSEC counters are opt-in through `{$BIND.ZONE.DNSSEC.MATCHES}`; the default `^$` discovers none. Set it to a targeted regular expression, or `.*` only when full per-zone DNSSEC detail is explicitly required.
