import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "docs" / "en"
PT = ROOT / "docs" / "pt-BR"
TEMPLATE = ROOT / "templates" / "7.0" / "isc-bind9-by-zabbix-agent.yaml"

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MACRO_ROW_RE = re.compile(
    r"^\|\s*`(?P<macro>\{\$[^`]+\})`\s*\|\s*`(?P<default>[^`]*)`\s*\|",
    re.MULTILINE,
)


def markdown_files():
    yield from sorted(ROOT.glob("*.md"))
    yield from sorted((ROOT / "docs").rglob("*.md"))


def validate_language_parity():
    en_files = {p.name for p in EN.glob("*.md")}
    pt_files = {p.name for p in PT.glob("*.md")}
    assert en_files == pt_files, (
        f"documentation parity mismatch: EN={sorted(en_files)} PT={sorted(pt_files)}"
    )

    pairs = [
        ("README.md", "README.pt-BR.md"),
        ("CHANGELOG.md", "CHANGELOG.pt-BR.md"),
        ("CONTRIBUTING.md", "CONTRIBUTING.pt-BR.md"),
        ("NOTICE.md", "NOTICE.pt-BR.md"),
        ("SECURITY.md", "SECURITY.pt-BR.md"),
    ]
    for en, pt in pairs:
        assert (ROOT / en).is_file(), f"missing {en}"
        assert (ROOT / pt).is_file(), f"missing {pt}"


def validate_markdown_structure():
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        h1 = [line for line in text.splitlines() if line.startswith("# ")]
        assert len(h1) == 1, f"{path.relative_to(ROOT)}: expected one H1, got {h1}"


def validate_internal_links():
    broken = []

    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip().strip("<>")
            if not target or target.startswith(
                ("#", "https://", "http://", "mailto:")
            ):
                continue

            target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                broken.append((path.relative_to(ROOT), target, "outside repository"))
                continue

            if not resolved.exists():
                broken.append((path.relative_to(ROOT), target, "missing"))

    assert not broken, f"broken internal documentation links: {broken}"


def template_macros():
    export = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))["zabbix_export"]
    template = export["templates"][0]
    return {entry["macro"]: str(entry.get("value", "")) for entry in template["macros"]}


def validate_configuration_macro_tables():
    expected = template_macros()

    for path in (EN / "configuration.md", PT / "configuration.md"):
        text = path.read_text(encoding="utf-8")
        rows = {
            match.group("macro"): match.group("default")
            for match in MACRO_ROW_RE.finditer(text)
        }

        assert rows.keys() == expected.keys(), (
            f"{path.relative_to(ROOT)} macro-table mismatch: "
            f"documented={sorted(rows)} expected={sorted(expected)}"
        )
        assert rows == expected, (
            f"{path.relative_to(ROOT)} macro defaults differ from template: "
            f"documented={rows} expected={expected}"
        )


def main():
    validate_language_parity()
    validate_markdown_structure()
    validate_internal_links()
    validate_configuration_macro_tables()

    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
