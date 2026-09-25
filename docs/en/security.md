# Security design

[Português (Brasil)](../pt-BR/security.md)

The BIND statistics channel exposes operational information and should be treated as an administrative interface.

The project defaults follow these principles:

- bind the statistics channel to loopback;
- allow localhost only;
- use Zabbix active checks for local acquisition;
- require no privileged BIND control permissions;
- perform no write or configuration operation;
- avoid external parsing programs.

If statistics must be collected through a non-loopback address, document the exception and restrict it with both the BIND ACL and the host/network firewall.

The template itself contains no credentials. Sensitive deployment values should be managed through the normal Zabbix secret-management mechanisms when applicable.
