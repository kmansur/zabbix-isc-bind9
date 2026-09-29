# AGENTS.md

## Scope

This file defines maintenance rules for the `zabbix-isc-bind9` repository.

The current stable baseline is **v1.1.0**. Changes must preserve production safety, compatibility, attribution and the existing monitoring model unless a deliberate versioned redesign is approved.

## Project goals

- Monitor ISC BIND through the native HTTP statistics channel.
- Support both **Zabbix Agent** and **Zabbix Agent 2**.
- Keep **Zabbix 7.0** as the primary baseline and **Zabbix 8.0** as a maintained compatibility target.
- Prefer passive standard Zabbix keys and dependent items.
- Keep the statistics channel bound to loopback by default.
- Minimize privilege, attack surface and unnecessary external dependencies.
- Preserve stable item keys and template identity across compatible releases.
- Maintain English documentation with a Brazilian Portuguese counterpart.

## Security requirements

Security is a release requirement, not an optional enhancement.

Do not introduce any of the following without a documented and justified architectural decision:

- `sudo`
- `rndc`
- external scripts
- remote shell execution
- `curl`
- `jq`
- write/control operations against BIND
- unnecessarily broad Agent `AllowKey` rules
- exposure of the BIND statistics channel to untrusted networks

Recommended BIND statistics configuration:

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

If Agent key hardening is documented, keep it narrowly scoped to the configured statistics endpoint and warn users not to apply blanket `DenyKey` rules when other templates depend on the same key family.

## Monitoring architecture

The maintained design uses:

- standard Zabbix agent keys;
- dependent items;
- low-level discovery;
- BIND JSON statistics endpoints;
- native `net.dns[]` and `net.dns.perf[]` checks for functional DNS validation.

Do not reintroduce an Agent 2-only architecture.

Do not convert the template to active checks unless there is a documented project-wide reason.

Raw BIND HTTP/JSON master items should normally use:

```text
history: 0
```

Derived dependent items keep normal history as appropriate.

The statistics-channel availability trigger must use the stored lightweight heartbeat item rather than `nodata()` directly against a raw item with history disabled.

## Functional DNS tests

Functional DNS alerting is intentionally disabled until the administrator selects and validates a suitable DNS test name.

Do not assume `localhost` is a valid authoritative test name.

A valid configured test name must be verified over both UDP and TCP before enabling functional DNS alerts.

Documentation must distinguish local loopback tests from true end-to-end checks involving public addresses, firewalls, NAT, VIPs or anycast.

For external service validation, recommend a separate Zabbix host or proxy outside the monitored server.

## BIND metrics and semantics

Preserve counter/gauge semantics.

Do not automatically apply change-per-second preprocessing to values that represent gauges, current values, high-water marks or capacities.

`RecursClients` is maintained as a dedicated gauge item and must not be duplicated through generic nsstats discovery.

Secondary-zone refresh and expiry values must remain signed numeric values so expired zones can expose negative time values without becoming unsupported.

Dynamic JSONPath-based prototypes should discard temporarily absent values instead of synthesizing false zeroes when absence is valid.

The normalized zones dataset exists to avoid repeatedly parsing large `/json/v1/zones` payloads. Do not regress to repeated per-prototype full-payload parsing without a strong reason.

## Discovery rules

All maintained LLD rules must:

- define an explicit lost-resource lifetime;
- preserve the current view include/exclude filter model;
- avoid unnecessary duplicate discovery;
- retain consistent component/view tags;
- avoid excessive default cardinality.

Per-zone secondary and DNSSEC monitoring should remain opt-in.

## Dashboard rules

The operational dashboard should remain concise and useful for daily operations.

Do not reintroduce `Item navigator` widgets unless a concrete operational benefit is demonstrated.

Detailed LLD data can remain available through Latest data instead of being forced into the dashboard.

## Compatibility targets

Maintained targets:

- Zabbix Server 7.0 LTS
- Zabbix Server 8.0
- Zabbix Agent 7.0+
- Zabbix Agent 2 7.0+
- ISC BIND 9.20
- ISC BIND 9.18 compatibility where supported by the existing template model

FreeBSD is architecture-compatible with the classic Agent design, but runtime claims should only be expanded when validated.

Do not claim compatibility that has not been tested or otherwise supported by reliable evidence.

## Validation requirements

Before merging a release-impacting change, run and pass:

```sh
python -m pip install -r requirements-dev.txt
ruff check tools tests
ruff format --check tools tests
pytest -q
python tools/validate_templates.py
python tools/validate_docs.py
```

Release validation should also include the repository CI gates for:

- Zabbix 7.0 fresh import
- Zabbix 8.0 fresh import
- BIND 9.18 live JSON contract
- BIND 9.20 live JSON contract
- supported Python validation jobs
- CodeQL

When available, manual import validation on real Zabbix 7 and Zabbix 8 environments is desirable and should be documented for stable releases.

## Repository and release hygiene

Use Semantic Versioning.

- patch release: compatible bug fixes only;
- minor release: backward-compatible features or monitoring expansion;
- major release: breaking changes.

Keep these files synchronized for stable releases:

- `VERSION`
- `STABLE_VERSION`
- template vendor version fields
- `README.md`
- `README.pt-BR.md`
- `CHANGELOG.md`
- `CHANGELOG.pt-BR.md`
- compatibility/versioning documentation
- validator expectations and repository-hygiene tests

Stable releases should:

- be merged to `main`;
- have a matching Git tag;
- have a GitHub release;
- use release notes that describe the actual release rather than relying only on autogenerated PR summaries;
- retain attribution to the original community template where appropriate;
- leave no stale release branches unless there is a documented reason to keep them.

## Attribution

This project was initially inspired by and partially based on:

- **bind9 by HTTP-JSON Agent 2 Active**
- Author: **Gabriele Rossetti (KaleidoscopeIT)**
- Source: Zabbix Community Templates
- License: MIT

Do not remove or weaken this attribution.

See:

- `NOTICE.md`
- `NOTICE.pt-BR.md`
- `docs/en/license-attribution.md`
- `docs/pt-BR/license-attribution.md`

## Documentation rules

Keep technical names, item keys and template identifiers in English.

Maintain equivalent documentation in:

- English
- Brazilian Portuguese

When changing behavior, update both language trees in the same change whenever applicable.

Document operational caveats explicitly, especially when a default can generate false positives in authoritative-only or otherwise specialized BIND deployments.

## Change discipline

Prefer small, reviewable changes.

Do not modify stable keys, UUIDs, discovery structure or trigger semantics casually.

When behavior changes, update tests and documentation in the same change.

Do not add speculative complexity solely because it may be useful someday.

After a stable release is finalized, treat further work as normal maintenance rather than reopening the previous PDCA indefinitely.
