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
   | active checks com web.page.get[]
   v
Itens mestres brutos
   |
   +--> dependent items
   +--> low-level discovery
   +--> triggers
```

O projeto evita scripts externos e caminhos privilegiados de controle. Dados brutos dos endpoints têm retenção curta, enquanto métricas numéricas derivadas mantêm histórico normal.

A primeira candidata utiliza `/json/v1/status`, `server`, `zones`, `mem`, `net` e `traffic`. Parsing adicional somente é incluído após validação entre versões.
