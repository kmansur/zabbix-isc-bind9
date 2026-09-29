import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "7.0": ROOT / "templates" / "7.0" / "isc-bind9-by-zabbix-agent.yaml",
    "8.0": ROOT / "templates" / "8.0" / "isc-bind9-by-zabbix-agent.yaml",
}
EXPECTED_NAME = "ISC BIND by Zabbix agent"
FORBIDDEN = (
    "system.run[",
    "type: SCRIPT",
    "type: SSH_AGENT",
    "type: TELNET",
    "ZABBIX_ACTIVE",
    "{$BIND9_STAT_PORT}",
    "{$BIND9.",
    "{#BIND9_CATEGORY}",
    "8653",
)


def load_template(version, path):
    if not path.is_file():
        raise AssertionError(f"missing template: {path}")

    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    export = data["zabbix_export"]

    assert export["version"] == version
    template = export["templates"][0]
    assert template["template"] == EXPECTED_NAME
    assert template["name"] == EXPECTED_NAME
    assert template["vendor"]["name"] == "Net Tech"
    assert template["vendor"]["version"] == "1.1-0"

    for token in FORBIDDEN:
        assert token not in text, f"forbidden dependency/control path found: {token!r}"

    idle_safe_discovery_tokens = (
        "var counters = d.nsstats || {};",
        "var counters = d.qtypes || {};",
        "var counters = d.rcodes || {};",
        "var views = d.views || {};",
        "var resolver = views[viewName].resolver || {};",
        "var stats = resolver.stats || {};",
        "var qtypes = resolver.qtypes || {};",
        "var adb = resolver.adb || {};",
    )
    for token in idle_safe_discovery_tokens:
        assert token in text, f"idle-safe discovery guard missing: {token!r}"

    items = template.get("items", [])
    passive_items = [
        item
        for item in items
        if item.get("key", "").startswith(
            (
                "web.page.get[",
                "net.dns[",
                "net.dns.perf[",
                "proc.num[",
                "net.tcp.listen[",
                "net.udp.listen[",
            )
        )
    ]
    assert passive_items, "no passive agent items found"

    for item in items:
        item_type = item.get("type")
        if item in passive_items:
            assert item_type is None, (
                f"passive agent item must omit type: {item.get('key')}"
            )
        else:
            assert item_type == "DEPENDENT", (
                f"unexpected non-dependent item type for {item.get('key')}: {item_type}"
            )

    for rule in template.get("discovery_rules", []):
        assert rule.get("type") == "DEPENDENT", (
            f"discovery rule must be dependent: {rule.get('key')}"
        )
        for proto in rule.get("item_prototypes", []):
            assert proto.get("type") == "DEPENDENT", (
                f"item prototype must be dependent: {proto.get('key')}"
            )

    macros = {m["macro"]: m.get("value") for m in template.get("macros", [])}
    assert macros["{$BIND.STATS.HOST}"] == "127.0.0.1"
    assert macros["{$BIND.STATS.PORT}"] == "8053"
    assert macros["{$BIND.ZONE.SECONDARY.MATCHES}"] == "^$"
    assert macros["{$BIND.ZONE.DNSSEC.MATCHES}"] == "^$"
    assert macros["{$BIND.DNS.TEST.ENABLED}"] == "0"
    assert macros["{$BIND.DNS.TEST.INTERVAL}"] == "30s"
    assert macros["{$BIND.DNS.PORT}"] == "53"
    assert macros["{$BIND.PROCESS.NAME}"] == "named"
    assert macros["{$BIND.DNS.TEST.SERVER}"] == "127.0.0.1"
    assert macros["{$BIND.DNS.TEST.NAME}"] == "localhost"
    assert macros["{$BIND.DNS.TEST.TYPE}"] == "A"
    assert macros["{$BIND.DNS.RESPONSE.UDP.WARN}"] == "0.1"
    assert macros["{$BIND.DNS.RESPONSE.TCP.WARN}"] == "0.1"
    assert macros["{$BIND.VIEW.MATCHES}"] == ".*"
    assert macros["{$BIND.VIEW.NOT_MATCHES}"] == "^_bind$"
    assert macros["{$BIND.RECURSCLIENTS.WARN}"] == "0"
    assert macros["{$BIND.CACHE.DELETELRU.WARN}"] == "0"
    assert "{$BIND.DNS.RESPONSE.WARN}" not in macros

    # Raw HTTP payloads are preprocessing masters only and must not consume history.
    raw_items = [item for item in items if item.get("name", "").endswith(" raw")]
    assert raw_items, "no raw master items found"
    assert all(str(item.get("history")) == "0" for item in raw_items), (
        "raw master items must use history: 0"
    )

    keys = {item.get("key") for item in items}
    assert "bind.stats.heartbeat" in keys
    heartbeat = next(item for item in items if item.get("key") == "bind.stats.heartbeat")
    assert str(heartbeat.get("history")) != "0", (
        "statistics heartbeat must retain history for nodata() evaluation"
    )
    heartbeat_triggers = heartbeat.get("triggers", [])
    assert heartbeat_triggers, "statistics heartbeat trigger missing"
    assert any(
        "nodata(/ISC BIND by Zabbix agent/bind.stats.heartbeat" in trigger.get("expression", "")
        for trigger in heartbeat_triggers
    ), "statistics nodata trigger must use the stored heartbeat item"

    keys = {item.get("key") for item in items}
    assert "bind.zones.normalized" in keys
    assert "bind.nsstats.recursclients" in keys
    assert "proc.num[{$BIND.PROCESS.NAME}]" in keys
    assert "net.tcp.listen[{$BIND.DNS.PORT}]" in keys
    assert "net.udp.listen[{$BIND.DNS.PORT}]" in keys

    dns_items = [
        item
        for item in items
        if item.get("key", "").startswith(("net.dns[", "net.dns.perf["))
    ]
    assert len(dns_items) == 4
    assert all(item.get("delay") == "{$BIND.DNS.TEST.INTERVAL}" for item in dns_items)

    zone_rule = discovery_rule(template, "bind.zones.secondary.discovery")
    expires = prototype(zone_rule, "bind.zone.expires.in[{#BIND.VIEW},{#BIND.ZONE}]")
    refresh = prototype(zone_rule, "bind.zone.refresh.in[{#BIND.VIEW},{#BIND.ZONE}]")
    serial = prototype(zone_rule, "bind.zone.serial[{#BIND.VIEW},{#BIND.ZONE}]")
    assert expires.get("value_type") == "FLOAT"
    assert refresh.get("value_type") == "FLOAT"
    assert expires["master_item"]["key"] == "bind.zones.normalized"
    assert refresh["master_item"]["key"] == "bind.zones.normalized"
    assert serial["master_item"]["key"] == "bind.zones.normalized"
    assert "expires_in" in preprocessing_script(
        next(item for item in items if item.get("key") == "bind.zones.normalized")
    )

    # Every LLD rule gets an explicit retention policy.
    assert all(
        rule.get("lifetime") == "7d" for rule in template.get("discovery_rules", [])
    )

    view_filtered_rules = {
        "bind.zones.secondary.discovery",
        "bind.zones.dnssec.discovery",
        "bind.resolver.stats.discovery",
        "bind.resolver.gauge.discovery",
        "bind.resolver.qtypes.discovery",
        "bind.resolver.adb.discovery",
        "bind.resolver.cache.discovery",
    }
    for rule in template.get("discovery_rules", []):
        if rule.get("key") in view_filtered_rules:
            filter_text = str(rule.get("filter", {}))
            assert "{$BIND.VIEW.MATCHES}" in filter_text
            assert "{$BIND.VIEW.NOT_MATCHES}" in filter_text

        for proto in rule.get("item_prototypes", []):
            assert proto.get("tags"), (
                f"item prototype is missing tags: {proto.get('key')}"
            )
            for step in proto.get("preprocessing", []):
                if step.get("type") == "JSONPATH":
                    assert step.get("error_handler") == "DISCARD_VALUE", (
                        f"dynamic JSONPath must discard absent values: {proto.get('key')}"
                    )

    dns_trigger_text = "\n".join(
        str(trigger)
        for item in items
        for trigger in item.get("triggers", [])
        if "DNS" in trigger.get("name", "")
    )
    assert "{$BIND.DNS.TEST.ENABLED}=1" in dns_trigger_text
    assert "DNS functional test failed over UDP" in dns_trigger_text
    assert "DNS functional test failed over TCP" in dns_trigger_text

    dashboards = template.get("dashboards", [])
    assert len(dashboards) == 1, "expected exactly one template dashboard"
    assert dashboards[0]["name"] == "ISC BIND: Overview"
    page_names = [page.get("name", "") for page in dashboards[0].get("pages", [])]
    assert page_names == ["Overview", "DNS activity", "Resolver & resources"]
    assert "itemnavigator" not in text, (
        "dashboard must not contain item navigator widgets"
    )
    assert "JSON stats version" in text

    graph_names = {graph["name"] for graph in export.get("graphs", [])}
    expected_graphs = {
        "BIND: Query rates",
        "BIND: Query errors",
        "BIND: DNS transport traffic",
        "BIND: Memory usage",
        "BIND: Zone inventory",
        "BIND: Incoming transfers",
        "BIND: Incoming transfer rate",
        "BIND: Server timing",
        "BIND: DNS query response time",
    }
    assert graph_names == expected_graphs, "unexpected graph set"

    # Counters and gauges must not share rate preprocessing.
    ns_rate = discovery_rule(template, "bind.nsstats.discovery")
    ns_gauge = discovery_rule(template, "bind.nsstats.gauge.discovery")
    assert "CHANGE_PER_SECOND" in preprocessing_types(
        prototype(ns_rate, "bind.nsstats[{#BIND.COUNTER}]")
    )
    assert "CHANGE_PER_SECOND" not in preprocessing_types(
        prototype(ns_gauge, "bind.nsstats.gauge[{#BIND.COUNTER}]")
    )
    for name in ("RecursClients", "TCPConnHighWater", "RecursHighwater"):
        assert name in preprocessing_script(ns_rate)
    assert "RecursClients" not in preprocessing_script(ns_gauge), (
        "RecursClients is a dedicated item and must not be duplicated by gauge LLD"
    )
    for name in ("TCPConnHighWater", "RecursHighwater"):
        assert name in preprocessing_script(ns_gauge)

    socket_rate = discovery_rule(template, "bind.sockstats.discovery")
    socket_gauge = discovery_rule(template, "bind.sockstats.gauge.discovery")
    assert "CHANGE_PER_SECOND" in preprocessing_types(
        prototype(socket_rate, "bind.sockstats[{#BIND.COUNTER}]")
    )
    assert "CHANGE_PER_SECOND" not in preprocessing_types(
        prototype(socket_gauge, "bind.sockstats.gauge[{#BIND.COUNTER}]")
    )
    for name in (
        "UDP4Active",
        "UDP6Active",
        "TCP4Active",
        "TCP6Active",
        "TCP4Clients",
        "TCP6Clients",
    ):
        assert name in preprocessing_script(socket_rate)
        assert name in preprocessing_script(socket_gauge)

    resolver_rate = discovery_rule(template, "bind.resolver.stats.discovery")
    resolver_gauge = discovery_rule(template, "bind.resolver.gauge.discovery")
    assert "CHANGE_PER_SECOND" in preprocessing_types(
        prototype(
            resolver_rate,
            "bind.resolver.stats[{#BIND.VIEW},{#BIND.COUNTER}]",
        )
    )
    assert "CHANGE_PER_SECOND" not in preprocessing_types(
        prototype(
            resolver_gauge,
            "bind.resolver.gauge[{#BIND.VIEW},{#BIND.COUNTER}]",
        )
    )
    for name in ("QueryCurUDP", "QueryCurTCP", "NumFetch", "BucketSize"):
        assert name in preprocessing_script(resolver_rate)
        assert name in preprocessing_script(resolver_gauge)

    adb_rule = discovery_rule(template, "bind.resolver.adb.discovery")
    adb_item = prototype(adb_rule, "bind.resolver.adb[{#BIND.VIEW},{#BIND.COUNTER}]")
    assert "CHANGE_PER_SECOND" not in preprocessing_types(adb_item)

    cache_rule = next(
        rule
        for rule in template.get("discovery_rules", [])
        if rule.get("key") == "bind.resolver.cache.discovery"
    )
    cache_ratio = prototype(cache_rule, "bind.cache.hitratio[{#BIND.VIEW}]")
    assert cache_ratio.get("value_type") == "FLOAT"
    assert cache_ratio.get("units") == "%"

    delete_lru = prototype(cache_rule, "bind.cache.deletelru[{#BIND.VIEW}]")
    assert delete_lru.get("trigger_prototypes"), "DeleteLRU warning prototype missing"

    cache_graphs = {graph["name"] for graph in cache_rule.get("graph_prototypes", [])}
    assert cache_graphs == {
        "BIND cache [{#BIND.VIEW}]: Hit and miss rates",
        "BIND cache [{#BIND.VIEW}]: Memory",
        "BIND cache [{#BIND.VIEW}]: Nodes",
    }

    return template


def item_keys(template):
    keys = {item["key"] for item in template.get("items", [])}
    for rule in template.get("discovery_rules", []):
        keys.add(rule["key"])
        keys.update(proto["key"] for proto in rule.get("item_prototypes", []))
    return keys


def macro_names(template):
    return {macro["macro"] for macro in template.get("macros", [])}


def discovery_rule(template, key):
    return next(
        rule for rule in template.get("discovery_rules", []) if rule.get("key") == key
    )


def prototype(rule, key):
    return next(
        item for item in rule.get("item_prototypes", []) if item.get("key") == key
    )


def preprocessing_types(item):
    return {step.get("type") for step in item.get("preprocessing", [])}


def preprocessing_script(rule):
    for step in rule.get("preprocessing", []):
        if step.get("type") == "JAVASCRIPT":
            params = step.get("parameters", [])
            return params[0] if params else ""
    return ""


def main():
    loaded = {
        version: load_template(version, path) for version, path in TARGETS.items()
    }

    assert item_keys(loaded["7.0"]) == item_keys(loaded["8.0"]), (
        "7.0/8.0 item-key drift"
    )
    assert macro_names(loaded["7.0"]) == macro_names(loaded["8.0"]), (
        "7.0/8.0 macro drift"
    )
    assert loaded["7.0"] == loaded["8.0"], "7.0/8.0 template-body drift"

    export_7 = yaml.safe_load(TARGETS["7.0"].read_text(encoding="utf-8"))[
        "zabbix_export"
    ]
    export_8 = yaml.safe_load(TARGETS["8.0"].read_text(encoding="utf-8"))[
        "zabbix_export"
    ]
    assert export_7.get("graphs", []) == export_8.get("graphs", []), (
        "7.0/8.0 graph-definition drift"
    )

    print("Template validation passed for Zabbix 7.0 and 8.0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
