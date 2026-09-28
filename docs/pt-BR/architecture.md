# Arquitetura

[English](../en/architecture.md)

O template utiliza o statistics-channel HTTP nativo do BIND e chaves padrão do Zabbix agent.

```text
ISC BIND 9
   |
   | estatísticas HTTP no loopback
   v
Zabbix Agent / Zabbix Agent 2
   |
   | passive checks com web.page.get[]
   v
Itens mestres brutos
   |
   +--> dependent items
   +--> low-level discovery
   +--> triggers
```

O projeto evita scripts externos e caminhos privilegiados de controle. Os payloads brutos dos endpoints são itens mestres apenas para preprocessing, com histórico desabilitado, enquanto as métricas numéricas derivadas mantêm histórico normal.

A versão 1.0.2 utiliza `/json/v1/status`, `server`, `zones`, `mem`, `net` e `traffic`, além do caminho version-aware `/json/v1/xfrins` no BIND 9.20. Parsing somente é promovido após validação entre versões.

O caminho de zonas possui uma etapa adicional de normalização:

```text
/json/v1/zones bruto
       |
       v
bind.zones.normalized  (histórico desabilitado)
       |
       +--> discovery de zonas secundárias
       +--> timers assinados de refresh/expiry
       +--> serial SOA local
       +--> contadores DNSSEC opcionais por zona
```

Essa etapa interpreta uma única vez o payload grande de zonas e fornece dados compactos aos prototypes por zona, evitando varrer repetidamente o JSON completo conforme a quantidade de zonas cresce. Checks independentes com `proc.num[]`, `net.tcp.listen[]` e `net.udp.listen[]` mantêm a visibilidade do daemon/listeners mesmo quando o statistics-channel está indisponível.
