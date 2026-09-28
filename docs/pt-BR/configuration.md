# Configuração

[English](../en/configuration.md)

## Macros do template

| Macro | Padrão | Finalidade |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Host local do statistics-channel do BIND usado pelo `web.page.get[]` |
| `{$BIND.STATS.PORT}` | `8053` | Porta TCP do statistics-channel do BIND |
| `{$BIND.STATS.NODATA}` | `10m` | Intervalo máximo sem estatísticas antes de gerar warning de monitoramento |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Limite de warning para queries descartadas em queries por segundo |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | Limite de warning para SERVFAIL em respostas por segundo |
| `{$BIND.ZONE.EXPIRES.WARN}` | `1h` | Janela de aviso antes da expiração SOA de uma zona secundária habilitada para monitoramento |
| `{$BIND.ZONE.SECONDARY.MATCHES}` | `^$` | Regex que seleciona zonas secundárias para refresh/expiry por zona; o padrão não seleciona nenhuma |
| `{$BIND.ZONE.DNSSEC.MATCHES}` | `^$` | Regex que seleciona zonas para detalhamento DNSSEC; o padrão não seleciona nenhuma |
| `{$BIND.DNS.TEST.SERVER}` | `127.0.0.1` | Endereço do DNS consultado pelos checks nativos de saúde do Zabbix |
| `{$BIND.DNS.TEST.NAME}` | `localhost` | Nome DNS usado no teste funcional de disponibilidade/performance |
| `{$BIND.DNS.TEST.TYPE}` | `A` | Tipo de registro DNS usado no teste funcional |
| `{$BIND.DNS.TEST.TIMEOUT}` | `1` | Timeout por tentativa de consulta em segundos |
| `{$BIND.DNS.TEST.COUNT}` | `2` | Quantidade de tentativas da consulta DNS |
| `{$BIND.DNS.FAIL.WINDOW}` | `3m` | Janela contínua de falha antes de gerar problema de disponibilidade UDP/TCP |
| `{$BIND.DNS.RESPONSE.WARN}` | `0.1` | Limite de warning para o tempo médio de resposta DNS local em segundos |

Mantenha o listener de estatísticas no loopback sempre que possível. Se outro endereço local for necessário, restrinja o acesso pela ACL do BIND e pelos firewalls do host/rede.

## Checks funcionais de saúde DNS

O statistics-channel prova que a interface de monitoramento do BIND está disponível; ele não prova que o serviço DNS esteja respondendo consultas úteis. Por isso o template também usa as keys padrão `net.dns[]` e `net.dns.perf[]` do Zabbix agent.

A consulta padrão `localhost/A` foi validada no ambiente runtime Ubuntu 24.04/BIND 9.18.39 do projeto, mas não há garantia de que toda implantação BIND responda esse nome.

Escolha um nome que represente o papel do servidor monitorado:

- **servidor autoritativo:** use um registro estável de uma zona que esta instância BIND deva responder autoritativamente;
- **resolver recursivo:** use um nome externo estável somente quando a recursão estiver intencionalmente habilitada e deva funcionar;
- **papel misto:** prefira um registro autoritativo estável para a disponibilidade local do daemon e use monitoramento externo separado quando precisar medir recursão fim a fim.

Antes de encaminhar alertas para produção, teste localmente o nome configurado em UDP e TCP com os mesmos parâmetros de `net.dns[]` do template. Valor `1` significa que a consulta produziu resposta utilizável; `0` significa que não produziu.

## Monitoramento opcional por zona

O monitoramento por zona fica desabilitado por padrão para manter a cardinalidade previsível.

Para monitorar refresh/expiry de todas as zonas secundárias:

```text
{$BIND.ZONE.SECONDARY.MATCHES}=.*
```

Para selecionar somente algumas zonas, use uma expressão regular ancorada, por exemplo:

```text
{$BIND.ZONE.SECONDARY.MATCHES}=^(example\.com|example\.net)$
```

Os contadores DNSSEC por zona seguem o mesmo modelo através de `{$BIND.ZONE.DNSSEC.MATCHES}`. Use `.*` somente quando o aumento de cardinalidade for intencional.
