# Compatibility

[Português (Brasil)](../pt-BR/compatibility.md)

| Component | Status |
| --- | --- |
| Zabbix 7.0 | Primary export target |
| Zabbix 8.0 | Runtime validated on Zabbix 8.0.0beta2; continuously fresh-import validated against official trunk images |
| Classic Zabbix Agent 6.0+ | Maintained design target |
| Zabbix Agent 2 6.0+ | Maintained design target |
| FreeBSD | Classic agent design path; package availability verified, runtime validation still recommended |
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


## Zabbix 8.0 validation

The 8.0 export is continuously imported in CI against the official Zabbix trunk Docker images.

In addition, template version `1.0-0` was imported successfully into a real **Zabbix 8.0.0beta2** server and linked to the monitored BIND host. Runtime collection was confirmed working, including DNS UDP/TCP availability and response time, IPv4/IPv6 request rates, SERVFAIL/dropped-query rates, transfer metrics, memory metrics, zone counters, raw statistics endpoints and discovered data.

The validated Zabbix 8.0.0beta2 template showed 35 base items, 8 triggers, 9 classic graphs, 1 dashboard and 10 discovery rules, with discovered runtime data being collected normally.

This provides real runtime validation for the Zabbix 8.0 development line. A final stable Zabbix 8.0 build should still be revalidated when available because beta-to-stable schema or frontend behavior can change.


## BIND JSON contract fixtures

The repository includes representative JSON fixtures for BIND 9.18 and 9.20. Pytest validates the structural contracts used by preprocessing and discovery, including resolver/cache blocks, socket statistics, memory fields, traffic histograms, secondary-zone timers and the 9.20 incoming-transfer endpoint. These fixtures complement, rather than replace, runtime validation against real BIND servers.


## Live BIND container validation

CI starts the official ISC Docker images for BIND 9.18 and 9.20 with a minimal statistics-channel configuration and validates the live JSON endpoints used by the template. The 9.18 job verifies that `/json/v1/xfrins` is absent, while the 9.20 job requires it to be present. This protects the version-aware transfer design against upstream endpoint changes.


## Real native DNS health-check validation

Runtime validation on Ubuntu 24.04 with BIND 9.18.39 and the classic Zabbix agent confirmed all native service checks used by template version 1.0.0:

- UDP DNS availability: `1`
- TCP DNS availability: `1`
- UDP response time: approximately `0.000480 s` (0.48 ms)
- TCP response time: approximately `0.000616 s` (0.62 ms)

The checks used `127.0.0.1`, query name `localhost`, record type `A`, one-second timeout and two attempts. This confirms that `net.dns[]` and `net.dns.perf[]` work as designed with the passive classic Zabbix agent in the real BIND 9.18.39 test environment.


## FreeBSD note

The template intentionally uses standard classic-agent keys and has no Linux-only helper scripts or privileged commands. The FreeBSD Ports Collection provides the Zabbix 7 classic agent (`net-mgmt/zabbix7-agent`), which supports the intended deployment path. The project's real runtime validation has been performed on Linux; therefore FreeBSD is considered architecture-compatible rather than a separately runtime-certified platform in version 1.0.
