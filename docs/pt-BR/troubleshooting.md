# Solução de problemas

[English](../en/troubleshooting.md)

## Sem dados de estatísticas

1. Confirme que o BIND carregou a configuração `statistics-channels`.
2. Teste `/json/v1/status` localmente no host monitorado.
3. Confirme `{$BIND.STATS.HOST}` e `{$BIND.STATS.PORT}`.
4. Confirme o funcionamento dos active checks do Zabbix no host.
5. Confirme que o build do BIND possui suporte às estatísticas JSON.

## Item mestre bruto contém cabeçalhos HTTP

O preprocessing mantém o objeto JSON iniciado no primeiro `{`. Se isso falhar, capture um resultado sanitizado do item mestre afetado e informe as versões do BIND e do agent.

## Um contador está ausente

O conjunto de contadores pode variar por workload, build e versão do BIND. As regras de descoberta se adaptam aos contadores realmente exportados pelo BIND. Não crie contadores artificiais com valor zero para campos que não são exportados.

## Protótipo de zona fica unsupported

Alguns campos de zona dependem do tipo de zona e da versão do BIND. Informe o objeto JSON sanitizado da zona, a versão do BIND, a view e o tipo da zona para melhorar a compatibilidade sem adivinhações.
