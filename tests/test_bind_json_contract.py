"""Contract tests for the BIND JSON structures used by the template."""

from __future__ import annotations

import json
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_bind_918_contract() -> None:
    data = load("bind-9.18.json")

    assert data["bind_version"].startswith("9.18.")
    assert data["status"]["json-stats-version"]
    assert data["status"]["version"].startswith("9.18.")

    server = data["server"]
    assert {"nsstats", "qtypes", "rcodes", "views"} <= server.keys()

    nsstats = server["nsstats"]
    assert {
        "Requestv4",
        "Requestv6",
        "QryDropped",
        "QrySERVFAIL",
        "QryRecursion",
    } <= nsstats.keys()

    resolver = server["views"]["_default"]["resolver"]
    assert {"stats", "qtypes", "cache", "cachestats", "adb"} <= resolver.keys()

    cache = resolver["cachestats"]
    common_cache_fields = {
        "CacheHits",
        "CacheMisses",
        "QueryHits",
        "QueryMisses",
        "DeleteLRU",
        "DeleteTTL",
        "CoveringNSEC",
        "CacheNodes",
        "CacheNSECNodes",
        "CacheBuckets",
        "TreeMemInUse",
        "HeapMemInUse",
    }
    assert common_cache_fields <= cache.keys()

    assert data["net"]["sockstats"]
    assert {"InUse", "Malloced", "contexts"} <= data["mem"]["memory"].keys()

    traffic = data["traffic"]["traffic"]
    expected_traffic = {
        "dns-udp-requests-sizes-received-ipv4",
        "dns-udp-requests-sizes-received-ipv6",
        "dns-tcp-requests-sizes-received-ipv4",
        "dns-tcp-requests-sizes-received-ipv6",
        "dns-udp-responses-sizes-sent-ipv4",
        "dns-udp-responses-sizes-sent-ipv6",
        "dns-tcp-responses-sizes-sent-ipv4",
        "dns-tcp-responses-sizes-sent-ipv6",
    }
    assert expected_traffic <= traffic.keys()

    zones = data["zones"]["views"]["_default"]["zones"]
    assert any(zone.get("type") == "primary" for zone in zones)
    secondaries = [zone for zone in zones if zone.get("type") == "secondary"]
    assert secondaries
    assert all("refresh" in zone and "expires" in zone for zone in secondaries)

    # BIND 9.18 does not provide the JSON /json/v1/xfrins endpoint.
    assert "xfrins" not in data


def test_bind_920_transfer_contract() -> None:
    data = load("bind-9.20.json")

    assert data["bind_version"].startswith("9.20.")
    resolver = data["server"]["views"]["_default"]["resolver"]
    assert {"stats", "qtypes", "cache", "cachestats", "adb"} <= resolver.keys()

    xfrins = data["xfrins"]["views"]["_default"]["xfrins"]
    assert len(xfrins) == 2
    assert {"name", "state", "nbytes", "rate"} <= xfrins[0].keys()
    assert any(xfr["state"] == "Deferred" for xfr in xfrins)

    total_bytes = sum(int(xfr.get("nbytes", 0)) for xfr in xfrins)
    aggregate_rate = sum(int(xfr.get("rate", 0)) for xfr in xfrins)
    assert total_bytes == 24576
    assert aggregate_rate == 8192
