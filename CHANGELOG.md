# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

No unreleased changes.

## [1.0.1] - 2026-09-28

### Changed

- Removed all `Item navigator` widgets from the template dashboard after real-use validation showed that the long Query Type, Response Code, `nsstats`, resolver, socket and zone lists added visual noise without improving day-to-day operations.
- Reorganized the **DNS activity** page around query rates, query errors, DNS transport traffic and DNS response time.
- Reorganized **Resolver & resources** around resolver-cache graph prototypes, memory, zone inventory and transfer graphs.
- Detailed LLD values remain available through Latest data without being forced into the operational dashboard.

## [1.0.0] - 2026-09-28

First production-stable release of **ISC BIND by Zabbix agent**.

### Validation

- Real runtime validation on Ubuntu 24.04 with BIND 9.18.39 and the classic Zabbix agent.
- Native UDP/TCP DNS availability and response-time checks validated in the real environment; local response times were below 1 ms.
- Live statistics-channel contract validation against the official ISC BIND 9.18.50 and 9.20.29 container images.
- Version-aware validation confirms that `/json/v1/xfrins` is absent on BIND 9.18 and available on BIND 9.20.
- Classic Zabbix Agent and Zabbix Agent 2 capability checks run against live BIND instances in CI.
- Fresh-import gates for Zabbix 7.0 and the official Zabbix 8.0 trunk development images.
- Python 3.11, 3.13 and 3.14 lint, formatting, pytest, template validation and bilingual-documentation validation.
- BIND 9.18/9.20 JSON contract fixtures protect preprocessing and LLD assumptions.
- Full functional parity is enforced between the 7.0 and 8.0 template bodies and graph definitions.
- Passive-template cleanup audit confirms no legacy active item types, old BIND9 macros, old LLD macros, legacy port 8653, shared item keys or shared UUIDs remain from the community source.

### Added

- Native UDP/TCP DNS availability and response-time monitoring with `net.dns[]` and `net.dns.perf[]`.
- BIND version, JSON statistics version, uptime and configuration-age monitoring.
- IPv4/IPv6 request, recursion, dropped-query and SERVFAIL rates.
- LLD for `nsstats`, query types, response codes and socket statistics.
- Resolver statistics, query types, ADB and cache metrics by BIND view.
- Memory usage, malloced memory and memory-context monitoring.
- Aggregate total/primary/secondary zone counters.
- Opt-in secondary-zone refresh/expiry monitoring with trigger prototypes.
- Opt-in per-zone DNSSEC signing/refresh counters.
- BIND 9.20 incoming-transfer monitoring via `/json/v1/xfrins`, with graceful BIND 9.18 compatibility.
- Nine reusable classic graphs.
- Three resolver-cache graph prototypes per view.
- Native three-page `ISC BIND: Overview` dashboard with Overview, DNS activity, and Resolver & resources pages.
- Dynamic dashboard navigators for query types, response codes, nsstats, resolver counters, socket statistics and zone-related items.
- CI, CodeQL, repository-hygiene tests and bilingual English/pt-BR documentation.

### Changed

- Template identity standardized as `ISC BIND by Zabbix agent`.
- Passive Zabbix agent checks are the default architecture; `ServerActive` is not required.
- Statistics-channel unavailability is a Warning because DNS service availability is checked independently.
- SERVFAIL and dropped-query anomalies are Warnings and depend on statistics-channel availability.
- Per-zone monitoring is opt-in to keep default cardinality low.
- Optional zero-valued BIND counters are normalized or safely omitted rather than producing unsupported noise.
- Socket statistics discovery uses `/json/v1/net`, matching BIND semantics.
- `{$BIND.STATS.HOST}` uses `127.0.0.1` rather than a full URL because path and port are supplied separately to `web.page.get[]`.

### Security

- Read-only architecture.
- Loopback-only statistics-channel recommended by default.
- No `sudo`, `rndc`, `system.run[]`, external scripts, `curl`, `jq`, SSH/Telnet items or Agent 2-only plugins required.
- No BIND write/control permission required.

## [0.4.0] - 2026-09-27

Final engineering-candidate line used for runtime, dashboard and CI validation before 1.0.0.
