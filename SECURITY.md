# Security Policy

**English** | [Português (Brasil)](SECURITY.pt-BR.md)

## Security model

The template is designed for read-only monitoring using the native BIND statistics channel and standard Zabbix agent capabilities.

The recommended statistics listener is restricted to loopback:

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

Do not expose the statistics listener to untrusted networks. If a non-loopback listener is operationally required, restrict access with the BIND ACL and host/network firewall.

The maintained template does not require privileged operating-system execution or BIND control/write permissions.

## Reporting a vulnerability

Do not include credentials, TSIG secrets, customer-identifying hostnames or unsanitized production configuration in public reports.

A sanitized public issue may be used when the problem can be reproduced without sensitive information. Clearly describe the security impact.

## Supported versions

Version `1.0.2` is the current production-stable baseline and is the supported security-maintenance line.
