# Compatibilidade

[English](../en/compatibility.md)

| Componente | Status |
| --- | --- |
| Zabbix 7.0 | Alvo principal |
| Zabbix 8.0 | Validado em runtime no Zabbix 8.0.0beta2; fresh-import validado continuamente contra imagens oficiais trunk |
| Zabbix Agent clássico 6.0+ | Alvo mantido pelo projeto |
| Zabbix Agent 2 6.0+ | Alvo mantido pelo projeto |
| FreeBSD | Caminho de projeto com Agent clássico; disponibilidade do pacote verificada, com validação runtime recomendada |
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


## Validação no Zabbix 8.0

O export 8.0 é importado continuamente no CI contra as imagens Docker oficiais trunk do Zabbix.

Além disso, o template na versão `1.0-0` foi importado com sucesso em um servidor real **Zabbix 8.0.0beta2** e vinculado ao host BIND monitorado. A coleta em runtime foi confirmada, incluindo disponibilidade DNS UDP/TCP e tempo de resposta, taxas de requests IPv4/IPv6, SERVFAIL/queries descartadas, métricas de transferências, memória, contadores de zonas, endpoints brutos de estatísticas e dados descobertos.

No Zabbix 8.0.0beta2 validado, o template apresentou 35 itens base, 8 triggers, 9 gráficos clássicos, 1 dashboard e 10 regras de descoberta, com os dados descobertos sendo coletados normalmente.

Isso fornece validação real em runtime para a linha de desenvolvimento do Zabbix 8.0. Uma build estável final do Zabbix 8.0 ainda deverá ser revalidada quando estiver disponível, pois podem existir mudanças de schema ou frontend entre beta e stable.


## Fixtures de contrato JSON do BIND

O repositório inclui fixtures JSON representativas do BIND 9.18 e 9.20. O pytest valida os contratos estruturais usados pelo preprocessing e pelas descobertas, incluindo blocos de resolver/cache, estatísticas de sockets, campos de memória, histogramas de tráfego, timers de zonas secundárias e o endpoint de transferências recebidas do 9.20. Essas fixtures complementam, mas não substituem, a validação em runtime contra servidores BIND reais.


## Validação em containers BIND reais

O CI inicia as imagens Docker oficiais do ISC para BIND 9.18 e 9.20 com uma configuração mínima do statistics-channel e valida os endpoints JSON reais usados pelo template. No 9.18 o job confirma que `/json/v1/xfrins` não existe; no 9.20 ele exige a presença desse endpoint. Isso protege o desenho version-aware das transferências contra mudanças upstream.


## Validação real dos checks nativos de saúde DNS

A validação em runtime no Ubuntu 24.04 com BIND 9.18.39 e Zabbix agent clássico confirmou todos os checks nativos de serviço usados pela versão 1.0.0 do template:

- disponibilidade DNS UDP: `1`
- disponibilidade DNS TCP: `1`
- tempo de resposta UDP: aproximadamente `0.000480 s` (0,48 ms)
- tempo de resposta TCP: aproximadamente `0.000616 s` (0,62 ms)

Os checks utilizaram `127.0.0.1`, nome `localhost`, tipo `A`, timeout de um segundo e duas tentativas. Isso confirma que `net.dns[]` e `net.dns.perf[]` funcionam conforme projetado com o Zabbix agent clássico passivo no ambiente real de teste com BIND 9.18.39.


## Nota sobre FreeBSD

O template utiliza deliberadamente apenas keys padrão do Agent clássico e não possui scripts auxiliares exclusivos de Linux nem comandos privilegiados. A coleção de Ports do FreeBSD disponibiliza o Zabbix 7 Agent clássico (`net-mgmt/zabbix7-agent`), que atende ao caminho de implantação projetado. A validação real em runtime do projeto foi realizada em Linux; por isso, no escopo da versão 1.0, o FreeBSD é considerado compatível por arquitetura, e não uma plataforma certificada separadamente em runtime.
