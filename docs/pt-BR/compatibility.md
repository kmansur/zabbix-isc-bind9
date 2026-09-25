# Compatibilidade

[English](../en/compatibility.md)

| Componente | Status |
| --- | --- |
| Zabbix 7.0 | Alvo principal |
| Zabbix 8.0 | Export de compatibilidade; requer validação real |
| Zabbix Agent clássico 6.0+ | Alvo mantido pelo projeto |
| Zabbix Agent 2 6.0+ | Alvo mantido pelo projeto |
| FreeBSD | Caminho com Agent clássico |
| Linux | Agent clássico ou Agent 2 |
| ISC BIND 9.18 | Alvo principal de validação do BIND |

O projeto não afirma suporte a todas as versões históricas do agent. Versões antigas podem funcionar se fornecerem as chaves padrão utilizadas, mas ficam fora da matriz mantida de testes.

O BIND deve possuir suporte às estatísticas JSON. Endpoints e contadores podem variar entre branches/builds; semânticas opcionais não suportadas não serão inventadas.
