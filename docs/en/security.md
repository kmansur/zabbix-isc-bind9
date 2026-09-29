# Security design

[Português (Brasil)](../pt-BR/security.md)

The BIND statistics channel exposes operational information and should be treated as an administrative interface.

The project defaults follow these principles:

- bind the statistics channel to loopback;
- allow localhost only;
- use standard passive Zabbix agent checks for local acquisition;
- require no privileged BIND control permissions;
- perform no write or configuration operation;
- avoid external parsing programs.

If statistics must be collected through a non-loopback address, document the exception and restrict it with both the BIND ACL and the host/network firewall.

The template itself contains no credentials. Sensitive deployment values should be managed through the normal Zabbix secret-management mechanisms when applicable.

## Optional Zabbix agent key hardening

The template only needs read-only standard keys. Administrators who want an additional agent-side restriction can explicitly allow the local BIND statistics paths and deny other uses of `web.page.get[]`.

Example for the default listener:

```ini
AllowKey=web.page.get["127.0.0.1","/json/v1/*","8053"]
DenyKey=web.page.get[*]
```

The quoted parameter form intentionally matches the literal `web.page.get[]` keys exported by the template. Adapt the address and port when `{$BIND.STATS.HOST}` or `{$BIND.STATS.PORT}` differs from the defaults. Validate the exact configuration with both the classic agent and Agent 2 before deployment. The project CI tests this allow/deny model against a live BIND statistics endpoint using the same quoted key form.

This hardening is optional because existing agent deployments may already use `web.page.get[]` for unrelated templates. Do not add a blanket deny without first reviewing those dependencies.
