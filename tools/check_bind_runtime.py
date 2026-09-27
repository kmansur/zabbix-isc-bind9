"""Validate the live ISC BIND statistics-channel JSON contract."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from typing import Any


def get_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=5) as response:
        if response.status != 200:
            raise RuntimeError(f"{url}: unexpected HTTP status {response.status}")
        return json.loads(response.read().decode("utf-8"))


def wait_json(url: str, timeout: int) -> dict[str, Any]:
    deadline = time.time() + timeout
    last_error: Exception | None = None

    while time.time() < deadline:
        try:
            return get_json(url)
        except (OSError, ValueError, urllib.error.URLError) as exc:
            last_error = exc
            time.sleep(2)

    raise RuntimeError(f"{url}: endpoint did not become ready: {last_error}")


def validate(base_url: str, expected_version: str, timeout: int) -> None:
    status = wait_json(f"{base_url}/json/v1/status", timeout)
    actual_version = str(status.get("version", ""))
    if not actual_version.startswith(expected_version + "."):
        raise RuntimeError(
            f"expected BIND {expected_version}.x, got {actual_version!r}"
        )

    server = get_json(f"{base_url}/json/v1/server")
    if "views" not in server:
        raise RuntimeError("server endpoint does not contain views")

    # BIND omits zero-valued counter families on a freshly started/idle server.
    # When present, they must still have the object shape used by template LLD.
    for optional_map in ("nsstats", "qtypes", "rcodes"):
        if optional_map in server and not isinstance(server[optional_map], dict):
            raise RuntimeError(
                f"server endpoint {optional_map!r} is not a JSON object"
            )

    net = get_json(f"{base_url}/json/v1/net")
    if "sockstats" not in net:
        raise RuntimeError("net endpoint does not contain sockstats")

    mem = get_json(f"{base_url}/json/v1/mem")
    memory = mem.get("memory", {})
    required_memory = {"InUse", "Malloced", "contexts"}
    missing = required_memory - memory.keys()
    if missing:
        raise RuntimeError(f"memory endpoint missing keys: {sorted(missing)}")

    traffic = get_json(f"{base_url}/json/v1/traffic")
    if "traffic" not in traffic:
        raise RuntimeError("traffic endpoint does not contain traffic")

    zones = get_json(f"{base_url}/json/v1/zones")
    if "views" not in zones:
        raise RuntimeError("zones endpoint does not contain views")

    xfrins_url = f"{base_url}/json/v1/xfrins"
    if expected_version == "9.20":
        xfrins = get_json(xfrins_url)
        if "views" not in xfrins:
            raise RuntimeError("BIND 9.20 xfrins endpoint does not contain views")
    elif expected_version == "9.18":
        try:
            get_json(xfrins_url)
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                raise
        else:
            raise RuntimeError("BIND 9.18 unexpectedly exposes /json/v1/xfrins")

    print(
        f"Validated live BIND {actual_version}: "
        "status/server/zones/net/mem/traffic"
        + ("/xfrins" if expected_version == "9.20" else "; xfrins correctly absent")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:18053")
    parser.add_argument("--version", required=True, choices=("9.18", "9.20"))
    parser.add_argument("--wait", type=int, default=120)
    args = parser.parse_args()
    validate(args.base_url.rstrip("/"), args.version, args.wait)


if __name__ == "__main__":
    main()
