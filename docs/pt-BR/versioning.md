# Versionamento

[English](../en/versioning.md)

O projeto utiliza Versionamento Semântico.

```text
VERSION:        0.1.3
STABLE_VERSION: 0.0.0
```

A `main` é a branch ativa de desenvolvimento. Uma versão suportada em produção começa somente quando uma release com tag for explicitamente promovida e o `STABLE_VERSION` atualizado.

## Regras

- PATCH: correções compatíveis e manutenção;
- MINOR: novas métricas, descobertas, triggers ou dashboards compatíveis;
- MAJOR: mudanças incompatíveis em chaves públicas, macros, identidade do template ou requisitos de configuração.

Os metadados do template Zabbix utilizam a representação equivalente `X.Y-Z`. A versão do projeto e a versão do formato de export do Zabbix são independentes; uma mesma release pode fornecer exports 7.0 e 8.0.
