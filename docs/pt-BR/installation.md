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

Pode ser utilizado Zabbix Agent ou Zabbix Agent 2. Os passive checks devem funcionar para o host. Não é necessário plugin customizado nem parser externo.

## 4. Importe o template

Importe o arquivo correspondente ao Zabbix Server:

- `templates/7.0/isc-bind9-by-zabbix-agent.yaml`
- `templates/8.0/isc-bind9-by-zabbix-agent.yaml` para validação de compatibilidade

Vincule **ISC BIND 9 by Zabbix Agent** ao host e revise Latest data antes de encaminhar alertas para produção.
