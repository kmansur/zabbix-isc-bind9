# Contribuindo

[English](CONTRIBUTING.md) | **Português (Brasil)**

Contribuições, relatos de compatibilidade, melhorias de documentação e resultados de validação são bem-vindos.

## Fluxo de desenvolvimento

1. Crie uma branch focada a partir da `main`.
2. Mantenha o monitoramento somente leitura e com o menor privilégio possível.
3. Atualize em conjunto a documentação em inglês e português do Brasil.
4. Preserve chaves de itens e UUIDs em alterações compatíveis.
5. Execute a suíte local de validação.
6. Abra um pull request.

Prefixos recomendados: `feature/`, `fix/`, `docs/`, `refactor/`, `test/`, `ci/` e `chore/`.

Conventional Commits são recomendados.

## Regras do modelo de monitoramento

As alterações não devem adicionar comandos privilegiados no sistema operacional, operações de controle/escrita no BIND ou exposição de rede desnecessária. Prefira estatísticas nativas do BIND, chaves padrão do Zabbix agent, dependent items e preprocessing.

## Relatos de compatibilidade

Informe:

- versão exata do ISC BIND;
- sistema operacional e versão;
- versão do Zabbix Server;
- versão do Zabbix Agent ou Agent 2;
- versão JSON das estatísticas do BIND;
- endpoint e chave de item afetados;
- amostra sanitizada quando necessária.

Não publique credenciais, material TSIG, endereços públicos de gerenciamento ou hostnames que identifiquem clientes.
