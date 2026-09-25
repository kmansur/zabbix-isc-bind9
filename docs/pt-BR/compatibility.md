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
| ISC BIND 9.20 | Alvo principal suportado do BIND |
| ISC BIND 9.18.50 | Compatibilidade legado; EOL upstream |

O projeto não afirma suporte a todas as versões históricas do agent. Versões antigas podem funcionar se fornecerem as chaves padrão utilizadas, mas ficam fora da matriz mantida de testes.

O BIND deve possuir suporte às estatísticas JSON. Endpoints e contadores podem variar entre branches/builds; semânticas opcionais não suportadas não serão inventadas.

## Nota de ciclo de vida do BIND

O ISC encerrou a manutenção do BIND 9.18 após a versão 9.18.50 em junho de 2026. O projeto mantém compatibilidade com 9.18.50 para ambientes existentes, enquanto novas validações de produção priorizam a branch ESV 9.20 suportada.
