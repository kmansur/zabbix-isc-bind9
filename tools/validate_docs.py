import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "docs" / "en"
PT = ROOT / "docs" / "pt-BR"
TEMPLATE = ROOT / "templates" / "7.0" / "isc-bind9-by-zabbix-agent.yaml"

ROOT_DOCS = (
    "README.md",
    "README.pt-BR.md",
    "CHANGELOG.md",
    "CHANGELOG.pt-BR.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING.pt-BR.md",
    "NOTICE.md",
    "NOTICE.pt-BR.md",
    "SECURITY.md",
    "SECURITY.pt-BR.md",
)

LINK_RE = re.compile(r"!?\\[[^\\]]*\\]\\(([^)]+)\\)")
H1_RE = re.compile(r"^#\\s+.+$", re.MULTILINE)
MACRO_ROW_RE = re.compile(
    r"^\\|\\s+\\x60(\\{\\$[^\\x60]+\\})\\x60\\s+\\|\\s+"
    r"\\x60([^\\x60]*)\\x60\\s+\\|",
    re.MULTILINE,
)

STALE_TEXT = (
    "Zabbix active checks are working for the host",
    "funcionamento dos active checks do Zabbix",
)


def documentation_files() -> list[Path]:
    files = [ROOT / name for name in ROOT_DOCS]
    files.extend(sorted(EN.glob("*.md")))
    files.extend(sorted(PT.glob("*.md")))
    return files


def validate_language_parity() -> None:
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


def validate_markdown_structure(files: list[Path]) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8")
        headings = H1_RE.findall(text)
        assert len(headings) == 1, (
            f"{path.relative_to(ROOT)} must contain exactly one top-level H1; "
            f"found {len(headings)}"
        )
        assert "\x60^# " not in text, (
            f"{path.relative_to(ROOT)} contains a corrupted inline Markdown fragment"
        )
        for stale in STALE_TEXT:
            assert stale not in text, (
                f"{path.relative_to(ROOT)} contains stale architecture text: {stale!r}"
            )


def validate_local_links(files: list[Path]) -> None:
    root_resolved = ROOT.resolve()

    for path in files:
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>")
            if not target or target.startswith("#"):
                continue
            if target.startswith(("http://", "https://", "mailto:")):
                continue

            target = target.split(' "')[0].split(" '")[0]
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue

            resolved = (path.parent / target).resolve()
            assert resolved == root_resolved or root_resolved in resolved.parents, (
                f"{path.relative_to(ROOT)} link escapes repository: {raw_target}"
            )
            assert resolved.exists(), (
                f"broken local link in {path.relative_to(ROOT)}: {raw_target}"
            )


def template_macros() -> dict[str, str]:
    data = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    template = data["zabbix_export"]["templates"][0]
    return {entry["macro"]: str(entry.get("value", "")) for entry in template["macros"]}


def documented_macros(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    return {macro: value for macro, value in MACRO_ROW_RE.findall(text)}


def validate_macro_documentation() -> None:
    expected = template_macros()
    for path in (EN / "configuration.md", PT / "configuration.md"):
        actual = documented_macros(path)
        assert actual == expected, (
            f"macro documentation drift in {path.relative_to(ROOT)}:\\n"
            f"expected={expected}\\nactual={actual}"
        )


def validate_release_markers() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    stable = (ROOT / "STABLE_VERSION").read_text(encoding="utf-8").strip()
    assert version == stable, (
        f"stable branch markers diverge: VERSION={version} STABLE_VERSION={stable}"
    )
    for path in (
        ROOT / "README.md",
        ROOT / "README.pt-BR.md",
        ROOT / "SECURITY.md",
        ROOT / "SECURITY.pt-BR.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert version in text, (
            f"{path.relative_to(ROOT)} does not mention current stable version {version}"
        )


def main() -> int:
    validate_language_parity()
    files = documentation_files()
    validate_markdown_structure(files)
    validate_local_links(files)
    validate_macro_documentation()
    validate_release_markers()

    print("Documentation structure, links, macro parity and release markers passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
