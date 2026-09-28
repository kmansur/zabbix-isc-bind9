# Instalação

[English](../en/installation.md)

## 1. Configure o BIND

Adicione um listener de estatísticas restrito ao localhost:

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

Valide a configuração do BIND antes de recarregar o serviço.

## 2. Verifique localmente

Confirme que este endpoint retorna JSON no servidor monitorado:

```text
http://127.0.0.1:8053/json/v1/status
```

Não exponha este listener a redes não confiáveis.

## 3. Configure o Zabbix agent

Utilize Zabbix Agent 7.0+ ou Zabbix Agent 2 7.0+. Os passive checks devem funcionar para o host. As keys padrão `web.page.get[]`, `net.dns[]` e `net.dns.perf[]` devem estar disponíveis. Não é necessário plugin customizado nem parser externo.

## 4. Importe o template

Importe o arquivo correspondente ao Zabbix Server:

- `templates/7.0/isc-bind9-by-zabbix-agent.yaml`
- `templates/8.0/isc-bind9-by-zabbix-agent.yaml` para Zabbix 8.0; validado em runtime no Zabbix 8.0.0beta2

Vincule **ISC BIND by Zabbix agent** ao host e revise Latest data antes de encaminhar alertas para produção.

## 5. Configure o teste funcional de DNS

O template coleta os dados de saúde DNS UDP/TCP imediatamente, mas os alertas funcionais DNS ficam desabilitados por padrão.

Escolha um nome estável adequado ao papel do servidor e sobrescreva `{$BIND.DNS.TEST.NAME}` no host. Para um servidor autoritativo, utilize um registro servido pela própria instância BIND.

Valide os dois transportes localmente, por exemplo:

```text
zabbix_agentd -t 'net.dns[127.0.0.1,example.com,A,1,2,udp]'
zabbix_agentd -t 'net.dns[127.0.0.1,example.com,A,1,2,tcp]'
```

Os dois checks devem retornar `1`. Depois da validação, defina:

```text
{$BIND.DNS.TEST.ENABLED}=1
```

Não habilite os alertas funcionais antes de confirmar que o nome escolhido é válido para o servidor monitorado.
