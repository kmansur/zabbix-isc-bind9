# Histórico de alterações

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

## [Não publicado]

### Validação
- Adicionadas fixtures de contrato JSON do BIND 9.18/9.20 e cobertura pytest para as estruturas de endpoint usadas pelo preprocessing e LLD.
- Adicionado gate de fresh-import do Zabbix 8.0 trunk no CI usando as imagens Docker oficiais de desenvolvimento.
- Concluída a auditoria de limpeza do template passivo contra o template comunitário original: não restam tipos de item ativos, macros BIND9 antigas, macros LLD antigas, porta 8653, keys compartilhadas ou UUIDs compartilhados. O nome do projeto original permanece apenas na atribuição de licença.
- O CI valida Python 3.11, 3.13 e 3.14, estrutura do template, documentação bilíngue e importação limpa no Zabbix 7.0.

### Adicionado
- Adicionados cards de saúde DNS UDP/TCP e gráfico de tempo de resposta DNS local na página Overview.
- Adicionadas verificações nativas de disponibilidade real do serviço DNS via UDP/TCP e tempo de resposta usando `net.dns` e `net.dns.perf`.
- Adicionado o gráfico `BIND: DNS query response time` e value map de estado do serviço.
- Adicionados oito gráficos clássicos reutilizáveis e a dashboard nativa de três páginas `ISC BIND: Overview`.
- Adicionados navegadores dinâmicos na dashboard para query types, response codes, nsstats, resolver, sockets e itens relacionados a zonas.
- Adicionados graph prototypes do cache do resolver por view para hits/misses, memória e quantidade de nós.
- Monitoramento compatível de transferências recebidas do BIND 9.20 via `/json/v1/xfrins`, com indicador de compatibilidade e sem itens unsupported no BIND 9.18.
- Timers de refresh e expiração de zonas secundárias com prototypes de trigger.
- Descoberta de contadores DNSSEC de assinatura/refresh para zonas que exportam `dnssec-sign`/`dnssec-refresh`.
- Monitoramento do resolver por view, incluindo contadores, tipos de query recursiva e descoberta ADB.
- Métricas de cache do resolver para hits/misses, evictions, nós e memória do cache.
- Métricas de memória do BIND a partir do endpoint nativo de memória.
- Contadores agregados para zonas totais, primárias e secundárias.

### Alterado
- A indisponibilidade do statistics-channel passa a ser Warning porque a disponibilidade do serviço DNS é monitorada independentemente.
- Anomalias de SERVFAIL e queries descartadas passam a Warning e dependem da disponibilidade do statistics-channel.
- Renomeado o template de `ISC BIND 9 by Zabbix Agent` para `ISC BIND by Zabbix agent`. O nome do repositório permanece inalterado.
- A descoberta individual de refresh/expiry das zonas secundárias passa a ser opt-in via `{$BIND.ZONE.SECONDARY.MATCHES}`; o padrão `^$` não cria itens individuais por zona secundária.
- Removida a descoberta padrão de serial SOA e idade de carregamento para todas as zonas; o template base passa a usar contadores agregados de zonas totais/primárias/secundárias.
- A descoberta DNSSEC por zona passa a ser opt-in via `{$BIND.ZONE.DNSSEC.MATCHES}` para controlar cardinalidade.
- Contadores opcionais do BIND com valor zero passam a ser normalizados para zero em vez de ficarem unsupported.
- Alterado o padrão dos itens mestres de active para passive Zabbix agent checks. Isso remove a dependência de `ServerActive` e mantém compatibilidade com Agent 2.

### Corrigido
- Corrigido `{$BIND.STATS.HOST}` para usar `127.0.0.1` em vez de URL completa quando `web.page.get[]` também fornece path e porta.
- A descoberta de estatísticas de socket agora utiliza `/json/v1/net`, conforme a semântica do statistics-channel do BIND.

## [0.4.0] - 2026-09-27

Candidata de engenharia com dashboard/gráficos. Ainda não existe release promovida como estável para produção.
