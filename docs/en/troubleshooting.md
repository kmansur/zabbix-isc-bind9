# Troubleshooting

[Português (Brasil)](../pt-BR/troubleshooting.md)

## No statistics data

1. Confirm that BIND loaded the `statistics-channels` configuration.
2. Test `/json/v1/status` locally on the monitored host.
3. Confirm `{$BIND.STATS.HOST}` and `{$BIND.STATS.PORT}`.
4. Confirm Zabbix active checks are working for the host.
5. Confirm the BIND build provides JSON statistics support.

## Ubuntu 24.04: named works but systemd remains in activating state

A BIND process can answer DNS, RNDC and statistics requests while `systemd` still reports:

```text
ActiveState=activating
SubState=start
```

When the unit uses `Type=notify`, check the kernel log for AppArmor denials involving:

```text
/run/systemd/notify
/proc/version_signature
```

A typical failure is an AppArmor profile blocking BIND from sending the `READY=1` notification to systemd. In that case, `systemd` waits until `TimeoutStartSec` expires and restarts an otherwise functional `named` process when `Restart=on-failure` is enabled.

Prefer a local AppArmor override rather than editing the vendor profile directly:

```text
/etc/apparmor.d/local/usr.sbin.named
```

Example rules validated on Ubuntu 24.04:

```text
/run/systemd/notify w,
/proc/version_signature r,
```

After updating the local profile, validate and reload AppArmor, then restart BIND and confirm:

```text
ActiveState=active
SubState=running
```

Do not grant broad capabilities such as `sys_admin` just to silence an AppArmor audit message. Add permissions only when a required BIND function is demonstrably blocked.

## Raw master item contains HTTP headers

The template preprocessing keeps the JSON object beginning at the first `{`. If this fails, capture a sanitized result from the affected master item and report the BIND and agent versions.

## A counter is missing

Counter sets can vary by workload, build and BIND version. Discovery rules adapt to the counters actually exported by BIND. Do not create synthetic zero-valued counters for fields that are not exported.

## Zone prototype becomes unsupported

Some zone fields depend on zone type and BIND version. Report the sanitized zone JSON object together with BIND version, view and zone type so the compatibility logic can be improved without guessing.
