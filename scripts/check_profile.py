#!/usr/bin/env python3
"""Sanity checks for the profile README (stdlib only, run in CI)."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    errors: list[str] = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    for needle in ("Daniel Alonso Gómez", "github-contribution-grid-snake"):
        if needle not in readme:
            errors.append(f"README is missing {needle!r}")

    # Every local image the README references must exist and be valid XML.
    local = set(re.findall(r'(?:src|srcset)="\./([^"]+)"', readme))
    if not local:
        errors.append("README references no local assets")
    for rel in sorted(local):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing asset: {rel}")
            continue
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"invalid SVG {rel}: {exc}")

    # Every <img> needs alt text (accessibility).
    for tag in re.findall(r"<img\b[^>]*>", readme):
        if not re.search(r'\balt="[^"]+"', tag):
            errors.append(f"img without alt text: {tag[:80]}")

    for err in errors:
        print(f"::error::{err}")
    print(f"checked {len(local)} local assets")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
