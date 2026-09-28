# Metrics

[Português (Brasil)](../pt-BR/metrics.md)

Version 1.0.2 separates raw endpoint acquisition from metrics whose semantics have already been validated.

## Parsed in 1.0.x

- BIND version and JSON statistics version;
- server uptime and time since the last configuration;
- IPv4 and IPv6 request rates;
- dropped-query, SERVFAIL and recursive-query rates;
- low-level discovery of `nsstats`, server incoming `qtypes`, `rcodes` and network `sockstats`;
- resolver discovery by view for resolver statistics, recursive query types and ADB counters;
- resolver cache metrics per view: hits/misses, hit ratio, query hits/misses, LRU/TTL deletions, covering NSEC, cache nodes and cache memory;
- BIND memory in use, malloced memory and memory-context count;
- aggregate zone counts (total, primary and secondary) without creating an item for every zone;
- secondary-zone refresh/expiry timers, local SOA serial and expiry warning/expired trigger prototypes;
- DNSSEC signing and refresh counters discovered only for zones that actually export `dnssec-sign`/`dnssec-refresh` statistics;
- aggregate UDP/TCP request and response rates derived from BIND traffic histograms.

## Raw endpoint retention

Raw HTTP/JSON endpoint items are preprocessing masters and use `history: 0`. Dependent items still receive the current master value, while the large raw payload itself is not written to history. This is particularly important for `/json/v1/zones` on servers with large zone inventories.

## Retention model

Raw JSON masters and the normalized zone dataset do not store history. Derived numeric items keep their normal history/trends, reducing database growth without removing operational metrics.

## Aggregate zone-count semantics

`bind.zones.total` counts every zone object exposed by the BIND statistics endpoint. `bind.zones.primary` and `bind.zones.secondary` count only those two specific zone types. BIND supports additional zone types such as hint, forward, stub, static-stub, mirror and redirect, so **total is not expected to equal primary + secondary**.

A future minor release may expose an additional "other zones" or per-type breakdown without changing the existing keys.

## Zone statistics level

The BIND zones endpoint can expose zone identity, serial and timer fields. Aggregate zone counts remain always available, while per-secondary refresh/expiry and local serial items are opt-in. DNSSEC per-zone counters require BIND zone statistics at the `full` level for the relevant zones. The DNSSEC discovery rule remains empty when those blocks are absent, so the common template does not create unsupported DNSSEC items.

## Incoming transfer monitoring

BIND 9.20 exposes the JSON `/json/v1/xfrins` endpoint. The common template polls this endpoint without forcing 9.18 hosts into an unsupported state. On versions without the endpoint, `bind.xfrins.supported` reports `0` and the transfer gauges remain zero. On BIND 9.20, the template collects active/queued transfer count, deferred transfers, current transfer bytes and aggregate transfer rate.

## Per-zone detail policy

The base template intentionally avoids discovering SOA serial and loaded age for every zone. The local serial is exposed only for secondary zones selected by `{$BIND.ZONE.SECONDARY.MATCHES}`. On authoritative servers with hundreds or thousands of zones, those items add substantial cardinality while providing little standalone health information. Secondary-zone expiry monitoring remains available per-zone because an individual secondary can expire independently, but it is opt-in through `{$BIND.ZONE.SECONDARY.MATCHES}` to keep the default template low-cardinality. Per-zone DNSSEC counters are opt-in through `{$BIND.ZONE.DNSSEC.MATCHES}`; the default `^$` discovers none. Set it to a targeted regular expression, or `.*` only when full per-zone DNSSEC detail is explicitly required.


## Counter versus gauge semantics

BIND statistics contain both monotonically increasing event counters and point-in-time gauges. Version 1.0.2 explicitly separates these classes so that gauges are never processed with `CHANGE_PER_SECOND`.

Rate families include cumulative query/request/response/error and socket-event counters. Gauge families include:

- `nsstats`: `RecursClients`, `TCPConnHighWater` and, on BIND 9.20, `RecursHighwater`;
- resolver statistics: `QueryCurUDP`, `QueryCurTCP`, `NumFetch` and `BucketSize`;
- resolver ADB: `nentries`, `entriescnt`, `nnames` and `namescnt`;
- socket statistics: active-socket and currently-connected-client values such as `UDP4Active`, `TCP4Active` and `TCP4Clients`.

The generic rate discovery rules exclude these gauges. Dedicated gauge discovery rules expose their current values directly. This prevents misleading values such as “RecursClients per second”.


## Independent service and capacity signals

The template now separates statistics-channel health from local daemon/listener health with `proc.num[{$BIND.PROCESS.NAME}]`, `net.tcp.listen[{$BIND.DNS.PORT}]` and `net.udp.listen[{$BIND.DNS.PORT}]`. It also promotes `RecursClients` to a dedicated gauge and exposes a per-view cache hit ratio.

The optional recursive-client and DeleteLRU saturation triggers default to disabled by using threshold value `0`; administrators enable them by choosing site-appropriate positive thresholds.
