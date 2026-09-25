#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "docs" / "en"
PT = ROOT / "docs" / "pt-BR"


def main():
    en_files = {p.name for p in EN.glob("*.md")}
    pt_files = {p.name for p in PT.glob("*.md")}
    assert en_files == pt_files, f"documentation parity mismatch: EN={sorted(en_files)} PT={sorted(pt_files)}"

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

    print("Bilingual documentation parity passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
