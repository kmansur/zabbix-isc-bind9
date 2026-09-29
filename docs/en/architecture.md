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

The design avoids external scripts and privileged control paths. Raw endpoint payloads are preprocessing-only masters with history disabled, while derived numeric metrics keep normal history.

Version 1.1.0 uses `/json/v1/status`, `server`, `zones`, `mem`, `net` and `traffic`, plus the version-aware `/json/v1/xfrins` path on BIND 9.20. Parsing is promoted only after cross-version validation.

The zones path has an additional normalization stage:

```text
/json/v1/zones raw
       |
       v
bind.zones.normalized  (history disabled)
       |
       +--> secondary-zone discovery
       +--> signed refresh/expiry timers
       +--> local SOA serial
       +--> optional per-zone DNSSEC counters
```

This stage parses the large zones payload once and feeds compact dependent data to per-zone prototypes, avoiding repeated full-payload scans as zone count grows. Independent `proc.num[]`, `net.tcp.listen[]` and `net.udp.listen[]` checks provide daemon/listener health even when the statistics channel itself is unavailable.
