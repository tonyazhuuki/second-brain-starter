#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RU2EN = {
    "январь": "january", "февраль": "february", "март": "march", "апрель": "april",
    "май": "may", "июнь": "june", "июль": "july", "август": "august",
    "сентябрь": "september", "октябрь": "october", "ноябрь": "november", "декабрь": "december",
}
EN_ORDER = ["january","february","march","april","may","june","july","august","september","october","november","december"]
RU_CAP = {
    "january":"Январь","february":"Февраль","march":"Март","april":"Апрель","may":"Май","june":"Июнь",
    "july":"Июль","august":"Август","september":"Сентябрь","october":"Октябрь","november":"Ноябрь","december":"Декабрь"
}

def mon_to_en(mon: str) -> str:
    m = mon.strip().lower()
    if m in EN_ORDER:
        return m
    if m in RU2EN:
        return RU2EN[m]
    raise SystemExit(f"Unknown month: {mon}")

def month_num(en: str) -> int:
    return EN_ORDER.index(en) + 1

def neighbor_month(en: str, year: int, delta: int) -> tuple[str, int]:
    idx = EN_ORDER.index(en)
    n = idx + delta
    y = year
    if n < 0:
        n += 12
        y -= 1
    if n > 11:
        n -= 12
        y += 1
    return EN_ORDER[n], y

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def gen_month(year: int, mon: str) -> Path:
    en = mon_to_en(mon)
    mon_num = month_num(en)
    ym = f"{year}-{mon_num:02d}"
    mon_id = f"{en}-{year}"
    prev_en, prev_y = neighbor_month(en, year, -1)
    next_en, next_y = neighbor_month(en, year, +1)
    prev_name = f"{prev_en}_{prev_y}"
    next_name = f"{next_en}_{next_y}"

    template_path = ROOT / "00_vision" / "goals" / "_monthly_template.md"
    if not template_path.exists():
        raise SystemExit(f"Template not found: {template_path}")
    tpl = read(template_path)
    title_ru = f"{RU_CAP[en]} {year}"
    content = (tpl
        .replace("{month-id}", mon_id)
        .replace("{YYYY-MM}", ym)
        .replace("{prev}", prev_name)
        .replace("{next}", next_name)
        .replace("{title}", title_ru)
        .replace("{лейтмотив}", "")
    )
    out = ROOT / "00_vision" / "goals" / str(year) / f"{en}_{year}.md"
    write(out, content)
    return out

def gen_year(year: int) -> Path:
    template_path = ROOT / "00_vision" / "goals" / "_year_template.md"
    if not template_path.exists():
        raise SystemExit(f"Template not found: {template_path}")
    tpl = read(template_path)
    content = tpl.replace("{YYYY}", str(year))
    out = ROOT / "00_vision" / "goals" / f"{year}.md"
    write(out, content)
    return out

def main():
    ap = argparse.ArgumentParser(description="Second Brain — note generator from templates")
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("month")
    m.add_argument("--year", type=int, required=True)
    m.add_argument("--mon", type=str, required=True, help="Month name: january..december или по‑русски")
    y = sub.add_parser("year")
    y.add_argument("--year", type=int, required=True)
    args = ap.parse_args()

    if args.cmd == "month":
        out = gen_month(args.year, args.mon)
        print(f"Created: {out}")
    elif args.cmd == "year":
        out = gen_year(args.year)
        print(f"Created: {out}")

if __name__ == "__main__":
    main()


