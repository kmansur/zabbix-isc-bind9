# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Resolver monitoring by view, including resolver counters, recursive query types and ADB discovery.
- Resolver cache metrics for hits/misses, evictions, cache nodes and cache memory.
- BIND memory usage metrics from the native memory statistics endpoint.

### Fixed
- Corrected `{$BIND.STATS.HOST}` to use `127.0.0.1` instead of a full URL when `web.page.get[]` also supplies path and port parameters.
- Socket statistics discovery now uses `/json/v1/net`, matching BIND statistics-channel semantics.

### Added
- Initial project structure and bilingual documentation.
- Agent-neutral architecture for classic Zabbix Agent and Zabbix Agent 2.
- BIND JSON statistics collection through the local statistics channel.
- Initial server-counter LLD and zone-discovery design.
- Zabbix 7.0 and 8.0 versioned exports.
- Repository validation and CI baseline.

## [0.1.0] - 2026-09-25

Initial engineering candidate. No production-stable release has been promoted yet.
