# ISC BIND 9 by Zabbix Agent

[English](README.md) | **Português (Brasil)**

Template Zabbix com foco em segurança para monitoramento do **ISC BIND 9** através do canal HTTP nativo de estatísticas do BIND. O projeto é compatível com **Zabbix Agent** e **Zabbix Agent 2** e evita dependências exclusivas do Agent 2 ou scripts externos.

> **Status:** a versão `0.1.3` é uma candidata inicial de engenharia e ainda não é uma release estável para produção.

## Objetivos

- mesmo template para Zabbix Agent e Zabbix Agent 2, usando checks passivos por padrão;
- statistics-channel restrito ao loopback por padrão;
- dependent items e LLD para reduzir coleta repetida;
- nenhuma operação de escrita/controle no BIND;
- documentação em inglês com versão equivalente em português do Brasil;
- Zabbix 7.0 como baseline principal e Zabbix 8.0 como alvo de compatibilidade.

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
| Zabbix Server 8.0 | Compatibilidade |
| Zabbix Agent 6.0+ | Suportado pelo projeto |
| Zabbix Agent 2 6.0+ | Suportado pelo projeto |
| FreeBSD | Agent clássico |
| Linux | Agent clássico ou Agent 2 |
| ISC BIND 9.20 | Alvo principal suportado |
| ISC BIND 9.18.50 | Compatibilidade legado (EOL upstream) |

Agents mais antigos podem funcionar se fornecerem as chaves padrão utilizadas pelo template, mas não fazem parte da matriz mantida de testes.

## Versionamento

```text
VERSION:        0.1.3
STABLE_VERSION: 0.0.0
```

`0.0.0` indica que ainda não há release estável promovida.

## Origem

O projeto foi inicialmente inspirado e parcialmente baseado em **bind9 by HTTP-JSON Agent 2 Active**, do Zabbix Community Templates, de **Gabriele Rossetti (KaleidoscopeIT)**, sob licença MIT.

Consulte [NOTICE.pt-BR.md](NOTICE.pt-BR.md). Licença: **MIT**.

Mantido por **Karim Mansur / Net Tech**.
