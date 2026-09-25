import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "7.0": ROOT / "templates" / "7.0" / "isc-bind9-by-zabbix-agent.yaml",
    "8.0": ROOT / "templates" / "8.0" / "isc-bind9-by-zabbix-agent.yaml",
}
EXPECTED_NAME = "ISC BIND 9 by Zabbix Agent"
FORBIDDEN = ("system.run[", "type: SCRIPT", "type: SSH_AGENT", "type: TELNET")


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
    assert template["vendor"]["version"] == "0.1-0"

    for token in FORBIDDEN:
        assert token not in text, f"forbidden dependency/control path found: {token!r}"

    masters = [
        item
        for item in template.get("items", [])
        if item.get("key", "").startswith("web.page.get[")
    ]
    assert masters, "no web.page.get[] master items found"
    for item in masters:
        assert "type" not in item, (
            f"passive agent master item must omit type: {item.get('key')}"
        )

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
