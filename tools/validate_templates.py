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
    assert template["vendor"]["version"] == "1.0-1"

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
            ("web.page.get[", "net.dns[", "net.dns.perf[")
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
    assert macros["{$BIND.DNS.TEST.SERVER}"] == "127.0.0.1"
    assert macros["{$BIND.DNS.TEST.NAME}"] == "localhost"
    assert macros["{$BIND.DNS.TEST.TYPE}"] == "A"

    dashboards = template.get("dashboards", [])
    assert len(dashboards) == 1, "expected exactly one template dashboard"
    assert dashboards[0]["name"] == "ISC BIND: Overview"
    page_names = [page.get("name", "") for page in dashboards[0].get("pages", [])]
    assert page_names == ["Overview", "DNS activity", "Resolver & resources"]
    assert "itemnavigator" not in text, "dashboard must not contain item navigator widgets"

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

    cache_rule = next(
        rule
        for rule in template.get("discovery_rules", [])
        if rule.get("key") == "bind.resolver.cache.discovery"
    )
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
