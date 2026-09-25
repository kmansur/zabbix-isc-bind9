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
