# ISC BIND by Zabbix agent

[![CI](https://github.com/kmansur/zabbix-isc-bind9/actions/workflows/ci.yml/badge.svg)](https://github.com/kmansur/zabbix-isc-bind9/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kmansur/zabbix-isc-bind9/actions/workflows/security.yml/badge.svg)](https://github.com/kmansur/zabbix-isc-bind9/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**English** | [Português (Brasil)](README.pt-BR.md)

A security-focused Zabbix template for monitoring **ISC BIND** through the native BIND HTTP statistics channel. The design is compatible with both **Zabbix Agent** and **Zabbix Agent 2** and intentionally avoids Agent 2-only plugins, external scripts, sudo, `rndc`, `curl` and `jq`.

> **Development status:** version `0.1.4` is an initial engineering candidate and is not yet a production-stable release.

## Design goals

- support Zabbix Agent and Zabbix Agent 2 with the same template using passive checks by default;
- keep the BIND statistics channel bound to loopback by default;
- collect once and fan out through dependent items and low-level discovery;
- avoid privileged commands and write/control operations;
- preserve stable item keys and template identity across compatible releases;
- provide English documentation with a maintained Brazilian Portuguese counterpart;
- support Zabbix 7.0 as the primary baseline and Zabbix 8.0 as a compatibility target.

## Current monitoring coverage

The initial candidate includes:

- BIND version and JSON statistics API version;
- server uptime and time since the last configuration/reload;
- IPv4 and IPv6 request rates;
- dropped-query, SERVFAIL and recursion rates;
- automatic discovery of `nsstats`, query types, response codes and socket counters;
- aggregate zone counts (total, primary and secondary), with optional per-zone secondary/DNSSEC discovery;
- local collection of the `status`, `server`, `zones`, `mem`, `net` and `traffic` JSON endpoints;
- UDP/TCP traffic-rate aggregation from BIND traffic histograms;
- availability and operational triggers for the statistics channel and critical DNS counters.

Resolver, cache, DNSSEC, memory, network and transfer metrics are included where their semantics have been validated across the supported BIND branches.

## Security model

Recommended BIND configuration:

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

The monitoring agent reads the statistics locally and sends the resulting data to Zabbix. The statistics listener should **not** be exposed to untrusted networks.

No control operation is required by the template.

## Compatibility

| Component | Project target |
| --- | --- |
| Zabbix Server 7.0 LTS | Primary |
| Zabbix Server 8.0 | Compatibility export / validation target |
| Zabbix Agent 6.0+ | Supported design target |
| Zabbix Agent 2 6.0+ | Supported design target |
| FreeBSD | Supported with classic Zabbix Agent |
| Linux | Supported with Zabbix Agent or Agent 2 |
| ISC BIND 9.20 | Primary supported validation target |
| ISC BIND 9.18.50 | Legacy compatibility target (EOL upstream) |
| ISC BIND newer supported branches | Compatibility target |

Older agents may work when they provide the required standard `web.page.get[]` key, but they are not part of the project's maintained test matrix.

See [docs/en/compatibility.md](docs/en/compatibility.md).

## Repository layout

```text
.github/                 GitHub workflows and contribution metadata
docs/
├── en/                  English documentation
└── pt-BR/               Brazilian Portuguese documentation
templates/
├── 7.0/                 Zabbix 7.0 export
└── 8.0/                 Zabbix 8.0 compatibility export
tests/                   Repository and template tests
tools/                   Template/documentation validators
```

## Development validation

```sh
python -m pip install -r requirements-dev.txt
ruff check tools tests
ruff format --check tools tests
pytest -q
python tools/validate_templates.py
python tools/validate_docs.py
```

## Versioning

The project uses Semantic Versioning.

```text
VERSION:        0.1.4
STABLE_VERSION: 0.0.0
```

`0.0.0` means that no production-stable release has been promoted yet. Production use should wait for a tagged release unless the operator is intentionally participating in validation.

## Origin and attribution

This project was initially inspired by and partially based on **bind9 by HTTP-JSON Agent 2 Active** from the Zabbix Community Templates repository, authored by **Gabriele Rossetti (KaleidoscopeIT)**. The upstream community repository is distributed under the MIT License.

This project substantially redesigns the original monitoring model to remove the Agent 2 requirement, add broader BIND statistics coverage, improve security defaults, introduce bilingual documentation and add validation/versioning infrastructure.

See [NOTICE.md](NOTICE.md) and [docs/en/license-attribution.md](docs/en/license-attribution.md).

## License

MIT License. See [LICENSE](LICENSE).

Maintained by **Karim Mansur / Net Tech**.
