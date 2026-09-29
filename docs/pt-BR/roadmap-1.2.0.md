# Roadmap da versão 1.2.0

[English](../en/roadmap-1.2.0.md)

Status: **planejado / sujeito a validação**

A versão 1.2.0 deve permanecer compatível com as versões anteriores. Este roadmap registra melhorias candidatas de monitoramento; nenhum item é compromisso de implementação até que sua semântica no BIND, comportamento no Zabbix, impacto de segurança e valor operacional sejam validados.

## Prioridades planejadas

### 1. Razão de SERVFAIL

Avaliar uma porcentagem dedicada de SERVFAIL além da taxa absoluta já existente.

Requisitos:

- manter o item e o trigger absolutos em qps;
- validar o denominador correto nas estatísticas suportadas do BIND 9.18 e 9.20;
- evitar divisão por zero e artefatos de inicialização;
- expor threshold percentual configurável somente após validação em runtime;
- manter a métrica compreensível em servidores autoritativos e recursivos.

### 2. Razão de queries descartadas

Avaliar uma porcentagem de queries descartadas além da taxa absoluta de `QryDropped`.

Requisitos:

- manter a métrica absoluta em qps;
- validar denominador e semântica dos counters nas versões suportadas do BIND;
- evitar falsos positivos em servidores de baixo tráfego;
- utilizar threshold configurável com padrão conservador.

### 3. Sinal dedicado de falha de validação DNSSEC

Promover falhas de validação DNSSEC, como `ValFail`, para uma métrica operacional dedicada quando expostas pelas estatísticas do resolver.

Requisitos:

- confirmar counter e endpoint nas versões suportadas do BIND;
- evitar coleta duplicada no discovery genérico de `nsstats` se o counter passar a ser dedicado;
- adicionar taxa dedicada e trigger opcional apenas quando o servidor expuser a métrica;
- preservar ambientes exclusivamente autoritativos sem gerar itens unsupported.

### 4. Checks E2E mais fortes no CI

Ampliar a cobertura de regressão sobre as keys realmente exportadas pelo template.

Checks candidatos:

- derivar ou validar as formas literais com aspas de `web.page.get[]` utilizadas pelos master items;
- validar a política restritiva de `AllowKey`/`DenyKey` com Agent clássico e Agent 2;
- adicionar smoke test de itens unsupported quando for possível torná-lo determinístico;
- preservar fresh-import no Zabbix 7.0/8.0 e contratos live BIND 9.18/9.20.

## Explicitamente fora do escopo do template base 1.2.0

As ideias abaixo podem ser úteis em alguns ambientes, mas não estão planejadas atualmente para o template base:

- baseline comportamental de QPS com `trendavg()`, `baselinedev()` ou funções semelhantes;
- comparação automática de serial primário versus secundário entre hosts Zabbix distintos;
- monitoramento de serviços DoT/DoH;
- orquestração de topologia ou replicação entre hosts.

Elas podem futuramente ser documentadas como receitas avançadas ou componentes separados caso apareça uma necessidade operacional concreta.

## Critérios de aceitação

Antes de promover a 1.2.0 para estável:

- nenhuma quebra de keys públicas existentes, identidade do template ou macros atuais sem plano explícito de migração;
- importação bem-sucedida nos alvos mantidos Zabbix 7.0 e 8.0;
- validação bem-sucedida com Agent clássico e Agent 2;
- cobertura de contrato BIND 9.18 e 9.20 para as novas métricas;
- nenhuma regressão de cardinalidade padrão ou postura de segurança;
- documentação em inglês e português do Brasil atualizada em conjunto;
- changelog, metadados de versão e assets de release sincronizados;
- validação manual em runtime quando viável.
