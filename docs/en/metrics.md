# Metrics

[Português (Brasil)](../pt-BR/metrics.md)

The template separates raw endpoint acquisition from derived metrics and explicitly distinguishes **monotonic counters** from **current-value gauges**.

## Core service and identification

- BIND version and JSON statistics version;
- server uptime and time since the last configuration;
- DNS UDP/TCP functional availability through `net.dns[]`;
- DNS UDP/TCP response time through `net.dns.perf[]`.

## Query and server statistics

Fixed rate items include:

- IPv4 and IPv6 requests per second;
- dropped queries per second;
- SERVFAIL responses per second;
- recursive queries per second.

The generic `nsstats` discovery converts monotonic event counters to rates. Values that are not counters are deliberately excluded from rate conversion and collected as gauges instead:

- TCP connection high-water;
- recursive-client high-water;
- current recursive clients.

## Resolver metrics by view

Resolver monitoring is view-aware.

Monotonic resolver counters and recursive query types are discovered and converted to rates. Current-value resolver gauges are collected separately:

- UDP queries in progress;
- TCP queries in progress;
- active fetches;
- bucket size.

ADB values are gauges, not event counters. The template exposes:

- address hash-table size;
- addresses in the hash table;
- name hash-table size;
- names in the hash table.

## Resolver cache

Per-view cache metrics include:

**Rates**

- cache hits and misses;
- query hits and misses;
- LRU deletions;
- TTL deletions;
- covering NSEC results.

**Gauges**

- cache nodes;
- NSEC auxiliary nodes;
- cache tree memory in use;
- cache heap memory in use.

Graph prototypes provide hit/miss, memory and node views for every discovered resolver view.

## Socket statistics

The generic socket discovery converts monotonic socket events such as opens, closes, failures, connects, accepts, send errors and receive errors to rates.

Current socket state is collected separately as gauges:

- active UDP/IPv4 and UDP/IPv6 sockets;
- active TCP/IPv4 and TCP/IPv6 sockets;
- currently connected TCP/IPv4 and TCP/IPv6 clients.

## Memory

Common memory metrics are:

- memory in use;
- malloced memory;
- number of active memory contexts.

The `contexts` member is validated as a JSON array in both the test fixtures and live BIND contract checks.

## Zone inventory

The base template does not create an item for every zone. Aggregate inventory is split into:

- all zones;
- primary zones;
- secondary zones;
- built-in zones;
- other zone types such as mirror, stub, static-stub, DLZ or redirect when present.

This makes the total reconcilable without adding per-zone cardinality.

## Optional per-zone monitoring

Secondary-zone refresh/expiry monitoring is opt-in through `{$BIND.ZONE.SECONDARY.MATCHES}`.

DNSSEC signing/refresh counters are opt-in through `{$BIND.ZONE.DNSSEC.MATCHES}` and require the corresponding BIND zone statistics to be exported. If a per-zone source value disappears, preprocessing discards the transient value instead of leaving the item unsupported.

## Traffic

Aggregate UDP/TCP request and response rates are derived from the BIND traffic histograms for IPv4 and IPv6.

## Incoming transfers

BIND 9.20 exposes `/json/v1/xfrins`. The template collects:

- active/queued incoming transfer count;
- deferred incoming transfers;
- current bytes transferred;
- aggregate transfer rate.

`bind.xfrins.supported` reports whether the endpoint is available. On BIND 9.18, where the endpoint does not exist, transfer metric values are discarded rather than reported as false zero measurements.

## Raw endpoint retention

The following raw acquisitions use short history and no trends:

- `/json/v1/status`;
- `/json/v1/server`;
- `/json/v1/zones`;
- `/json/v1/mem`;
- `/json/v1/net`;
- `/json/v1/traffic`;
- `/json/v1/xfrins` when available.

Derived numeric items retain normal history/trends so raw JSON payloads do not unnecessarily increase the Zabbix database footprint.

## Cardinality policy

High-cardinality data is deliberately opt-in. The default template favors global health, protocol behavior and bounded per-view metrics. Per-zone detail is enabled only when the operator explicitly selects zones.
