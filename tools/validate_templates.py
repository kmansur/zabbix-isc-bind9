import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "7.0": ROOT / "templates" / "7.0" / "isc-bind9-by-zabbix-agent.yaml",
    "8.0": ROOT / "templates" / "8.0" / "isc-bind9-by-zabbix-agent.yaml",
}
EXPECTED_NAME = "ISC BIND 9 by Zabbix Agent"
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
    assert template["vendor"]["version"] == "0.1-3"

    for token in FORBIDDEN:
        assert token not in text, f"forbidden dependency/control path found: {token!r}"

    items = template.get("items", [])
    masters = [
        item for item in items if item.get("key", "").startswith("web.page.get[")
    ]
    assert masters, "no web.page.get[] master items found"

    for item in items:
        item_type = item.get("type")
        if item in masters:
            assert item_type is None, (
                f"passive agent master item must omit type: {item.get('key')}"
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

    print("Template validation passed for Zabbix 7.0 and 8.0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
