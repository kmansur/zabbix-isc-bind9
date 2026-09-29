# Dashboard e gráficos

[English](../en/dashboard.md)

A versão 1.1.0 fornece uma dashboard nativa do Zabbix mais enxuta e gráficos clássicos reutilizáveis.

## Dashboard do template

A dashboard se chama **ISC BIND: Overview** e possui três páginas.

### Overview

A primeira página foi pensada para operação diária. Ela inclui:

- versão do BIND;
- uptime;
- quantidade total de zonas, primárias e secundárias;
- memória em uso;
- estado DNS UDP/TCP;
- versão JSON das estatísticas do BIND;
- gráfico de tempo de resposta DNS local;
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
- gráfico de tempo de resposta DNS local.

Os detalhes de Query Types, Response Codes e `nsstats` continuam disponíveis em Latest data, mas deixam de ser listados em navegadores na dashboard para manter a visão operacional mais limpa.

### Resolver & resources

Esta página concentra o resolver recursivo e diagnósticos de recursos:

- graph prototypes do cache por view para hits/misses, memória e quantidade de nós;
- gráfico de memória;
- inventário de zonas;
- transferências recebidas;
- taxa de transferência.

Os detalhes de resolver, sockets e itens por zona continuam disponíveis em Latest data. Os itens individuais de zonas secundárias e DNSSEC continuam opt-in pelas macros correspondentes.

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
- `BIND: DNS query response time`

Os gráficos foram baseados deliberadamente em itens estáveis e de baixa cardinalidade. Famílias dinâmicas de LLD, como query types, response codes, resolver e sockets, continuam disponíveis em Latest data sem poluir a dashboard.
