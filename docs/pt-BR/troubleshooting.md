# Solução de problemas

[English](../en/troubleshooting.md)

## Sem dados de estatísticas

1. Confirme que o BIND carregou a configuração `statistics-channels`.
2. Teste `/json/v1/status` localmente no host monitorado.
3. Confirme `{$BIND.STATS.HOST}` e `{$BIND.STATS.PORT}`.
4. Confirme que a interface passiva do Zabbix Agent está acessível ao Zabbix Server/Proxy e que um item padrão do agent pode ser consultado.
5. Confirme que o build do BIND possui suporte às estatísticas JSON.

## Ubuntu 24.04: named funciona, mas o systemd permanece em activating

O BIND pode responder DNS, RNDC e estatísticas enquanto o `systemd` ainda mostra:

```text
ActiveState=activating
SubState=start
```

Quando a unit utiliza `Type=notify`, verifique o log do kernel por bloqueios do AppArmor envolvendo:

```text
/run/systemd/notify
/proc/version_signature
```

Um caso típico é o profile do AppArmor impedir o BIND de enviar o `READY=1` ao systemd. Nesse cenário, o `systemd` espera até `TimeoutStartSec` expirar e reinicia um `named` que estava funcional quando `Restart=on-failure` está habilitado.

Prefira um override local do AppArmor em vez de editar diretamente o profile fornecido pelo pacote:

```text
/etc/apparmor.d/local/usr.sbin.named
```

Regras validadas em Ubuntu 24.04:

```text
/run/systemd/notify w,
/proc/version_signature r,
```

Depois da alteração, valide e recarregue o AppArmor, reinicie o BIND e confirme:

```text
ActiveState=active
SubState=running
```

Não conceda capabilities amplas como `sys_admin` apenas para eliminar uma mensagem de auditoria do AppArmor. Adicione permissões somente quando uma função necessária do BIND estiver comprovadamente sendo bloqueada.

## Item mestre bruto contém cabeçalhos HTTP

O preprocessing mantém o objeto JSON iniciado no primeiro `{`. Se isso falhar, capture um resultado sanitizado do item mestre afetado e informe as versões do BIND e do agent.

## Um contador está ausente

O conjunto de contadores pode variar por workload, build e versão do BIND. As regras de descoberta dinâmica se adaptam aos contadores realmente exportados. Alguns contadores fixos cuja ausência representa valor zero são normalizados para zero pelo preprocessing; famílias descobertas dinamicamente não são sintetizadas quando estão ausentes.

## Protótipo de zona fica unsupported

Alguns campos de zona dependem do tipo de zona e da versão do BIND. Informe o objeto JSON sanitizado da zona, a versão do BIND, a view e o tipo da zona para melhorar a compatibilidade sem adivinhações.
