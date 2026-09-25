from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_version_markers():
    assert (ROOT / "VERSION").read_text().strip() == "0.1.1"
    assert (ROOT / "STABLE_VERSION").read_text().strip() == "0.0.0"


def test_required_root_files():
    required = [
        "README.md",
        "README.pt-BR.md",
        "LICENSE",
        "NOTICE.md",
        "NOTICE.pt-BR.md",
        "CHANGELOG.md",
        "CHANGELOG.pt-BR.md",
        "CONTRIBUTING.md",
        "CONTRIBUTING.pt-BR.md",
        "SECURITY.md",
        "SECURITY.pt-BR.md",
    ]
    for name in required:
        assert (ROOT / name).is_file(), name


def test_template_paths():
    for version in ("7.0", "8.0"):
        path = ROOT / "templates" / version / "isc-bind9-by-zabbix-agent.yaml"
        assert path.is_file()


def test_documentation_language_parity():
    en = {p.name for p in (ROOT / "docs" / "en").glob("*.md")}
    pt = {p.name for p in (ROOT / "docs" / "pt-BR").glob("*.md")}
    assert en == pt
