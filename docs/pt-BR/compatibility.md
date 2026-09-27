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
| ISC BIND 9.18.39 no Ubuntu 24.04 | Validação real dos endpoints concluída |

O projeto não afirma suporte a todas as versões históricas do agent. Versões antigas podem funcionar se fornecerem as chaves padrão utilizadas, mas ficam fora da matriz mantida de testes.

O BIND deve possuir suporte às estatísticas JSON. Endpoints e contadores podem variar entre branches/builds; semânticas opcionais não suportadas não serão inventadas.

## Nota de ciclo de vida do BIND

O ISC encerrou a manutenção do BIND 9.18 após a versão 9.18.50 em junho de 2026. O projeto mantém compatibilidade com 9.18 para ambientes existentes, enquanto novas validações de produção priorizam a branch ESV 9.20 suportada.

## Nota de validação real

Os endpoints JSON `status`, `server`, `zones`, `mem`, `net` e `traffic` foram validados no Ubuntu 24.04 com BIND 9.18.39. O servidor testado expôs os blocos do resolver `stats`, `qtypes`, `cache`, `cachestats` e `adb`, e exportou `sockstats` através de `/json/v1/net`.


## Validação de desenvolvimento no Zabbix 8.0

O export 8.0 é importado continuamente no CI contra as imagens Docker oficiais trunk do Zabbix, que correspondem à linha de desenvolvimento do Zabbix 8.0. Isso valida compatibilidade de schema/import antes da existência de uma versão 8.0 estável. O comportamento em runtime continua sendo considerado pré-release até a validação contra uma build oficial estável do 8.0.


## Fixtures de contrato JSON do BIND

O repositório inclui fixtures JSON representativas do BIND 9.18 e 9.20. O pytest valida os contratos estruturais usados pelo preprocessing e pelas descobertas, incluindo blocos de resolver/cache, estatísticas de sockets, campos de memória, histogramas de tráfego, timers de zonas secundárias e o endpoint de transferências recebidas do 9.20. Essas fixtures complementam, mas não substituem, a validação em runtime contra servidores BIND reais.
