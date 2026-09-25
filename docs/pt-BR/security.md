# Projeto de segurança

[English](../en/security.md)

O statistics-channel do BIND expõe informações operacionais e deve ser tratado como uma interface administrativa.

Os padrões do projeto seguem estes princípios:

- associar o statistics-channel ao loopback;
- permitir apenas localhost;
- utilizar active checks do Zabbix para aquisição local;
- não exigir permissões privilegiadas de controle do BIND;
- não realizar operações de escrita ou configuração;
- evitar programas externos de parsing.

Se as estatísticas precisarem ser coletadas por um endereço diferente de loopback, documente a exceção e restrinja-a pela ACL do BIND e pelos firewalls do host/rede.

O template não contém credenciais. Valores sensíveis da implantação devem utilizar os mecanismos normais de gerenciamento de segredos do Zabbix quando aplicável.
