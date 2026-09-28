# Versionamento

[English](../en/versioning.md)

O projeto utiliza Versionamento Semântico.

```text
VERSION:        1.0.1
STABLE_VERSION: 1.0.1
```

A `main` contém o código mantido atual. `STABLE_VERSION` registra o baseline suportado para produção. A versão `1.0.1` é o baseline estável atual do projeto.

## Regras

- PATCH: correções compatíveis e manutenção;
- MINOR: novas métricas, descobertas, triggers ou dashboards compatíveis;
- MAJOR: mudanças incompatíveis em chaves públicas, macros, identidade do template ou requisitos de configuração.

Os metadados do template Zabbix utilizam a representação equivalente `X.Y-Z`. A versão do projeto e a versão do formato de export do Zabbix são independentes; uma mesma release pode fornecer exports 7.0 e 8.0.
