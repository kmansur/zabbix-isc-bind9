# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Validation
- Completed a passive-template cleanup audit against the original community template: no active item types, legacy BIND9 macros, legacy LLD macros, legacy port 8653, shared item keys or shared UUIDs remain. The original project name remains only in license attribution.
- CI validates Python 3.11, 3.13 and 3.14, template structure, bilingual documentation and a fresh import into Zabbix 7.0.

### Added
- Added graceful BIND 9.20 incoming-transfer monitoring through `/json/v1/xfrins`, with a compatibility indicator and no unsupported items on BIND 9.18.
- Secondary-zone refresh and expiry timers with trigger prototypes.
- DNSSEC signing/refresh counter discovery for zones exporting `dnssec-sign`/`dnssec-refresh`.
- Resolver monitoring by view, including resolver counters, recursive query types and ADB discovery.
- Resolver cache metrics for hits/misses, evictions, cache nodes and cache memory.
- BIND memory usage metrics from the native memory statistics endpoint.
- Aggregate zone counters for total, primary and secondary zones.

### Changed
- Renamed the template from `ISC BIND 9 by Zabbix Agent` to `ISC BIND by Zabbix agent`. The repository name remains unchanged.
- Per-zone secondary refresh/expiry discovery is opt-in via `{$BIND.ZONE.SECONDARY.MATCHES}`; the default `^$` creates no per-zone secondary items.
- Removed default all-zone SOA serial and loaded-age discovery; the base template now uses aggregate total/primary/secondary zone counts.
- Per-zone DNSSEC discovery is opt-in via `{$BIND.ZONE.DNSSEC.MATCHES}` to control cardinality.
- Optional zero-valued BIND counters are normalized to zero instead of becoming unsupported.
- Switched the default master items from active to passive Zabbix agent checks. This removes the `ServerActive` requirement while remaining compatible with Agent 2.

### Fixed
- Corrected `{$BIND.STATS.HOST}` to use `127.0.0.1` instead of a full URL when `web.page.get[]` also supplies path and port parameters.
- Socket statistics discovery now uses `/json/v1/net`, matching BIND statistics-channel semantics.

## [0.1.4] - 2026-09-25

Current engineering candidate. No production-stable release has been promoted yet.
