# Dashboard e gráficos

[English](../en/dashboard.md)

A versão 0.2.0 adiciona uma dashboard nativa de template do Zabbix e gráficos clássicos reutilizáveis.

## Dashboard do template

A dashboard se chama **ISC BIND: Overview** e possui três páginas.

### Overview

A primeira página foi pensada para operação diária. Ela inclui:

- versão do BIND;
- uptime;
- quantidade total de zonas, primárias e secundárias;
- memória em uso;
- gráfico de taxa de queries;
- gráfico de erros de query;
- gráfico de tráfego DNS UDP/TCP;
- gráfico de memória;
- gráfico de timing do servidor;
- gráfico de transferências recebidas;
- problemas atuais.

### DNS activity

Esta página concentra o comportamento das consultas e os resultados do protocolo DNS:

- taxas IPv4, IPv6 e recursivas;
- taxas de SERVFAIL e queries descartadas;
- requests e responses UDP/TCP;
- navegador dinâmico de Query Types;
- navegador dinâmico de Response Codes;
- navegador dinâmico dos contadores `nsstats`.

Os navegadores usam as tags dos itens do template. Assim, novos contadores descobertos por LLD aparecem automaticamente sem necessidade de alterar a dashboard.

### Resolver & resources

Esta página concentra o resolver recursivo e diagnósticos de recursos:

- contadores do resolver agrupados por view do BIND;
- estatísticas de sockets;
- gráfico de memória;
- inventário de zonas;
- transferências recebidas;
- taxa de transferência;
- navegador de itens relacionados a zonas.

Os itens individuais de zonas secundárias e DNSSEC continuam opt-in. Quando habilitados pelas macros correspondentes, eles passam a aparecer automaticamente no navegador de zonas.

## Gráficos clássicos

O template também fornece gráficos reutilizáveis fora da dashboard:

- `BIND: Query rates`
- `BIND: Query errors`
- `BIND: DNS transport traffic`
- `BIND: Memory usage`
- `BIND: Zone inventory`
- `BIND: Incoming transfers`
- `BIND: Incoming transfer rate`
- `BIND: Server timing`

Os gráficos foram baseados deliberadamente em itens estáveis e de baixa cardinalidade. Famílias dinâmicas de LLD, como query types, response codes, resolver e sockets, são apresentadas através dos navegadores da dashboard em vez de gerar grande quantidade de graph prototypes.
