import sys
from pathlib import Path
from typing import Any

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

RATE_RULES = {
    "bind.nsstats.discovery",
    "bind.qtypes.discovery",
    "bind.rcodes.discovery",
    "bind.sockstats.discovery",
    "bind.resolver.stats.discovery",
    "bind.resolver.qtypes.discovery",
}

STATIC_GAUGES = {
    "bind.nsstats.tcpconn.highwater",
    "bind.nsstats.recurs.highwater",
    "bind.nsstats.recurs.clients",
    "bind.sockstats.udp4.active",
    "bind.sockstats.udp6.active",
    "bind.sockstats.tcp4.active",
    "bind.sockstats.tcp6.active",
    "bind.sockstats.tcp4.clients",
    "bind.sockstats.tcp6.clients",
}

RESOLVER_GAUGES = {
    "bind.resolver.query.current.udp[{#BIND.VIEW}]",
    "bind.resolver.query.current.tcp[{#BIND.VIEW}]",
    "bind.resolver.fetches.current[{#BIND.VIEW}]",
    "bind.resolver.bucket.size[{#BIND.VIEW}]",
}

ADB_GAUGES = {
    "bind.resolver.adb.nentries[{#BIND.VIEW}]",
    "bind.resolver.adb.entries[{#BIND.VIEW}]",
    "bind.resolver.adb.nnames[{#BIND.VIEW}]",
    "bind.resolver.adb.names[{#BIND.VIEW}]",
}

CACHE_RATE_KEYS = {
    "bind.cache.hits[{#BIND.VIEW}]",
    "bind.cache.misses[{#BIND.VIEW}]",
    "bind.cache.queryhits[{#BIND.VIEW}]",
    "bind.cache.querymisses[{#BIND.VIEW}]",
    "bind.cache.deletelru[{#BIND.VIEW}]",
    "bind.cache.deletettl[{#BIND.VIEW}]",
    "bind.cache.coveringnsec[{#BIND.VIEW}]",
}

CACHE_GAUGE_KEYS = {
    "bind.cache.nodes[{#BIND.VIEW}]",
    "bind.cache.nsecnodes[{#BIND.VIEW}]",
    "bind.cache.tree.memory[{#BIND.VIEW}]",
    "bind.cache.heap.memory[{#BIND.VIEW}]",
}


def vendor_version() -> str:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    major, minor, patch = version.split(".")
    return f"{major}.{minor}-{patch}"


def preprocessing_types(item: dict[str, Any]) -> list[str]:
    return [step["type"] for step in item.get("preprocessing", [])]


def first_step(item: dict[str, Any], step_type: str) -> dict[str, Any]:
    return next(
        step for step in item.get("preprocessing", []) if step.get("type") == step_type
    )


def assert_optional_jsonpath_is_safe(item: dict[str, Any]) -> None:
    step = first_step(item, "JSONPATH")
    assert step.get("error_handler") == "CUSTOM_VALUE", (
        f"optional JSONPath must use CUSTOM_VALUE: {item.get('key')}"
    )
    assert str(step.get("error_handler_params")) == "0", (
        f"optional JSONPath fallback must be zero: {item.get('key')}"
    )


def rule_by_key(template: dict[str, Any], key: str) -> dict[str, Any]:
    return next(rule for rule in template.get("discovery_rules", []) if rule["key"] == key)


def item_by_key(template: dict[str, Any], key: str) -> dict[str, Any]:
    return next(item for item in template.get("items", []) if item["key"] == key)


def prototype_keys(rule: dict[str, Any]) -> set[str]:
    return {proto["key"] for proto in rule.get("item_prototypes", [])}


def javascript(rule: dict[str, Any]) -> str:
    chunks = []
    for step in rule.get("preprocessing", []):
        if step.get("type") == "JAVASCRIPT":
            chunks.extend(str(value) for value in step.get("parameters", []))
    return "\n".join(chunks)


def collect_uuids(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "uuid":
                found.append(str(child))
            found.extend(collect_uuids(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(collect_uuids(child))
    return found


def validate_semantics(template: dict[str, Any]) -> None:
    items = template.get("items", [])
    item_map = {item["key"]: item for item in items}

    assert STATIC_GAUGES <= item_map.keys(), "missing static gauge items"
    for key in STATIC_GAUGES:
        assert "CHANGE_PER_SECOND" not in preprocessing_types(item_map[key]), (
            f"gauge must not be converted to a rate: {key}"
        )

    for rule_key in RATE_RULES:
        rule = rule_by_key(template, rule_key)
        for proto in rule.get("item_prototypes", []):
            assert "CHANGE_PER_SECOND" in preprocessing_types(proto), (
                f"counter prototype must be rate-converted: {proto['key']}"
            )
            assert_optional_jsonpath_is_safe(proto)

    ns_script = javascript(rule_by_key(template, "bind.nsstats.discovery"))
    for gauge in ("TCPConnHighWater", "RecursHighwater", "RecursClients"):
        assert gauge in ns_script, f"nsstats gauge is not excluded from rate LLD: {gauge}"

    socket_script = javascript(rule_by_key(template, "bind.sockstats.discovery"))
    for gauge in (
        "UDP4Active",
        "UDP6Active",
        "TCP4Active",
        "TCP6Active",
        "TCP4Clients",
        "TCP6Clients",
    ):
        assert gauge in socket_script, (
            f"socket gauge is not excluded from rate LLD: {gauge}"
        )

    resolver_script = javascript(rule_by_key(template, "bind.resolver.stats.discovery"))
    for gauge in ("QueryCurUDP", "QueryCurTCP", "NumFetch", "BucketSize"):
        assert gauge in resolver_script, (
            f"resolver gauge is not excluded from rate LLD: {gauge}"
        )

    resolver_gauge_rule = rule_by_key(template, "bind.resolver.gauges.discovery")
    assert prototype_keys(resolver_gauge_rule) == RESOLVER_GAUGES
    for proto in resolver_gauge_rule["item_prototypes"]:
        assert "CHANGE_PER_SECOND" not in preprocessing_types(proto)
        assert_optional_jsonpath_is_safe(proto)

    adb_rule = rule_by_key(template, "bind.resolver.adb.discovery")
    assert prototype_keys(adb_rule) == ADB_GAUGES
    for proto in adb_rule["item_prototypes"]:
        assert "CHANGE_PER_SECOND" not in preprocessing_types(proto)
        assert_optional_jsonpath_is_safe(proto)

    cache_rule = rule_by_key(template, "bind.resolver.cache.discovery")
    cache = {proto["key"]: proto for proto in cache_rule.get("item_prototypes", [])}
    assert CACHE_RATE_KEYS | CACHE_GAUGE_KEYS <= cache.keys()
    for key in CACHE_RATE_KEYS:
        assert "CHANGE_PER_SECOND" in preprocessing_types(cache[key]), key
        assert_optional_jsonpath_is_safe(cache[key])
    for key in CACHE_GAUGE_KEYS:
        assert "CHANGE_PER_SECOND" not in preprocessing_types(cache[key]), key
        assert_optional_jsonpath_is_safe(cache[key])

    for key in (
        "bind.xfrins.count",
        "bind.xfrins.deferred",
        "bind.xfrins.bytes",
        "bind.xfrins.rate",
    ):
        step = first_step(item_map[key], "JAVASCRIPT")
        assert step.get("error_handler") == "DISCARD_VALUE", (
            f"unsupported xfrins metric must discard, not report a false zero: {key}"
        )

    secondary = rule_by_key(template, "bind.zones.secondary.discovery")
    for proto in secondary.get("item_prototypes", []):
        step = first_step(proto, "JAVASCRIPT")
        assert step.get("error_handler") == "DISCARD_VALUE", proto["key"]

    dnssec = rule_by_key(template, "bind.zones.dnssec.discovery")
    for proto in dnssec.get("item_prototypes", []):
        step = first_step(proto, "JAVASCRIPT")
        assert step.get("error_handler") == "DISCARD_VALUE", proto["key"]

    zone_keys = {
        "bind.zones.total",
        "bind.zones.primary",
        "bind.zones.secondary",
        "bind.zones.builtin",
        "bind.zones.other",
    }
    assert zone_keys <= item_map.keys(), "zone inventory cannot reconcile all zone types"


def load_template(version: str, path: Path) -> dict[str, Any]:
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
    assert template["vendor"]["version"] == vendor_version()

    for token in FORBIDDEN:
        assert token not in text, f"forbidden dependency/control path found: {token!r}"

    uuids = collect_uuids(export)
    assert len(uuids) == len(set(uuids)), "duplicate UUID found in export"

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

    cache_rule = rule_by_key(template, "bind.resolver.cache.discovery")
    cache_graphs = {graph["name"] for graph in cache_rule.get("graph_prototypes", [])}
    assert cache_graphs == {
        "BIND cache [{#BIND.VIEW}]: Hit and miss rates",
        "BIND cache [{#BIND.VIEW}]: Memory",
        "BIND cache [{#BIND.VIEW}]: Nodes",
    }

    validate_semantics(template)
    return template


def item_keys(template: dict[str, Any]) -> set[str]:
    keys = {item["key"] for item in template.get("items", [])}
    for rule in template.get("discovery_rules", []):
        keys.add(rule["key"])
        keys.update(proto["key"] for proto in rule.get("item_prototypes", []))
    return keys


def macro_names(template: dict[str, Any]) -> set[str]:
    return {macro["macro"] for macro in template.get("macros", [])}


def main() -> int:
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

    print("Template structure, semantics and 7.0/8.0 parity passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
