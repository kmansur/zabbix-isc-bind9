# ISC BIND by Zabbix agent

[English](README.md) | **Português (Brasil)**

Template Zabbix com foco em segurança para monitoramento do **ISC BIND** através do canal HTTP nativo de estatísticas do BIND. O projeto é compatível com **Zabbix Agent** e **Zabbix Agent 2** e evita dependências exclusivas do Agent 2 ou scripts externos.

> **Release estável:** a versão `1.1.0` é a release estável atual do projeto para produção.

## Objetivos

- mesmo template para Zabbix Agent e Zabbix Agent 2, usando checks passivos por padrão;
- statistics-channel restrito ao loopback por padrão;
- dependent items e LLD para reduzir coleta repetida;
- nenhuma operação de escrita/controle no BIND;
- documentação em inglês com versão equivalente em português do Brasil;
- Zabbix 7.0 como baseline principal e Zabbix 8.0 como alvo de compatibilidade.

A versão 1.1.0 monitora disponibilidade DNS UDP/TCP e tempo de resposta usando as keys nativas `net.dns` e `net.dns.perf`; os alertas funcionais ficam desabilitados por padrão até a escolha de um nome de teste válido para o host.

A versão 1.1.0 também adiciona checks independentes do processo `named` e dos listeners UDP/TCP, normalização escalável do dataset de zonas, serial local de secundárias selecionadas, hit ratio do cache e monitoramento dedicado de clientes recursivos.

## Configuração recomendada

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

## Compatibilidade alvo

| Componente | Alvo |
| --- | --- |
| Zabbix Server 7.0 LTS | Principal |
| Zabbix Server 8.0 | Validado em runtime no 8.0.0beta2; export mantido para a linha 8.0 |
| Zabbix Agent 7.0+ | Alvo suportado e testado |
| Zabbix Agent 2 7.0+ | Alvo suportado e testado |
| FreeBSD | Compatível por arquitetura com Agent clássico; validação runtime recomendada |
| Linux | Agent clássico ou Agent 2 |
| ISC BIND 9.20 | Alvo principal suportado |
| ISC BIND 9.18.50 | Compatibilidade legado (EOL upstream) |

Agents mais antigos ficam fora da matriz mantida de testes. O template atual requer as keys padrão `web.page.get[]`, `net.dns[]` e `net.dns.perf[]`; o baseline mantido é 7.0+.

A versão 1.1.0 inclui nove gráficos clássicos reutilizáveis e uma dashboard nativa de três páginas. Consulte [docs/pt-BR/dashboard.md](docs/pt-BR/dashboard.md).

## Versionamento

```text
VERSION:        1.1.0
STABLE_VERSION: 1.1.0
```

`STABLE_VERSION` identifica a linha suportada para produção. A versão `1.1.0` é o baseline estável atual.

## Origem

O projeto foi inicialmente inspirado e parcialmente baseado em **bind9 by HTTP-JSON Agent 2 Active**, do Zabbix Community Templates, de **Gabriele Rossetti (KaleidoscopeIT)**, sob licença MIT.

Consulte [NOTICE.pt-BR.md](NOTICE.pt-BR.md). Licença: **MIT**.

Mantido por **Karim Mansur / Net Tech**.
