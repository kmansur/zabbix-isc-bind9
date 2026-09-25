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

Use either Zabbix Agent or Zabbix Agent 2. Active checks must work for the host. No custom agent plugin or external parser is required.

## 4. Import the template

Import the file matching the target Zabbix Server:

- `templates/7.0/isc-bind9-by-zabbix-agent.yaml`
- `templates/8.0/isc-bind9-by-zabbix-agent.yaml` for compatibility validation

Link **ISC BIND 9 by Zabbix Agent** to the host and review Latest data before routing alerts to production.
