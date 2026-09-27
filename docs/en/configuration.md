# Configuration

[Português (Brasil)](../pt-BR/configuration.md)

## Template macros

| Macro | Default | Purpose |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Local statistics host |
| `{$BIND.STATS.PORT}` | `8053` | Statistics TCP port |
| `{$BIND.STATS.NODATA}` | `10m` | No-data threshold |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Dropped-query rate threshold |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | SERVFAIL rate threshold |
| `{$BIND.ZONE.EXPIRES.WARN}` | `1h` | Warning window before a secondary zone expires |
| `{$BIND.ZONE.SECONDARY.MATCHES}` | `^# Configuration

[Português (Brasil)](../pt-BR/configuration.md)

## Template macros

| Macro | Default | Purpose |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Local statistics host |
| `{$BIND.STATS.PORT}` | `8053` | Statistics TCP port |
| `{$BIND.STATS.NODATA}` | `10m` | No-data threshold |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Dropped-query rate threshold |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | SERVFAIL rate threshold |
 | Regex selecting secondary zones for per-zone refresh/expiry monitoring; default disables discovery |
| `{$BIND.ZONE.DNSSEC.MATCHES}` | `^# Configuration

[Português (Brasil)](../pt-BR/configuration.md)

## Template macros

| Macro | Default | Purpose |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Local statistics host |
| `{$BIND.STATS.PORT}` | `8053` | Statistics TCP port |
| `{$BIND.STATS.NODATA}` | `10m` | No-data threshold |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Dropped-query rate threshold |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | SERVFAIL rate threshold |
 | Regex selecting zones for per-zone DNSSEC detail; default disables discovery |

Keep the listener on loopback whenever possible. If another local address is required, restrict access with both the BIND ACL and the host/network firewall.


## Native DNS health checks

The template validates the DNS service itself independently of the statistics channel.

| Macro | Default | Purpose |
| --- | --- | --- |
| `{$BIND.DNS.TEST.SERVER}` | `127.0.0.1` | DNS server address queried by the agent |
| `{$BIND.DNS.TEST.NAME}` | `localhost` | DNS name used for the test query |
| `{$BIND.DNS.TEST.TYPE}` | `A` | DNS record type |
| `{$BIND.DNS.TEST.TIMEOUT}` | `1` | Per-attempt timeout in seconds |
| `{$BIND.DNS.TEST.COUNT}` | `2` | Query attempts |
| `{$BIND.DNS.FAIL.WINDOW}` | `3m` | Continuous failure window before an availability problem |
| `{$BIND.DNS.RESPONSE.WARN}` | `0.1` | Average response-time warning threshold in seconds |

The default `localhost/A` query is intended as a low-cost local service check. Override the name/type on hosts where the monitored BIND instance does not answer that query.
