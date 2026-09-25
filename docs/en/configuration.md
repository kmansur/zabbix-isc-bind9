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
