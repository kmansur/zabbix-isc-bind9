# Configuration

[Português (Brasil)](../pt-BR/configuration.md)

## Template macros

| Macro | Default | Purpose |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Local BIND statistics-channel host used by `web.page.get[]` |
| `{$BIND.STATS.PORT}` | `8053` | BIND statistics-channel TCP port |
| `{$BIND.STATS.NODATA}` | `10m` | Maximum interval without statistics data before raising a monitoring warning |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Dropped-query rate warning threshold in queries per second |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | SERVFAIL rate warning threshold in responses per second |
| `{$BIND.ZONE.EXPIRES.WARN}` | `1h` | Warning window before an enabled secondary-zone monitor reaches SOA expiry |
| `{$BIND.ZONE.SECONDARY.MATCHES}` | `^$` | Regex selecting secondary zones for per-zone refresh/expiry monitoring; default selects none |
| `{$BIND.ZONE.DNSSEC.MATCHES}` | `^$` | Regex selecting zones for per-zone DNSSEC detail; default selects none |
| `{$BIND.DNS.TEST.SERVER}` | `127.0.0.1` | DNS server address queried by the native Zabbix DNS health checks |
| `{$BIND.DNS.TEST.NAME}` | `localhost` | DNS name used by the functional availability/performance test |
| `{$BIND.DNS.TEST.TYPE}` | `A` | DNS record type used by the functional test |
| `{$BIND.DNS.TEST.TIMEOUT}` | `1` | Per-attempt DNS query timeout in seconds |
| `{$BIND.DNS.TEST.COUNT}` | `2` | Number of DNS query attempts |
| `{$BIND.DNS.FAIL.WINDOW}` | `3m` | Continuous failure window before UDP/TCP availability raises a problem |
| `{$BIND.DNS.RESPONSE.WARN}` | `0.1` | Average local DNS response-time warning threshold in seconds |

Keep the statistics listener on loopback whenever possible. If another local address is required, restrict access with both the BIND ACL and the host/network firewall.

## Functional DNS health checks

The statistics channel proves that the BIND monitoring interface is available; it does not prove that the DNS service is answering useful queries. The template therefore also uses the standard Zabbix agent keys `net.dns[]` and `net.dns.perf[]`.

The default `localhost/A` query was validated in the project's Ubuntu 24.04/BIND 9.18.39 runtime environment, but it is not guaranteed to be answered by every BIND deployment.

Choose a test name that represents the role of the monitored server:

- **authoritative server:** use a stable record in a zone that this BIND instance must answer authoritatively;
- **recursive resolver:** use a stable external name only when recursion is intentionally enabled and expected to work;
- **mixed role:** prefer a stable authoritative record for local daemon availability and use separate external monitoring when end-to-end recursive reachability is required.

Before routing alerts to production, test the configured name locally over both UDP and TCP with the same `net.dns[]` parameters used by the template. A value of `1` means the query produced a usable answer; `0` means it did not.

## Optional per-zone monitoring

Per-zone monitoring is deliberately disabled by default to keep cardinality predictable.

To monitor all secondary-zone expiry/refresh timers:

```text
{$BIND.ZONE.SECONDARY.MATCHES}=.*
```

To monitor selected secondary zones, use an anchored regular expression, for example:

```text
{$BIND.ZONE.SECONDARY.MATCHES}=^(example\.com|example\.net)$
```

DNSSEC per-zone counters follow the same model through `{$BIND.ZONE.DNSSEC.MATCHES}`. Use `.*` only when the additional item cardinality is intentional.
