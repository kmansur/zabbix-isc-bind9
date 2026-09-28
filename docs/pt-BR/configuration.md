# Configuração

[English](../en/configuration.md)

## Macros do template

| Macro | Padrão | Finalidade |
| --- | --- | --- |
| `{$BIND.DNS.TEST.SERVER}` | `127.0.0.1` | Endereço DNS consultado pelos checks nativos de saúde do Zabbix |
| `{$BIND.DNS.TEST.NAME}` | `localhost` | Nome DNS usado nos checks de disponibilidade e tempo de resposta |
| `{$BIND.DNS.TEST.TYPE}` | `A` | Tipo de registro DNS usado pelos checks nativos |
| `{$BIND.DNS.TEST.TIMEOUT}` | `1` | Timeout por tentativa de consulta DNS, em segundos |
| `{$BIND.DNS.TEST.COUNT}` | `2` | Quantidade de tentativas da consulta DNS |
| `{$BIND.DNS.FAIL.WINDOW}` | `3m` | Janela contínua de falha antes de gerar problema de disponibilidade |
| `{$BIND.DNS.RESPONSE.WARN}` | `0.1` | Limite de warning para o tempo médio de resposta DNS local, em segundos |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Limite da taxa média de queries descartadas para warning em 5 minutos |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | Limite da taxa média de SERVFAIL para warning em 5 minutos |
| `{$BIND.ZONE.EXPIRES.WARN}` | `1h` | Janela de aviso antes de uma zona secundária atingir o prazo de expiração |
| `{$BIND.ZONE.SECONDARY.MATCHES}` | `^$` | Regex que seleciona zonas secundárias para refresh/expiry por zona; o padrão não descobre nenhuma |
| `{$BIND.ZONE.DNSSEC.MATCHES}` | `^$` | Regex que seleciona zonas para monitoramento DNSSEC por zona; o padrão não descobre nenhuma |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Host usado pelo `web.page.get[]` para o statistics-channel do BIND |
| `{$BIND.STATS.NODATA}` | `10m` | Intervalo máximo sem estatísticas antes de gerar warning de monitoramento |
| `{$BIND.STATS.PORT}` | `8053` | Porta TCP local do statistics-channel do BIND |

Mantenha o listener de estatísticas no loopback sempre que possível. Se outro endereço local for necessário, restrinja o acesso pela ACL do BIND e pelos firewalls do host/rede.

## Statistics-channel do BIND

Configuração recomendada:

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

O template lê as estatísticas localmente através das keys padrão do Zabbix Agent. Não são necessárias permissões de controle/escrita no BIND.

## Checks nativos de saúde DNS

O template valida o serviço DNS independentemente do statistics-channel usando `net.dns[]` e `net.dns.perf[]` em UDP e TCP.

O teste padrão é:

```text
server: 127.0.0.1
name:   localhost
type:   A
```

A consulta `localhost/A` foi validada com sucesso no ambiente runtime Ubuntu 24.04/BIND 9.18.39 usado pelo projeto, mas nem toda configuração BIND é obrigada a responder esse nome.

> **Importante:** `localhost` só é um padrão seguro quando a instância BIND monitorada está realmente configurada para responder `localhost/A`. Em servidores exclusivamente autoritativos, essa consulta pode legitimamente não produzir uma resposta utilizável e gerar falsos positivos de indisponibilidade UDP/TCP. Para servidores autoritativos, sobrescreva `{$BIND.DNS.TEST.NAME}` no host ou no template com um registro estável de uma zona servida pela própria instância BIND. Por exemplo, se o servidor é autoritativo por `example.com`, utilize `example.com` ou outro nome estável dessa zona.

### Escolhendo o nome para o teste funcional de DNS

Escolha um nome que represente o papel do servidor monitorado:

- **servidor autoritativo:** utilize um registro estável de uma zona que essa instância BIND deva responder autoritativamente;
- **resolver recursivo:** utilize um nome externo estável somente quando a recursão estiver intencionalmente habilitada e deva funcionar;
- **papel misto:** prefira um registro autoritativo estável para testar a disponibilidade local do daemon e use monitoramento externo separado caso também precise medir a recursão fim a fim.

Antes de encaminhar alertas para produção, valide localmente o nome configurado em UDP e TCP usando os mesmos parâmetros de `net.dns[]` do template. Valor `1` significa que a consulta produziu uma resposta utilizável; valor `0` significa que não produziu.

## Monitoramento por zona

O detalhamento por zona é deliberadamente opt-in para controlar a cardinalidade.

Para monitorar todas as zonas secundárias quanto a refresh/expiry:

```text
{$BIND.ZONE.SECONDARY.MATCHES}=.*
```

Para habilitar contadores DNSSEC em todas as zonas que os exportam:

```text
{$BIND.ZONE.DNSSEC.MATCHES}=.*
```

Prefira uma regex direcionada quando apenas zonas críticas selecionadas precisarem de detalhamento individual.
