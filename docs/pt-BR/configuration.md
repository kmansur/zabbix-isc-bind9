# Configuração

[English](../en/configuration.md)

## Macros do template

| Macro | Padrão | Finalidade |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Host local das estatísticas |
| `{$BIND.STATS.PORT}` | `8053` | Porta TCP das estatísticas |
| `{$BIND.STATS.NODATA}` | `10m` | Limite sem dados |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Limite de queries descartadas |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | Limite de SERVFAIL |
| `{$BIND.ZONE.EXPIRES.WARN}` | `1h` | Janela de aviso antes da expiração de uma zona secundária |
| `{$BIND.ZONE.SECONDARY.MATCHES}` | `^# Configuração

[English](../en/configuration.md)

## Macros do template

| Macro | Padrão | Finalidade |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Host local das estatísticas |
| `{$BIND.STATS.PORT}` | `8053` | Porta TCP das estatísticas |
| `{$BIND.STATS.NODATA}` | `10m` | Limite sem dados |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Limite de queries descartadas |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | Limite de SERVFAIL |
 | Regex que seleciona zonas secundárias para monitoramento individual de refresh/expiry; o padrão desabilita a descoberta |
| `{$BIND.ZONE.DNSSEC.MATCHES}` | `^# Configuração

[English](../en/configuration.md)

## Macros do template

| Macro | Padrão | Finalidade |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Host local das estatísticas |
| `{$BIND.STATS.PORT}` | `8053` | Porta TCP das estatísticas |
| `{$BIND.STATS.NODATA}` | `10m` | Limite sem dados |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Limite de queries descartadas |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | Limite de SERVFAIL |
 | Regex que seleciona zonas para detalhamento DNSSEC por zona; o padrão desabilita a descoberta |

Mantenha o listener no loopback sempre que possível. Se outro endereço local for necessário, restrinja o acesso pela ACL do BIND e pelos firewalls do host/rede.


## Verificações nativas de saúde do DNS

O template valida o serviço DNS de forma independente do statistics-channel.

| Macro | Padrão | Finalidade |
| --- | --- | --- |
| `{$BIND.DNS.TEST.SERVER}` | `127.0.0.1` | Endereço DNS consultado pelo agent |
| `{$BIND.DNS.TEST.NAME}` | `localhost` | Nome DNS usado na consulta de teste |
| `{$BIND.DNS.TEST.TYPE}` | `A` | Tipo de registro DNS |
| `{$BIND.DNS.TEST.TIMEOUT}` | `1` | Timeout por tentativa em segundos |
| `{$BIND.DNS.TEST.COUNT}` | `2` | Quantidade de tentativas |
| `{$BIND.DNS.FAIL.WINDOW}` | `3m` | Janela contínua de falha antes do problema de disponibilidade |
| `{$BIND.DNS.RESPONSE.WARN}` | `0.1` | Limite de warning para o tempo médio de resposta em segundos |

A consulta padrão `localhost/A` é um teste local de baixo custo. Altere nome/tipo no host caso o BIND monitorado não responda essa consulta.
