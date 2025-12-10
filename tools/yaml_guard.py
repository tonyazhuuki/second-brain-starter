#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [
    ROOT / "00_vision" / "goals",
    ROOT / "00_vision" / "analytics",
    ROOT / "06_projects",
    ROOT / "01_library",
]

def is_markdown(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in {".md", ".mdc"}

def has_frontmatter(p: Path) -> bool:
    try:
        head = p.read_text(encoding="utf-8", errors="ignore").lstrip()
    except Exception:
        return False
    return head.startswith("---\n")

def main() -> int:
    errors: list[str] = []
    for d in TARGET_DIRS:
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if is_markdown(p):
                if not has_frontmatter(p):
                    errors.append(f"[NO_YAML] {p.relative_to(ROOT)}")
    if errors:
        print("YAML Guard — files without frontmatter:")
        for e in errors:
            print(" -", e)
        return 1
    print("YAML Guard — OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())


