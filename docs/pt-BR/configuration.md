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


### Escolhendo o nome para o teste funcional de DNS

O padrão `{$BIND.DNS.TEST.NAME}=localhost` foi validado com sucesso no ambiente real Ubuntu 24.04/BIND 9.18.39 usado durante o desenvolvimento, mas não existe garantia de que toda configuração BIND responda esse nome.

Escolha um nome que represente o papel do servidor monitorado:

- **servidor autoritativo:** utilize um registro estável de uma zona que essa instância BIND deva responder autoritativamente;
- **resolver recursivo:** utilize um nome externo estável somente quando a recursão estiver intencionalmente habilitada e deva funcionar;
- **papel misto:** prefira um registro autoritativo estável para testar o daemon local e use monitoramento externo separado caso seja necessário medir a recursão fim a fim.

Antes de encaminhar alertas para produção, valide localmente o nome configurado em UDP e TCP usando os mesmos parâmetros de `net.dns[]` do template. Valor `1` significa que a consulta produziu resposta; valor `0` significa que a troca DNS não produziu uma resposta utilizável.
