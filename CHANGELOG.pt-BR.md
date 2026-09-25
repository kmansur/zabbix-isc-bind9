# Histórico de alterações

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

## [Não publicado]

### Adicionado
- Adicionado monitoramento compatível de transferências recebidas do BIND 9.20 via `/json/v1/xfrins`, com indicador de compatibilidade e sem itens unsupported no BIND 9.18.
- Timers de refresh e expiração de zonas secundárias com prototypes de trigger.
- Descoberta de contadores DNSSEC de assinatura/refresh somente para zonas que exportam essas estatísticas.
- Monitoramento do resolver por view, incluindo contadores, tipos de query recursiva e descoberta ADB.
- Métricas de cache do resolver para hits/misses, evictions, nós e memória do cache.
- Métricas de memória do BIND a partir do endpoint nativo de memória.

### Alterado
- Alterado o padrão dos itens mestres de active para passive Zabbix agent checks. Isso remove a dependência de ServerActive e corresponde ao modelo comum do Agent clássico, mantendo compatibilidade com Agent 2.

### Corrigido
- Corrigido `{$BIND.STATS.HOST}` para usar `127.0.0.1` em vez de URL completa quando `web.page.get[]` também fornece path e porta.
- A descoberta de estatísticas de socket agora utiliza `/json/v1/net`, conforme a semântica do statistics-channel do BIND.

### Adicionado
- Estrutura inicial do projeto e documentação bilíngue.
- Arquitetura neutra para Zabbix Agent clássico e Zabbix Agent 2.
- Coleta das estatísticas JSON do BIND pelo statistics-channel local.
- Projeto inicial de LLD dos contadores do servidor e descoberta de zonas.
- Exports versionados para Zabbix 7.0 e 8.0.
- Baseline de validação do repositório e CI.

## [0.1.0] - 2026-09-25

Candidata inicial de engenharia. Ainda não existe release promovida como estável para produção.
