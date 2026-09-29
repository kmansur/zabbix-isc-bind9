# Histórico de alterações

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

## [Não publicado]

## [1.1.0] - 2026-09-29

### Validação

- Importação manual do template confirmada com sucesso em ambientes Zabbix 7 e Zabbix 8.
- Gates automatizados de fresh import, contratos live BIND 9.18/9.20, validação Python 3.11/3.13/3.14 e CodeQL passaram antes da promoção para a `main`.

### Adicionado

- Monitoramento independente do processo `named` e dos listeners UDP/TCP usando keys padrão do Zabbix agent.
- Intervalo configurável para teste DNS, filtros de discovery por view, limite de clientes recursivos e limite de DeleteLRU.
- Gauge dedicado de `RecursClients`, hit ratio do cache por view e serial SOA local para secundárias selecionadas.
- Hardening opcional documentado com `AllowKey`/`DenyKey` para o caminho `web.page.get[]` do statistics-channel.
- Cobertura de regressão no CI para zonas secundárias expiradas e allowlists de classificação de métricas.

### Alterado

- Adicionado dataset normalizado de zonas para interpretar o payload grande de `/json/v1/zones` uma única vez antes de LLD/prototypes por zona.
- Prototypes JSONPath dinâmicos passam a descartar valores temporariamente ausentes em vez de ficar unsupported ou inventar zero.
- Discoveries de resolver/cache/zonas usam filtros explícitos de view e todas as regras LLD usam lifetime explícito de 7 dias.
- Itens mestres HTTP/JSON brutos deixam de armazenar histórico; dependent items derivados continuam com histórico normal.
- A disponibilidade do statistics-channel passa a usar um heartbeat leve e armazenado derivado de `/json/v1/status`, preservando a avaliação do `nodata()` sem reter o JSON bruto.
- Item prototypes de cache passam a usar tags consistentes de componente/view.

### Corrigido

- Timers de expiração e refresh de zonas secundárias passam a ser explicitamente numéricos com sinal, permitindo manter zonas expiradas supported e acionar corretamente o trigger já existente.
- Adicionado trigger de restart baseado na redução do uptime do BIND.
- Removida a descoberta duplicada de `RecursClients`, que agora é exposto somente como item gauge dedicado.

## [1.0.2] - 2026-09-28

### Adicionado

- Adicionada a macro `{$BIND.DNS.TEST.ENABLED}`, com padrão `0`, para manter os alertas funcionais DNS silenciosos até que o administrador valide um nome de teste adequado ao servidor.
- Adicionados limites separados de tempo de resposta para UDP e TCP: `{$BIND.DNS.RESPONSE.UDP.WARN}` e `{$BIND.DNS.RESPONSE.TCP.WARN}`.
- Adicionada a versão JSON das estatísticas do BIND à dashboard operacional Overview.

### Alterado

- Os nomes dos problemas funcionais DNS agora descrevem falha no teste configurado, sem sugerir automaticamente que o daemon BIND está indisponível.
- Os eventos e dados operacionais dos problemas DNS passam a incluir o nome/tipo configurado para facilitar o diagnóstico.
- A documentação de instalação e configuração agora exige validar o nome de teste em UDP e TCP antes de definir `{$BIND.DNS.TEST.ENABLED}=1`.
- O baseline mantido para Zabbix Agent e Agent 2 passa a ser documentado como 7.0+.
- Removidas referências antigas a 1.0.0/1.0-0 da documentação atual de compatibilidade.

### Corrigido

- Evitados falsos positivos de DNS funcional causados pelo padrão genérico `localhost/A` em servidores BIND exclusivamente autoritativos.

## [1.0.1] - 2026-09-28

### Corrigido

- Corrigida a semântica de counters/gauges do BIND: `RecursClients`, high-water marks, valores de queries em andamento/fetch/bucket do resolver, tamanhos do ADB e sockets/clientes ativos deixam de ser tratados como taxas.
- Corrigida a fixture do BIND 9.18 para representar `memory.contexts` como array JSON, conforme o ISC BIND.
- Reconstruídas as tabelas de macros EN/pt-BR que estavam corrompidas e reforçada a validação da documentação.
- Corrigidas referências antigas a active checks no troubleshooting e o nome atual do projeto no NOTICE.

### Alterado

- Removidos todos os widgets `Item navigator` da dashboard após a validação de uso real mostrar que as listas extensas de Query Types, Response Codes, `nsstats`, resolver, sockets e zonas geravam ruído visual sem melhorar a operação diária.
- Reorganizada a página **DNS activity** em torno de taxas de queries, erros, tráfego DNS e tempo de resposta.
- Reorganizada a página **Resolver & resources** em torno dos graph prototypes de cache, memória, inventário de zonas e gráficos de transferências.
- Os detalhes descobertos por LLD continuam disponíveis em Latest data sem serem forçados na dashboard operacional.

## [1.0.0] - 2026-09-28

Primeira release estável para produção do **ISC BIND by Zabbix agent**.

### Validação

- Validação real em runtime no Ubuntu 24.04 com BIND 9.18.39 e Zabbix Agent clássico.
- Checks nativos de disponibilidade DNS UDP/TCP e tempo de resposta validados no ambiente real; tempos locais abaixo de 1 ms.
- Validação live do contrato do statistics-channel contra as imagens oficiais ISC BIND 9.18.50 e 9.20.29.
- Validação version-aware confirma ausência de `/json/v1/xfrins` no BIND 9.18 e presença no BIND 9.20.
- Checks de capacidade do Zabbix Agent clássico e Agent 2 executados contra instâncias BIND reais no CI.
- Gates de fresh-import para Zabbix 7.0 e imagens oficiais trunk de desenvolvimento do Zabbix 8.0.
- Python 3.11, 3.13 e 3.14 com lint, formatação, pytest, validação de templates e documentação bilíngue.
- Fixtures JSON do BIND 9.18/9.20 protegem as premissas de preprocessing e LLD.
- Paridade funcional completa entre os corpos dos templates 7.0 e 8.0 e suas definições de gráficos.
- Auditoria do template passivo confirma que não restam tipos ativos antigos, macros BIND9 legadas, macros LLD antigas, porta 8653, keys ou UUIDs compartilhados com a origem comunitária.

### Adicionado

- Disponibilidade DNS UDP/TCP e tempo de resposta usando `net.dns[]` e `net.dns.perf[]`.
- Versão do BIND, versão JSON das estatísticas, uptime e idade da configuração.
- Taxas IPv4/IPv6, recursão, queries descartadas e SERVFAIL.
- LLD de `nsstats`, tipos de query, response codes e estatísticas de sockets.
- Estatísticas do resolver, query types, ADB e cache por view do BIND.
- Memória em uso, memória malloced e contextos de memória.
- Contadores agregados de zonas totais, primárias e secundárias.
- Monitoramento opt-in de refresh/expiry de zonas secundárias com trigger prototypes.
- Contadores DNSSEC por zona em modo opt-in.
- Monitoramento de transferências recebidas do BIND 9.20 via `/json/v1/xfrins`, com compatibilidade limpa no BIND 9.18.
- Nove gráficos clássicos reutilizáveis.
- Três graph prototypes de cache por view.
- Dashboard nativa de três páginas `ISC BIND: Overview`: Overview, DNS activity e Resolver & resources.
- Navegadores dinâmicos para query types, response codes, nsstats, resolver, sockets e itens de zonas.
- CI, CodeQL, testes de higiene do repositório e documentação bilíngue EN/pt-BR.

### Alterado

- Identidade do template padronizada como `ISC BIND by Zabbix agent`.
- Checks passivos do Zabbix Agent são a arquitetura padrão; `ServerActive` não é necessário.
- Indisponibilidade do statistics-channel é Warning porque o serviço DNS é validado separadamente.
- Anomalias de SERVFAIL e queries descartadas são Warning e dependem da disponibilidade do statistics-channel.
- Monitoramento por zona é opt-in para manter baixa a cardinalidade padrão.
- Contadores opcionais zerados são normalizados ou omitidos com segurança em vez de gerar ruído unsupported.
- Descoberta de sockets utiliza `/json/v1/net`, conforme a semântica do BIND.
- `{$BIND.STATS.HOST}` usa `127.0.0.1`, pois path e porta são fornecidos separadamente ao `web.page.get[]`.

### Segurança

- Arquitetura somente leitura.
- statistics-channel restrito ao loopback por padrão.
- Não requer `sudo`, `rndc`, `system.run[]`, scripts externos, `curl`, `jq`, itens SSH/Telnet ou plugins exclusivos do Agent 2.
- Não requer permissão de escrita/controle no BIND.

## [0.4.0] - 2026-09-27

Linha final candidata de engenharia usada para validação de runtime, dashboard e CI antes da 1.0.0.
