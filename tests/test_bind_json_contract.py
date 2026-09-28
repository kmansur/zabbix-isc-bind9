"""Contract tests for the BIND JSON structures used by the template."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"

KNOWN_NSSTATS = {
    "Requestv4",
    "Requestv6",
    "QryDropped",
    "QrySERVFAIL",
    "QryRecursion",
    "RecursClients",
    "RecursHighwater",
    "TCPConnHighWater",
}

KNOWN_SOCKSTATS = {
    "UDP4Active",
    "UDP6Active",
    "UDP4Open",
    "UDP6Open",
    "TCP4Active",
    "TCP6Active",
    "TCP4Clients",
    "TCP6Clients",
    "TCP4Open",
    "TCP6Open",
}

KNOWN_RESOLVER_STATS = {
    "QueryCurUDP",
    "QueryCurTCP",
    "NumFetch",
    "BucketSize",
    "Queryv4",
    "Queryv6",
}

KNOWN_RESOLVER_ADB = {
    "nentries",
    "entriescnt",
    "nnames",
    "namescnt",
}

KNOWN_CACHE_STATS = {
    "CacheBuckets",
    "CacheHits",
    "CacheMisses",
    "QueryHits",
    "QueryMisses",
    "DeleteLRU",
    "DeleteTTL",
    "CoveringNSEC",
    "CacheNodes",
    "CacheNSECNodes",
    "TreeMemInUse",
    "TreeMemMax",
    "TreeMemTotal",
    "HeapMemInUse",
    "HeapMemMax",
    "HeapMemTotal",
}


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
    assert isinstance(data["mem"]["memory"]["contexts"], list)

    ns_gauges = {"RecursClients", "TCPConnHighWater"}
    assert ns_gauges <= server["nsstats"].keys()

    resolver_gauges = {"QueryCurUDP", "QueryCurTCP", "NumFetch", "BucketSize"}
    assert resolver_gauges <= resolver["stats"].keys()

    adb_gauges = {"nentries", "entriescnt", "nnames", "namescnt"}
    assert adb_gauges <= resolver["adb"].keys()

    socket_gauges = {
        "UDP4Active",
        "UDP6Active",
        "TCP4Active",
        "TCP6Active",
        "TCP4Clients",
        "TCP6Clients",
    }
    assert socket_gauges <= data["net"]["sockstats"].keys()

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
    assert {"RecursClients", "RecursHighwater", "TCPConnHighWater"} <= data["server"][
        "nsstats"
    ].keys()

    resolver = data["server"]["views"]["_default"]["resolver"]
    assert {"stats", "qtypes", "cache", "cachestats", "adb"} <= resolver.keys()
    assert {"QueryCurUDP", "QueryCurTCP", "NumFetch", "BucketSize"} <= resolver[
        "stats"
    ].keys()
    assert {"nentries", "entriescnt", "nnames", "namescnt"} <= resolver["adb"].keys()
    assert {"UDP4Active", "TCP4Active", "TCP4Clients"} <= data["net"][
        "sockstats"
    ].keys()

    xfrins = data["xfrins"]["views"]["_default"]["xfrins"]
    assert len(xfrins) == 2
    assert {"name", "state", "nbytes", "rate"} <= xfrins[0].keys()
    assert any(xfr["state"] == "Deferred" for xfr in xfrins)

    total_bytes = sum(int(xfr.get("nbytes", 0)) for xfr in xfrins)
    aggregate_rate = sum(int(xfr.get("rate", 0)) for xfr in xfrins)
    assert total_bytes == 24576
    assert aggregate_rate == 8192


def test_metric_classification_allowlists_cover_supported_fixtures() -> None:
    """Fail loudly when supported fixtures introduce an unclassified metric."""

    for fixture in ("bind-9.18.json", "bind-9.20.json"):
        data = load(fixture)
        server = data["server"]
        assert set(server.get("nsstats", {})) <= KNOWN_NSSTATS
        assert set(data.get("net", {}).get("sockstats", {})) <= KNOWN_SOCKSTATS

        for view in server.get("views", {}).values():
            resolver = view.get("resolver", {})
            assert set(resolver.get("stats", {})) <= KNOWN_RESOLVER_STATS
            assert set(resolver.get("adb", {})) <= KNOWN_RESOLVER_ADB
            assert set(resolver.get("cachestats", {})) <= KNOWN_CACHE_STATS


def test_secondary_zone_expiry_fixture_can_be_negative() -> None:
    """Expired-zone fixtures must remain representable as a signed delta."""

    data = load("bind-9.18.json")
    zones = data["zones"]
    now = datetime.fromisoformat(zones["current-time"].replace("Z", "+00:00"))

    secondary = next(
        zone
        for zone in zones["views"]["_default"]["zones"]
        if zone.get("type") == "secondary"
    )
    expired = dict(secondary)
    expired["expires"] = "2026-09-24T18:36:26.000Z"

    expires_at = datetime.fromisoformat(expired["expires"].replace("Z", "+00:00"))
    expires_in = int((expires_at - now).total_seconds())

    assert now.tzinfo == timezone.utc
    assert expires_in < 0
    assert expired["serial"] > 0
