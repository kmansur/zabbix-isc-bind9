# Métricas

[English](../en/metrics.md)

A versão 0.1.0 separa a aquisição bruta dos endpoints das métricas cuja semântica já foi validada.

## Interpretado na 0.1.0

- versão do BIND e versão JSON das estatísticas;
- uptime do servidor e tempo desde a última configuração;
- taxas de requests IPv4 e IPv6;
- taxas de queries descartadas, SERVFAIL e recursão;
- low-level discovery de `nsstats`, `qtypes`, `rcodes` e `sockstats`;
- descoberta de zonas entre as views, incluindo tipo, serial SOA e idade de carregamento;
- taxas agregadas UDP/TCP de requests e responses derivadas dos histogramas de tráfego do BIND.

## Coletado bruto para implementação em etapas

- `/json/v1/mem`;
- `/json/v1/net`.

Esses blocos são coletados sem triggers de produção até que os campos e a semântica estejam validados entre as branches suportadas do BIND.

## Modelo de retenção

Itens mestres JSON brutos possuem histórico curto e sem trends. Métricas numéricas derivadas mantêm histórico/trends normais para evitar crescimento desnecessário do banco do Zabbix.
