# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

- Improved the Overview dashboard readability: the Uptime card now uses a smaller value font, Primary/Secondary zones and Memory in use were moved below the DNS status cards, and the DNS response-time graph was raised/aligned with the summary area.
- DNS UDP and DNS TCP dashboard cards now use dedicated display-only dependent items so they show `Up`/`Down` without the raw numeric value in parentheses.
- The Overview Problems widget now filters by `BIND:` so unrelated host problems from other templates are not shown.

## [1.1.0] - 2026-09-29

### Validation

- Manual template import confirmed successfully on both Zabbix 7 and Zabbix 8 environments.
- Automated fresh-import gates, BIND 9.18/9.20 live contracts, Python 3.11/3.13/3.14 validation and CodeQL passed before promotion to `main`.

### Added

- Independent `named` process and UDP/TCP listener monitoring using standard Zabbix agent keys.
- Configurable DNS-test interval, view discovery filters, recursive-client threshold and DeleteLRU threshold.
- Dedicated `RecursClients` gauge, per-view cache hit ratio and local SOA serial for selected secondary zones.
- Optional documented `AllowKey`/`DenyKey` hardening for the statistics-channel `web.page.get[]` path.
- CI regression coverage for expired secondary zones and metric classification allowlists.

### Changed

- Added a normalized zone dataset so large `/json/v1/zones` payloads are parsed once before per-zone LLD/prototypes.
- Dynamic LLD JSONPath prototypes discard temporarily absent values instead of becoming unsupported or synthesizing zero.
- Resolver/cache/zone discoveries use explicit view filters and all LLD rules use an explicit 7-day lost-resource lifetime.
- Raw HTTP/JSON master items no longer store history; derived dependent items continue to keep normal history.
- Statistics-channel availability now uses a lightweight stored heartbeat derived from `/json/v1/status`, preserving `nodata()` trigger evaluation while keeping raw JSON history disabled.
- Cache item prototypes now carry consistent component/view tags.

### Fixed

- Secondary-zone expiry and refresh timers are explicitly signed numeric values, allowing expired zones to remain supported and the existing expired-zone trigger to fire correctly.
- Added a restart trigger based on decreasing BIND uptime.
- Removed duplicate `RecursClients` discovery now that it is exposed as a dedicated gauge item.

## [1.0.2] - 2026-09-28

### Added

- Added `{$BIND.DNS.TEST.ENABLED}`, defaulting to `0`, so functional DNS alerts remain silent until the administrator validates a server-appropriate test name.
- Added separate UDP and TCP response-time thresholds: `{$BIND.DNS.RESPONSE.UDP.WARN}` and `{$BIND.DNS.RESPONSE.TCP.WARN}`.
- Added the BIND JSON statistics version to the operational Overview dashboard.

### Changed

- Functional DNS problem names now describe a failed configured test rather than implying that the BIND daemon itself is down.
- Functional DNS problem event names and operational data include the configured test name/type for faster diagnosis.
- Installation and configuration documentation now requires validating the test name over UDP and TCP before setting `{$BIND.DNS.TEST.ENABLED}=1`.
- Maintained Zabbix Agent and Agent 2 baseline is now documented as 7.0+.
- Removed stale 1.0.0/1.0-0 compatibility references from current documentation.

### Fixed

- Prevented false-positive functional DNS alerts caused by the generic `localhost/A` collection default on authoritative-only BIND servers.

## [1.0.1] - 2026-09-28

### Fixed

- Corrected BIND counter/gauge semantics: `RecursClients`, high-water marks, resolver in-progress/fetch/bucket values, ADB sizes and active/current socket values are no longer treated as rates.
- Corrected the BIND 9.18 memory fixture to model `memory.contexts` as a JSON array, matching ISC BIND.
- Rebuilt corrupted EN/pt-BR configuration macro tables and strengthened documentation validation.
- Corrected stale passive/active troubleshooting references and the current project name in NOTICE.

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
