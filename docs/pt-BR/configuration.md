# Configuração

[English](../en/configuration.md)

## Macros do template

| Macro | Padrão | Finalidade |
| --- | --- | --- |
| `{$BIND.STATS.HOST}` | `127.0.0.1` | Host local das estatísticas |
| `{$BIND.STATS.PORT}` | `8053` | Porta TCP das estatísticas |
| `{$BIND.STATS.NODATA}` | `10m` | Limite sem dados |
| `{$BIND.QRYDROPPED.RATE.WARN}` | `0` | Limite de queries descartadas |
| `{$BIND.SERVFAIL.RATE.WARN}` | `5` | Limite de SERVFAIL |
| `{$BIND.ZONE.EXPIRES.WARN}` | `1h` | Janela de aviso antes da expiração de uma zona secundária |

Mantenha o listener no loopback sempre que possível. Se outro endereço local for necessário, restrinja o acesso pela ACL do BIND e pelos firewalls do host/rede.
