# Architecture

[Português (Brasil)](../pt-BR/architecture.md)

The template uses BIND's native HTTP statistics channel and standard Zabbix agent keys.

```text
ISC BIND 9
   |
   | HTTP statistics on loopback
   v
Zabbix Agent / Zabbix Agent 2
   |
   | passive web.page.get[] checks
   v
Raw master items
   |
   +--> dependent items
   +--> low-level discovery
   +--> triggers
```

The design avoids external scripts and privileged control paths. Raw endpoint data is retained briefly, while derived numeric metrics keep normal history.

Version 1.0.2 uses `/json/v1/status`, `server`, `zones`, `mem`, `net` and `traffic`, plus the version-aware `/json/v1/xfrins` path on BIND 9.20. Parsing is promoted only after cross-version validation.
