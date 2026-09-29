# Métricas

[English](../en/metrics.md)

A versão 1.1.0 separa a aquisição bruta dos endpoints das métricas cuja semântica já foi validada.

## Interpretado na 1.0.x

- versão do BIND e versão JSON das estatísticas;
- uptime do servidor e tempo desde a última configuração;
- taxas de requests IPv4 e IPv6;
- taxas de queries descartadas, SERVFAIL e recursão;
- low-level discovery de `nsstats`, `qtypes` de queries recebidas pelo servidor, `rcodes` e `sockstats` de rede;
- descoberta do resolver por view para estatísticas, tipos de query recursiva e contadores ADB;
- métricas de cache do resolver por view: hits/misses, hit ratio, query hits/misses, remoções LRU/TTL, covering NSEC, nós e memória do cache;
- memória em uso pelo BIND, memória malloced e quantidade de contextos de memória;
- contadores agregados de zonas (total, primárias e secundárias), sem criar item para cada zona;
- timers de refresh/expire de zonas secundárias, serial SOA local e prototypes de alerta para proximidade de expiração e zona expirada;
- contadores DNSSEC de assinatura e refresh descobertos somente nas zonas que realmente exportam `dnssec-sign`/`dnssec-refresh`;
- taxas agregadas UDP/TCP de requests e responses derivadas dos histogramas de tráfego do BIND.

## Retenção dos endpoints brutos

Os itens HTTP/JSON brutos são mestres somente para preprocessing e utilizam `history: 0`. Os dependent items continuam recebendo o valor atual do master, enquanto o payload bruto grande deixa de ser gravado no histórico. Isso é especialmente importante para `/json/v1/zones` em servidores com muitas zonas.

## Modelo de retenção

Os masters JSON brutos e o dataset normalizado de zonas não armazenam histórico. As métricas numéricas derivadas mantêm histórico/trends normais, reduzindo crescimento do banco sem remover dados operacionais.

## Semântica dos contadores agregados de zonas

`bind.zones.total` conta todos os objetos de zona expostos pelo endpoint de estatísticas do BIND. `bind.zones.primary` e `bind.zones.secondary` contam somente esses dois tipos específicos. O BIND suporta outros tipos, como hint, forward, stub, static-stub, mirror e redirect; portanto, **não é esperado que total seja igual a primárias + secundárias**.

Uma futura release minor pode adicionar um contador "other zones" ou detalhamento por tipo sem alterar as keys existentes.

## Nível de estatísticas por zona

O endpoint de zonas do BIND pode expor identidade, serial e timers. Os contadores agregados permanecem sempre disponíveis, enquanto refresh/expiry e o serial local por secundária são opt-in. Os contadores DNSSEC por zona exigem `zone-statistics full` no BIND para as zonas relevantes. Quando esses blocos não existem, a descoberta DNSSEC fica vazia e o template comum não cria itens DNSSEC unsupported.

## Monitoramento de transferências recebidas

O BIND 9.20 expõe o endpoint JSON `/json/v1/xfrins`. O template comum consulta esse endpoint sem transformar hosts 9.18 em unsupported. Em versões sem o endpoint, `bind.xfrins.supported` retorna `0` e as métricas de transferência permanecem em zero. No BIND 9.20, o template coleta quantidade de transferências ativas/em fila, transferências deferred, bytes atuais e taxa agregada.

## Política de detalhamento por zona

O template base evita deliberadamente descobrir serial SOA e idade de carregamento para todas as zonas. O serial local é exposto apenas para zonas secundárias selecionadas por `{$BIND.ZONE.SECONDARY.MATCHES}`. Em servidores autoritativos com centenas ou milhares de zonas, isso aumenta muito a cardinalidade sem oferecer informação de saúde suficiente isoladamente. A expiração de zonas secundárias continua disponível por zona porque cada secundária pode expirar de forma independente, mas passa a ser opt-in através de `{$BIND.ZONE.SECONDARY.MATCHES}` para manter baixa a cardinalidade padrão do template. Os contadores DNSSEC por zona são opt-in através de `{$BIND.ZONE.DNSSEC.MATCHES}`; o padrão `^$` não descobre nenhuma zona. Use uma expressão regular direcionada ou `.*` apenas quando o detalhamento DNSSEC completo for realmente necessário.


## Semântica de counters e gauges

As estatísticas do BIND misturam contadores cumulativos de eventos e gauges que representam valores instantâneos. A versão 1.1.0 separa explicitamente essas classes para que gauges nunca sejam processados com `CHANGE_PER_SECOND`.

As famílias de taxa incluem contadores cumulativos de queries/requests/responses/erros e eventos de sockets. Entre os gauges estão:

- `nsstats`: `RecursClients`, `TCPConnHighWater` e, no BIND 9.20, `RecursHighwater`;
- estatísticas do resolver: `QueryCurUDP`, `QueryCurTCP`, `NumFetch` e `BucketSize`;
- ADB do resolver: `nentries`, `entriescnt`, `nnames` e `namescnt`;
- sockets: valores de sockets ativos e clientes atualmente conectados, como `UDP4Active`, `TCP4Active` e `TCP4Clients`.

As discoveries genéricas de taxa excluem esses gauges. Discoveries específicas de gauge expõem diretamente o valor atual. Isso evita valores enganosos como “RecursClients per second”.


## Sinais independentes de serviço e capacidade

O template passa a separar a saúde do statistics-channel da saúde local do daemon/listeners usando `proc.num[{$BIND.PROCESS.NAME}]`, `net.tcp.listen[{$BIND.DNS.PORT}]` e `net.udp.listen[{$BIND.DNS.PORT}]`. Também promove `RecursClients` para um gauge dedicado e expõe hit ratio do cache por view.

Os triggers opcionais de saturação de clientes recursivos e DeleteLRU ficam desabilitados por padrão através do valor de limite `0`; o administrador os habilita escolhendo limites positivos adequados ao ambiente.
