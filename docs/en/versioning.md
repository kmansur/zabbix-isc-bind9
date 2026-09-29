# Versioning

[Português (Brasil)](../pt-BR/versioning.md)

The project uses Semantic Versioning.

```text
VERSION:        1.1.0
STABLE_VERSION: 1.1.0
```

`main` contains the current maintained source. `STABLE_VERSION` records the production-supported baseline. Version `1.1.0` is the current stable project baseline.

## Rules

- PATCH: backward-compatible fixes and maintenance;
- MINOR: new backward-compatible metrics, discovery, triggers or dashboards;
- MAJOR: incompatible changes to public item keys, macro names, template identity or required setup.

Zabbix template metadata uses the equivalent `X.Y-Z` representation. Project version and Zabbix export format version are independent; the same project release may provide both 7.0 and 8.0 exports.
