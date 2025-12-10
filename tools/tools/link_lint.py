#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import re
import sys
from pathlib import Path

# [text](relative/path.md) — исключаем картинки ![
RE_MD_LINK = re.compile(r'(?<!\!)\[[^\]]+\]\(([^)]+)\)')

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {".git", ".github", "node_modules", ".venv", ".history"}
BACKLINK_EXCLUDE_PREFIXES = (
    ".cursor/rules/",
    "02_frameworks/templates/",
)

def is_markdown(path: Path) -> bool:
    return path.suffix.lower() in {".md", ".mdc"}

def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*"):
        if p.is_file() and is_markdown(p):
            parts = set(p.parts)
            if parts & EXCLUDE_DIRS:
                continue
            files.append(p)
    return files

def extract_links(md_path: Path) -> list[str]:
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    return RE_MD_LINK.findall(text)

def is_external(link: str) -> bool:
    return link.startswith("http://") or link.startswith("https://") or link.startswith("mailto:")

def normalize_target(src_file: Path, link: str) -> Path:
    link_no_anchor = link.split("#", 1)[0]
    return (src_file.parent / link_no_anchor).resolve()

def relpath(from_file: Path, to_file: Path) -> str:
    return Path(Path.relpath(to_file, start=from_file.parent)).as_posix()

def is_backlink_exempt(target_rel_from_root: str, source_name: str) -> bool:
    if any(target_rel_from_root.startswith(pref) for pref in BACKLINK_EXCLUDE_PREFIXES):
        return True
    if source_name == "index.md":
        return True
    return False

def check_repo() -> int:
    errors: list[str] = []
    md_files = iter_markdown_files()
    md_set = {p.resolve() for p in md_files}

    for src in md_files:
        links = extract_links(src)
        for link in links:
            if is_external(link):
                continue
            target_abs = normalize_target(src, link)
            target_rel_from_root = target_abs.relative_to(ROOT).as_posix() if target_abs.exists() else "(missing)"
            if not target_abs.exists():
                errors.append(f"[MISSING] {src.relative_to(ROOT)} → {link}")
                continue
            if not is_markdown(target_abs):
                continue
            if not is_backlink_exempt(target_rel_from_root, src.name):
                try:
                    backtext = target_abs.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    errors.append(f"[READ_FAIL] cannot read target for backlink: {target_rel_from_root}")
                    continue
                expected_backlink = relpath(target_abs, src)
                if f"]({expected_backlink})" not in backtext:
                    errors.append(f"[NO_BACKLINK] {src.relative_to(ROOT)} ↔ {target_rel_from_root} (expect link to '{expected_backlink}')")

    if errors:
        print("Link Lint — errors found:")
        for e in errors:
            print(" -", e)
        return 1
    print("Link Lint — OK")
    return 0

if __name__ == "__main__":
    sys.exit(check_repo())


