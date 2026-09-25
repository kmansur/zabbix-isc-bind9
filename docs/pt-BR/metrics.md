# Métricas

[English](../en/metrics.md)

A versão 0.1.0 separa a aquisição bruta dos endpoints das métricas cuja semântica já foi validada.

## Interpretado na 0.1.0

- versão do BIND e versão JSON das estatísticas;
- uptime do servidor e tempo desde a última configuração;
- taxas de requests IPv4 e IPv6;
- taxas de queries descartadas, SERVFAIL e recursão;
- low-level discovery de `nsstats`, `qtypes` autoritativos, `rcodes` e `sockstats` de rede;
- descoberta do resolver por view para estatísticas, tipos de query recursiva e contadores ADB;
- métricas de cache do resolver por view: hits/misses, query hits/misses, remoções LRU/TTL, covering NSEC, nós e memória do cache;
- memória em uso pelo BIND, memória malloced e quantidade de contextos de memória;
- descoberta de zonas entre as views, incluindo tipo, serial SOA e idade de carregamento;
- timers de refresh/expire de zonas secundárias, com prototypes de alerta para proximidade de expiração e zona expirada;
- contadores DNSSEC de assinatura e refresh descobertos somente nas zonas que realmente exportam `dnssec-sign`/`dnssec-refresh`;
- taxas agregadas UDP/TCP de requests e responses derivadas dos histogramas de tráfego do BIND.

## Retenção dos endpoints brutos

Os payloads `/json/v1/mem` e `/json/v1/net` continuam disponíveis como itens mestres de retenção curta. Campos comuns estáveis são convertidos em dependent items, enquanto campos específicos de versão não são promovidos sem evidência de compatibilidade.

## Modelo de retenção

Itens mestres JSON brutos possuem histórico curto e sem trends. Métricas numéricas derivadas mantêm histórico/trends normais para evitar crescimento desnecessário do banco do Zabbix.

## Nível de estatísticas por zona

Identidade da zona, serial e timers básicos não exigem contadores completos por zona. Os contadores DNSSEC por zona exigem `zone-statistics full` no BIND para as zonas relevantes. Quando esses blocos não existem, a descoberta DNSSEC fica vazia e o template comum não cria itens DNSSEC unsupported.
