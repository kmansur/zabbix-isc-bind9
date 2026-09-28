# Configuration

[Português (Brasil)](../pt-BR/configuration.md)

## Template macros

| Macro | Default | Purpose |
| --- | --- | --- |
| `{$BIND.DNS.TEST.ENABLED}` | `0` | Enables functional DNS alerting after the test name has been validated; set to `1` to enable alerts |
| `{$BIND.DNS.TEST.SERVER}` | `127.0.0.1` | DNS server address queried by the native Zabbix DNS health checks |
| `{$BIND.DNS.TEST.NAME}` | `localhost` | DNS name used for service availability and response-time checks |
| `{$BIND.DNS.TEST.TYPE}` | `A` | DNS record type used by the native health checks |
| `{$BIND.DNS.TEST.TIMEOUT}` | `1` | Per-attempt DNS query timeout in seconds |
| `{$BIND.DNS.TEST.COUNT}` | `2` | Number of DNS query attempts |
| `{$BIND.DNS.FAIL.WINDOW}` | `3m` | Continuous failure window before a DNS availability problem |
| `{$BIND.DNS.RESPONSE.UDP.WARN}` | `0.1` | Average UDP DNS response-time warning threshold in seconds |
| `{$BIND.DNS.RESPONSE.TCP.WARN}` | `0.1` | Average TCP DNS response-time warning threshold in seconds |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Average dropped-query rate threshold for the 5-minute warning |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | Average SERVFAIL rate threshold for the 5-minute warning |
| `{$BIND.ZONE.EXPIRES.WARN}` | `1h` | Warning window before a secondary zone reaches its expiry deadline |
| `{$BIND.ZONE.SECONDARY.MATCHES}` | `^$` | Regex selecting secondary zones for per-zone refresh/expiry monitoring; the default discovers none |
| `{$BIND.ZONE.DNSSEC.MATCHES}` | `^$` | Regex selecting zones for per-zone DNSSEC monitoring; the default discovers none |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Host used by `web.page.get[]` for the BIND statistics channel |
| `{$BIND.STATS.NODATA}` | `10m` | Maximum interval without statistics data before a monitoring warning |
| `{$BIND.STATS.PORT}` | `8053` | Local BIND statistics-channel TCP port |

Keep the statistics listener on loopback whenever possible. If another local address is required, restrict access with both the BIND ACL and the host/network firewall.

## BIND statistics channel

Recommended configuration:

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

The template reads the statistics locally through standard Zabbix agent keys. It does not require BIND control/write permissions.

## Native DNS health checks

The template validates DNS functionality independently of the statistics channel by using `net.dns[]` and `net.dns.perf[]` over both UDP and TCP. Collection is enabled by default, but DNS functional **alerting is disabled by default** with `{$BIND.DNS.TEST.ENABLED}=0` until the test name has been reviewed.

The default test is:

```text
server: 127.0.0.1
name:   localhost
type:   A
```

The `localhost/A` query was validated successfully in the project's Ubuntu 24.04/BIND 9.18.39 runtime environment, but not every BIND configuration is required to answer that name.

> **Important:** `localhost` is only a collection default. Before enabling DNS functional alerts, set `{$BIND.DNS.TEST.NAME}` to a name appropriate for the monitored server role and validate both UDP and TCP. On authoritative-only servers, use a stable record from a zone served by that same BIND instance. After validation, set `{$BIND.DNS.TEST.ENABLED}=1` on the host or template.

### Choosing the functional DNS test name

Choose a name that represents the role of the monitored server:

- **authoritative server:** use a stable record from a zone that this BIND instance is expected to answer authoritatively;
- **recursive resolver:** use a stable external name only when recursion is intentionally enabled and expected to work;
- **mixed role:** prefer a stable authoritative record for local daemon availability, and use separate external monitoring if end-to-end recursive reachability must also be measured.

Before routing alerts to production, validate the configured name locally with both UDP and TCP using the same `net.dns[]` parameters as the template. A returned value of `1` means the query produced a usable answer; `0` means it did not. Only then set `{$BIND.DNS.TEST.ENABLED}=1`.

## Per-zone monitoring

Per-zone monitoring is deliberately opt-in to control cardinality.

To monitor every secondary zone for refresh/expiry:

```text
{$BIND.ZONE.SECONDARY.MATCHES}=.*
```

To enable DNSSEC counters for every zone exporting them:

```text
{$BIND.ZONE.DNSSEC.MATCHES}=.*
```

Prefer a targeted regex when only selected critical zones require per-zone detail.
