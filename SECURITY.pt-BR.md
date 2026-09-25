# Política de segurança

[English](SECURITY.md) | **Português (Brasil)**

## Modelo de segurança

O template foi projetado para monitoramento somente leitura usando o statistics-channel nativo do BIND e recursos padrão do Zabbix agent.

O listener recomendado fica restrito ao loopback:

```conf
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

Não exponha o listener de estatísticas a redes não confiáveis. Se um endereço diferente de loopback for operacionalmente necessário, restrinja o acesso pela ACL do BIND e pelos firewalls do host/rede.

O template mantido não requer execução privilegiada no sistema operacional nem permissões de controle/escrita no BIND.

## Relato de vulnerabilidades

Não inclua credenciais, segredos TSIG, hostnames que identifiquem clientes ou configurações de produção não sanitizadas em relatos públicos.

Uma issue pública sanitizada pode ser utilizada quando o problema puder ser reproduzido sem informações sensíveis. Descreva claramente o impacto de segurança.

## Versões suportadas

A versão `0.1.0` é uma candidata de engenharia. Ainda não existe release promovida como estável para produção; `STABLE_VERSION` permanece `0.0.0`.
