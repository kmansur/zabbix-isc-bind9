# Projeto de segurança

[English](../en/security.md)

O statistics-channel do BIND expõe informações operacionais e deve ser tratado como uma interface administrativa.

Os padrões do projeto seguem estes princípios:

- associar o statistics-channel ao loopback;
- permitir apenas localhost;
- utilizar checks passivos padrão do Zabbix agent para aquisição local;
- não exigir permissões privilegiadas de controle do BIND;
- não realizar operações de escrita ou configuração;
- evitar programas externos de parsing.

Se as estatísticas precisarem ser coletadas por um endereço diferente de loopback, documente a exceção e restrinja-a pela ACL do BIND e pelos firewalls do host/rede.

O template não contém credenciais. Valores sensíveis da implantação devem utilizar os mecanismos normais de gerenciamento de segredos do Zabbix quando aplicável.

## Hardening opcional das keys do Zabbix agent

O template precisa apenas de keys padrão e somente leitura. Administradores que desejarem uma restrição adicional no próprio agent podem permitir explicitamente os caminhos locais de estatísticas do BIND e negar outros usos de `web.page.get[]`.

Exemplo para o listener padrão:

```ini
AllowKey=web.page.get[127.0.0.1,/json/v1/*,8053]
DenyKey=web.page.get[*]
```

Adapte endereço e porta quando `{$BIND.STATS.HOST}` ou `{$BIND.STATS.PORT}` forem diferentes dos padrões. Valide a configuração exata tanto no Zabbix Agent clássico quanto no Agent 2 antes da implantação. O CI do projeto testa esse modelo allow/deny contra um statistics-channel BIND real.

Esse hardening é opcional porque instalações existentes do agent podem utilizar `web.page.get[]` em outros templates. Não aplique um deny genérico sem antes revisar essas dependências.
