# Versioning

[Português (Brasil)](../pt-BR/versioning.md)

The project uses Semantic Versioning.

```text
VERSION:        0.1.2
STABLE_VERSION: 0.0.0
```

`main` is the active development branch. A production-supported version begins only when a tagged release is explicitly promoted and `STABLE_VERSION` is updated.

## Rules

- PATCH: backward-compatible fixes and maintenance;
- MINOR: new backward-compatible metrics, discovery, triggers or dashboards;
- MAJOR: incompatible changes to public item keys, macro names, template identity or required setup.

Zabbix template metadata uses the equivalent `X.Y-Z` representation. Project version and Zabbix export format version are independent; the same project release may provide both 7.0 and 8.0 exports.
