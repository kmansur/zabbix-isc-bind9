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

O projeto evita scripts externos e caminhos privilegiados de controle. Dados brutos dos endpoints têm retenção curta, enquanto métricas numéricas derivadas mantêm histórico normal.

A versão 1.0.1 utiliza `/json/v1/status`, `server`, `zones`, `mem`, `net` e `traffic`, além do caminho version-aware `/json/v1/xfrins` no BIND 9.20. Parsing somente é promovido após validação entre versões.
