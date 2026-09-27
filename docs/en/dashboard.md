# Dashboard and graphs

[Português (Brasil)](../pt-BR/dashboard.md)

Version 0.4.0 adds a native Zabbix template dashboard and reusable classic graphs.

## Template dashboard

The dashboard is named **ISC BIND: Overview** and contains three pages.

### Overview

The first page is intended for day-to-day operations. It includes:

- BIND version;
- uptime;
- total, primary and secondary zone counts;
- memory in use;
- DNS UDP/TCP state;
- local DNS response-time graph;
- query-rate graph;
- query-error graph;
- DNS transport traffic graph;
- memory graph;
- server timing graph;
- incoming-transfer graph;
- current problems.

### DNS activity

This page focuses on request behavior and DNS protocol results:

- IPv4, IPv6 and recursive query rates;
- SERVFAIL and dropped-query rates;
- UDP/TCP request and response rates;
- dynamic Query Type navigator;
- dynamic Response Code navigator;
- dynamic server `nsstats` navigator.

The navigators use template item tags, so counters discovered by LLD appear automatically without requiring a dashboard redesign.

### Resolver & resources

This page focuses on recursive resolver behavior and resource-level diagnostics:

- resolver counters grouped by BIND view;
- resolver-cache graph prototypes per view for hit/miss rates, cache memory and cache nodes;
- socket statistics;
- memory graph;
- zone inventory;
- incoming transfers;
- transfer rate;
- zone-related item navigator.

Per-zone secondary and DNSSEC items remain opt-in. When enabled through their macros, discovered zone items automatically appear in the zone-related navigator.

## Classic graphs

The template also provides reusable graphs outside the dashboard:

- `BIND: Query rates`
- `BIND: Query errors`
- `BIND: DNS transport traffic`
- `BIND: Memory usage`
- `BIND: Zone inventory`
- `BIND: Incoming transfers`
- `BIND: Incoming transfer rate`
- `BIND: Server timing`

These graphs are intentionally based on stable, low-cardinality items. Dynamic LLD families such as query types, response codes, resolver counters and socket counters are presented through dashboard navigators instead of generating large numbers of graph prototypes.
