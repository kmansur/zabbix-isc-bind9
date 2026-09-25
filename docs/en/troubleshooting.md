# Troubleshooting

[Português (Brasil)](../pt-BR/troubleshooting.md)

## No statistics data

1. Confirm that BIND loaded the `statistics-channels` configuration.
2. Test `/json/v1/status` locally on the monitored host.
3. Confirm `{$BIND.STATS.HOST}` and `{$BIND.STATS.PORT}`.
4. Confirm Zabbix active checks are working for the host.
5. Confirm the BIND build provides JSON statistics support.

## Raw master item contains HTTP headers

The template preprocessing keeps the JSON object beginning at the first `{`. If this fails, capture a sanitized result from the affected master item and report the BIND and agent versions.

## A counter is missing

Counter sets can vary by workload, build and BIND version. Discovery rules adapt to the counters actually exported by BIND. Do not create synthetic zero-valued counters for fields that are not exported.

## Zone prototype becomes unsupported

Some zone fields depend on zone type and BIND version. Report the sanitized zone JSON object together with BIND version, view and zone type so the compatibility logic can be improved without guessing.
