# Roadmap for version 1.2.0

[Português (Brasil)](../pt-BR/roadmap-1.2.0.md)

Status: **planned / subject to validation**

Version 1.2.0 is intended to remain backward compatible. This roadmap records candidate monitoring improvements; it is not a commitment to merge an item until its BIND semantics, Zabbix behavior, security impact and operational value are validated.

## Planned priorities

### 1. SERVFAIL ratio

Evaluate a dedicated SERVFAIL percentage in addition to the existing absolute SERVFAIL rate.

Requirements:

- retain the existing absolute qps item and trigger;
- validate the correct denominator across supported BIND 9.18 and 9.20 statistics;
- avoid division by zero and startup artifacts;
- expose a configurable percentage threshold only after runtime validation;
- keep the metric understandable for both authoritative and recursive deployments.

### 2. Dropped-query ratio

Evaluate a dropped-query percentage in addition to the existing absolute `QryDropped` rate.

Requirements:

- retain the existing absolute qps metric;
- validate the denominator and counter semantics against supported BIND branches;
- avoid false positives on low-traffic servers;
- use a configurable threshold with a conservative default.

### 3. Dedicated DNSSEC validation-failure signal

Promote DNSSEC validation failures such as `ValFail` to a dedicated operational metric when exposed by resolver statistics.

Requirements:

- confirm the counter and endpoint on supported BIND versions;
- keep generic `nsstats` discovery free of duplicate collection if the counter becomes dedicated;
- add a dedicated rate and optional trigger only when the server exposes the metric;
- preserve authoritative-only deployments without unsupported noise.

### 4. Stronger end-to-end CI checks

Extend regression coverage around the actual keys exported by the template.

Candidate checks:

- derive or validate the literal quoted `web.page.get[]` forms used by template master items;
- verify restricted `AllowKey`/`DenyKey` policy with both classic Agent and Agent 2;
- add an unsupported-item smoke check where it can be made deterministic;
- preserve fresh-import validation for Zabbix 7.0 and 8.0 and live BIND 9.18/9.20 contracts.

## Explicitly outside the 1.2.0 base-template scope

The following ideas may be useful in specific environments but are not currently planned for the base template:

- QPS anomaly baselines using `trendavg()`, `baselinedev()` or similar behavior models;
- automatic primary-versus-secondary serial comparison across separate Zabbix hosts;
- DoT/DoH service monitoring;
- cross-host topology or replication orchestration.

These can be documented later as advanced recipes or separate monitoring components if a concrete operational requirement appears.

## Acceptance criteria

Before 1.2.0 can be promoted to stable:

- no breaking changes to existing public item keys, template identity or current macros without an explicit migration plan;
- successful import into maintained Zabbix 7.0 and 8.0 targets;
- successful classic Agent and Agent 2 validation;
- BIND 9.18 and 9.20 contract coverage for new metrics;
- no regression in default cardinality or security posture;
- English and Brazilian Portuguese documentation updated together;
- changelog, version metadata and release assets synchronized;
- manual runtime validation where practical.
