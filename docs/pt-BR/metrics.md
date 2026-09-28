# Métricas

[English](../en/metrics.md)

O template separa a aquisição bruta dos endpoints das métricas derivadas e diferencia explicitamente **contadores monotônicos** de **gauges de valor atual**.

## Serviço e identificação

- versão do BIND e versão JSON das estatísticas;
- uptime e tempo desde a última configuração;
- disponibilidade funcional DNS UDP/TCP através de `net.dns[]`;
- tempo de resposta DNS UDP/TCP através de `net.dns.perf[]`.

## Queries e estatísticas do servidor

Os itens fixos de taxa incluem:

- requests IPv4 e IPv6 por segundo;
- queries descartadas por segundo;
- respostas SERVFAIL por segundo;
- queries recursivas por segundo.

A descoberta genérica de `nsstats` converte contadores monotônicos de eventos em taxas. Valores que não são contadores são excluídos da conversão e coletados separadamente como gauges:

- high-water de conexões TCP;
- high-water de clientes recursivos;
- clientes recursivos atuais.

## Métricas do resolver por view

O monitoramento do resolver é sensível à view.

Contadores monotônicos do resolver e tipos de query recursiva são descobertos e convertidos em taxas. Gauges de estado atual são coletados separadamente:

- queries UDP em andamento;
- queries TCP em andamento;
- fetches ativos;
- tamanho de bucket.

Os valores ADB são gauges, e não contadores de eventos. O template expõe:

- tamanho da hash table de endereços;
- endereços presentes na hash table;
- tamanho da hash table de nomes;
- nomes presentes na hash table.

## Cache do resolver

As métricas de cache por view incluem:

**Taxas**

- cache hits e misses;
- query hits e misses;
- remoções LRU;
- remoções por TTL;
- resultados covering NSEC.

**Gauges**

- nós do cache;
- nós auxiliares NSEC;
- memória em uso na árvore do cache;
- memória em uso no heap do cache.

Graph prototypes fornecem visões de hit/miss, memória e nós para cada view descoberta.

## Estatísticas de sockets

A descoberta genérica de sockets converte eventos monotônicos, como opens, closes, falhas, connects, accepts e erros de envio/recepção, em taxas.

O estado atual dos sockets é coletado separadamente como gauge:

- sockets UDP/IPv4 e UDP/IPv6 ativos;
- sockets TCP/IPv4 e TCP/IPv6 ativos;
- clientes TCP/IPv4 e TCP/IPv6 conectados atualmente.

## Memória

As métricas comuns são:

- memória em uso;
- memória malloced;
- quantidade de contextos de memória ativos.

O membro `contexts` é validado como array JSON tanto nas fixtures quanto nos checks live de contrato do BIND.

## Inventário de zonas

O template base não cria um item para cada zona. O inventário agregado é dividido em:

- todas as zonas;
- zonas primárias;
- zonas secundárias;
- zonas built-in;
- outros tipos de zona, como mirror, stub, static-stub, DLZ ou redirect quando existentes.

Assim o total pode ser reconciliado sem aumentar a cardinalidade por zona.

## Monitoramento opcional por zona

Refresh/expiry de zonas secundárias é opt-in através de `{$BIND.ZONE.SECONDARY.MATCHES}`.

Contadores DNSSEC de assinatura/refresh são opt-in através de `{$BIND.ZONE.DNSSEC.MATCHES}` e dependem de o BIND exportar as estatísticas correspondentes. Se um valor por zona desaparecer temporariamente, o preprocessing descarta a amostra em vez de deixar o item unsupported.

## Tráfego

Taxas agregadas de requests e responses UDP/TCP são derivadas dos histogramas de tráfego do BIND para IPv4 e IPv6.

## Transferências recebidas

O BIND 9.20 expõe `/json/v1/xfrins`. O template coleta:

- quantidade de transferências recebidas ativas/em fila;
- transferências deferred;
- bytes atuais transferidos;
- taxa agregada de transferência.

`bind.xfrins.supported` informa se o endpoint está disponível. No BIND 9.18, onde esse endpoint não existe, as métricas de transferência são descartadas em vez de informar falsos valores zero.

## Retenção dos endpoints brutos

As seguintes aquisições brutas usam histórico curto e sem trends:

- `/json/v1/status`;
- `/json/v1/server`;
- `/json/v1/zones`;
- `/json/v1/mem`;
- `/json/v1/net`;
- `/json/v1/traffic`;
- `/json/v1/xfrins` quando disponível.

Itens numéricos derivados mantêm histórico/trends normais para evitar que payloads JSON brutos aumentem desnecessariamente o banco do Zabbix.

## Política de cardinalidade

Dados de alta cardinalidade são opt-in. O padrão prioriza saúde global, comportamento do protocolo e métricas por view com cardinalidade limitada. Detalhes por zona somente são ativados quando o operador seleciona explicitamente as zonas.
