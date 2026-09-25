# Histórico de alterações

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

## [Não publicado]

### Adicionado
- Monitoramento do resolver por view, incluindo contadores, tipos de query recursiva e descoberta ADB.
- Métricas de cache do resolver para hits/misses, evictions, nós e memória do cache.
- Métricas de memória do BIND a partir do endpoint nativo de memória.

### Corrigido
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
