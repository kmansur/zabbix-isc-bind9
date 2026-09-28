# Dashboard and graphs

[Português (Brasil)](../pt-BR/dashboard.md)

Version 1.0.2 provides a streamlined native Zabbix template dashboard and reusable classic graphs.

## Template dashboard

The dashboard is named **ISC BIND: Overview** and contains three pages.

### Overview

The first page is intended for day-to-day operations. It includes:

- BIND version;
- uptime;
- total, primary and secondary zone counts;
- memory in use;
- DNS UDP/TCP state;
- BIND JSON statistics version;
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
- local DNS response-time graph.

Detailed Query Type, Response Code and `nsstats` values remain available in Latest data, but are intentionally not listed as dashboard navigators to keep the operational view concise.

### Resolver & resources

This page focuses on recursive resolver behavior and resource-level diagnostics:

- resolver-cache graph prototypes per view for hit/miss rates, cache memory and cache nodes;
- memory graph;
- zone inventory;
- incoming transfers;
- transfer rate.

Detailed resolver, socket and per-zone items remain available in Latest data. Per-zone secondary and DNSSEC items remain opt-in through their macros.

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
- `BIND: DNS query response time`

These graphs are intentionally based on stable, low-cardinality items. Dynamic LLD families such as query types, response codes, resolver counters and socket counters remain available in Latest data without cluttering the dashboard.
