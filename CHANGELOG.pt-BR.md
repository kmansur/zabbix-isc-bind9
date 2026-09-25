# Histórico de alterações

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

## [Não publicado]

### Validação
- Concluída a auditoria de limpeza do template passivo contra o template comunitário original: não restam tipos de item ativos, macros BIND9 antigas, macros LLD antigas, porta 8653, keys compartilhadas ou UUIDs compartilhados. O nome do projeto original permanece apenas na atribuição de licença.
- O CI valida Python 3.11, 3.13 e 3.14, estrutura do template, documentação bilíngue e importação limpa no Zabbix 7.0.

### Adicionado
- Monitoramento compatível de transferências recebidas do BIND 9.20 via `/json/v1/xfrins`, com indicador de compatibilidade e sem itens unsupported no BIND 9.18.
- Timers de refresh e expiração de zonas secundárias com prototypes de trigger.
- Descoberta de contadores DNSSEC de assinatura/refresh para zonas que exportam `dnssec-sign`/`dnssec-refresh`.
- Monitoramento do resolver por view, incluindo contadores, tipos de query recursiva e descoberta ADB.
- Métricas de cache do resolver para hits/misses, evictions, nós e memória do cache.
- Métricas de memória do BIND a partir do endpoint nativo de memória.
- Contadores agregados para zonas totais, primárias e secundárias.

### Alterado
- Renomeado o template de `ISC BIND 9 by Zabbix Agent` para `ISC BIND by Zabbix agent`. O nome do repositório permanece inalterado.
- A descoberta individual de refresh/expiry das zonas secundárias passa a ser opt-in via `{$BIND.ZONE.SECONDARY.MATCHES}`; o padrão `^$` não cria itens individuais por zona secundária.
- Removida a descoberta padrão de serial SOA e idade de carregamento para todas as zonas; o template base passa a usar contadores agregados de zonas totais/primárias/secundárias.
- A descoberta DNSSEC por zona passa a ser opt-in via `{$BIND.ZONE.DNSSEC.MATCHES}` para controlar cardinalidade.
- Contadores opcionais do BIND com valor zero passam a ser normalizados para zero em vez de ficarem unsupported.
- Alterado o padrão dos itens mestres de active para passive Zabbix agent checks. Isso remove a dependência de `ServerActive` e mantém compatibilidade com Agent 2.

### Corrigido
- Corrigido `{$BIND.STATS.HOST}` para usar `127.0.0.1` em vez de URL completa quando `web.page.get[]` também fornece path e porta.
- A descoberta de estatísticas de socket agora utiliza `/json/v1/net`, conforme a semântica do statistics-channel do BIND.

## [0.1.4] - 2026-09-25

Candidata atual de engenharia. Ainda não existe release promovida como estável para produção.
