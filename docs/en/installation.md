# Installation

[Português (Brasil)](../pt-BR/installation.md)

## 1. Configure BIND

Add a statistics listener restricted to localhost:

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

Validate the BIND configuration before reloading the service.

## 2. Verify locally

Confirm that this endpoint returns JSON on the monitored server:

```text
http://127.0.0.1:8053/json/v1/status
```

Do not expose this listener to untrusted networks.

## 3. Configure the Zabbix agent

Use Zabbix Agent 7.0+ or Zabbix Agent 2 7.0+. Passive checks must work for the host. The standard `web.page.get[]`, `net.dns[]` and `net.dns.perf[]` keys must be available. No custom agent plugin or external parser is required.

## 4. Import the template

Import the file matching the target Zabbix Server:

- `templates/7.0/isc-bind9-by-zabbix-agent.yaml`
- `templates/8.0/isc-bind9-by-zabbix-agent.yaml` for Zabbix 8.0; runtime validated on Zabbix 8.0.0beta2

Link **ISC BIND by Zabbix agent** to the host and review Latest data before routing alerts to production.

## 5. Configure the functional DNS test

The template collects UDP/TCP DNS health data immediately, but functional DNS alerts are disabled by default.

Choose a stable test name appropriate for the server role and override `{$BIND.DNS.TEST.NAME}` on the host. For an authoritative server, use a record served by that BIND instance.

Validate both transports locally, for example:

```text
zabbix_agentd -t 'net.dns[127.0.0.1,example.com,A,1,2,udp]'
zabbix_agentd -t 'net.dns[127.0.0.1,example.com,A,1,2,tcp]'
```

Both checks should return `1`. After validation, set:

```text
{$BIND.DNS.TEST.ENABLED}=1
```

Do not enable the functional alerts until the selected name is known to be valid for the monitored server.
