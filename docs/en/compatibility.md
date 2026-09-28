# Compatibility

[Português (Brasil)](../pt-BR/compatibility.md)

| Component | Status |
| --- | --- |
| Zabbix 7.0 | Primary export target |
| Zabbix 8.0 | Compatibility export; runtime/import validation required |
| Classic Zabbix Agent 6.0+ | Maintained design target |
| Zabbix Agent 2 6.0+ | Maintained design target |
| FreeBSD | Classic agent path |
| Linux | Classic agent or Agent 2 |
| ISC BIND 9.20 | Primary supported BIND validation target |
| ISC BIND 9.18.50 | Legacy compatibility target; upstream EOL |
| ISC BIND 9.18.39 on Ubuntu 24.04 | Runtime statistics endpoint validation completed |

The project does not claim support for every historical agent version. Older agents can work if the standard keys used by the template are available, but they are outside the maintained test matrix.

BIND builds must provide JSON statistics support. Endpoint availability and individual counters can vary by BIND branch/build; unsupported optional semantics are not guessed.

## BIND lifecycle note

ISC ended maintenance for BIND 9.18 after 9.18.50 in June 2026. The project keeps 9.18 compatibility for existing deployments, while new production validation prioritizes the supported 9.20 ESV branch.

## Runtime validation note

The `status`, `server`, `zones`, `mem`, `net` and `traffic` JSON endpoints were validated on Ubuntu 24.04 with BIND 9.18.39. The tested server exposed resolver blocks containing `stats`, `qtypes`, `cache`, `cachestats` and `adb`, and exported `sockstats` through `/json/v1/net`.


## Zabbix 8.0 development validation

The 8.0 export is continuously imported in CI against the official Zabbix trunk Docker images, which are the development line for Zabbix 8.0. This validates schema/import compatibility before a stable 8.0 release exists. Runtime behavior is still considered pre-release until validated against an official stable 8.0 build.


## BIND JSON contract fixtures

The repository includes representative JSON fixtures for BIND 9.18 and 9.20. Pytest validates the structural contracts used by preprocessing and discovery, including resolver/cache blocks, socket statistics, memory fields, traffic histograms, secondary-zone timers and the 9.20 incoming-transfer endpoint. These fixtures complement, rather than replace, runtime validation against real BIND servers.


## Live BIND container validation

CI starts the official ISC Docker images for BIND 9.18 and 9.20 with a minimal statistics-channel configuration and validates the live JSON endpoints used by the template. The 9.18 job verifies that `/json/v1/xfrins` is absent, while the 9.20 job requires it to be present. This protects the version-aware transfer design against upstream endpoint changes.


## Real native DNS health-check validation

Runtime validation on Ubuntu 24.04 with BIND 9.18.39 and the classic Zabbix agent confirmed all native service checks used by template version 0.4.0:

- UDP DNS availability: `1`
- TCP DNS availability: `1`
- UDP response time: approximately `0.000480 s` (0.48 ms)
- TCP response time: approximately `0.000616 s` (0.62 ms)

The checks used `127.0.0.1`, query name `localhost`, record type `A`, one-second timeout and two attempts. This confirms that `net.dns[]` and `net.dns.perf[]` work as designed with the passive classic Zabbix agent in the real BIND 9.18.39 test environment.
