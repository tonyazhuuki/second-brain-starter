#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dreams Structurer — раскладывает RAW-мечты по сферам в structured-шаблон.

Usage:
  python3 tools/dreams_structurer.py --raw 00_vision/dreams/raw.md --out 00_vision/dreams/structured.md

Принцип:
- Читает bullets/строки из RAW (любой текст; bullets предпочтительны).
- Эвристически относит пункты к сферам по ключевым словам (без LLM).
- Строит structured-документ с разделами-сферами и переносит пункты.
Дополнительно:
- Делает мульти‑разметку: один пункт может попасть в несколько сфер (напр. «паспорт» → Документы + Пространство).
- Пишет JSON рядом c Markdown: список элементов с метками сфер, 4‑опор и уровнями сигналов.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
from typing import Dict, List, Tuple, Any

SPHERES = [
    ("Здоровье", {"сон","здоров","энерг","тело","спорт","zone2","hrv","пульс","вес","сауна","марафон","бег","йога"}),
    ("Отношения / Семья / Сообщество", {"отношен","семь","друз","сообществ","дет","партнер","партнёр","встреч","комьюнити","любим","семья"}),
    ("Творчество / Игра / Проекты", {"творч","муз","писать","рис","картин","сцен","альбом","книга","создат","проект","игр","арт","стиль","одев"}),
    ("Работа / Служение", {"работ","служен","клиент","польз","продукт","запуск","релиз","выручка","команда","настав","бизнес","систем"}),
    ("Документы / Гражданство / Локации", {"паспорт","граждан","виза","шенген","шэнген","внж","пмж","citizenship","visa","resid","локац"}),
    ("Пространство / Образ жизни", {"дом","пространств","переезд","путешеств","море","студия","город","среда","ритм","распорядок"}),
    ("Капитал / Финансы", {"капитал","инвест","доход","финанс","сбереж","портфель","акции","крипт","cash","budget","бюджет","налог","недвиж"}),
]

BULLET_RE = re.compile(r"^\s*[-*]\s+(.+)")
NUMBERED_RE = re.compile(r"^\s*(\d+)[\.\)]\s+(.+)")
EMPTY_RE = re.compile(r"^\s*$")
LINK_LINE_RE = re.compile(r"^\[.+\]\(.+\)$")
META_PREFIXES = (
    "Этот файл содержит",
    "Эти формулировки",
    "Важно помнить",
    "К ним можно возвращаться",
    "Они могут служить",
    "В них содержится",
)

# Four Pillars (Arthur Brooks) эвристики
PILLARS = {
    "Faith": {"вера","духов","бог","молит","медит","смысл"},
    "Family": {"семь","дет","муж","жена","партнер","партнёр","любим"},
    "Friends": {"друз","друг","сообществ","комьюн","встре","контакт","товарищ"},
    "Service": {"служен","работ","клиент","польз","бизнес","проект","систем","доход","выруч"},
}

def read_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()

def extract_items(raw_lines: List[str]) -> List[str]:
    items: List[str] = []
    for ln in raw_lines:
        if EMPTY_RE.match(ln):
            continue
        s = ln.rstrip()
        # отфильтровываем служебные строки: заголовки, цитаты, код-блоки, таблицы/ссылки
        if s.lstrip().startswith(("#", ">", "```")):
            continue
        if s.strip().startswith(("[", "|")):  # ссылки в квадратных скобках как отдельные строки, таблицы
            continue
        m = BULLET_RE.match(s)
        if m:
            content = m.group(1).strip()
            if LINK_LINE_RE.match(content) or (content.startswith("[") and "](" in content):
                continue
            if content.startswith(META_PREFIXES):
                continue
            items.append(content)
            continue
        n = NUMBERED_RE.match(s)
        if n:
            content = n.group(2).strip()
            if LINK_LINE_RE.match(content) or (content.startswith("[") and "](" in content):
                continue
            if content.startswith(META_PREFIXES):
                continue
            items.append(content)
            continue
        # всё прочее игнорируем (не мечты)
    return items

def classify(item: str) -> str:
    low = item.lower()
    # приоритетная маршрутизация по сферам (пространство → капитал → работа → творчество → здоровье)
    space_keys = {"дом","домик","камин","бань","баня","локац","квартира","жилье","жильё","терраса","сад"}
    if any(k in low for k in space_keys):
        return "Пространство / Образ жизни"
    capital_keys = {"недвиж","капитал","доход","инвест","сбереж","акции","крипт","бюджет","финанс","cash","portfolio","портфель"}
    if any(k in low for k in capital_keys):
        return "Капитал / Финансы"
    work_keys = {"бизнес","дело","прибыл","выруч","клиент","продукт","запуск","команда","служен"}
    if any(k in low for k in work_keys):
        return "Работа / Служение"
    art_keys = {"рис","карти","сцен","муз","альбом","книга","арт","творч","рисую","рисовать"}
    if any(k in low for k in art_keys):
        return "Творчество / Игра / Проекты"
    # «секс/тело» в связке с искусством → творчество
    if ("секс" in low or "обнажен" in low or "обнажён" in low) and any(k in low for k in ("рис","карти","арт","творч")):
        return "Творчество / Игра / Проекты"
    # приоритетная маршрутизация документов/гражданства
    doc_keys = {"паспорт","граждан","виза","шенген","шэнген","внж","пмж","citizenship","visa","resid"}
    if any(k in low for k in doc_keys):
        return "Документы / Гражданство / Локации"
    for sphere, keywords in SPHERES:
        if any(k in low for k in keywords):
            return sphere
    return "Прочее"

def classify_multi(item: str) -> Tuple[List[str], str]:
    """
    Возвращает (список_сфер, главная_сфера).
    Мульти‑разметка: собираем все подходящие сферы; главная выбирается по фиксированному порядку приоритета.
    """
    low = item.lower()
    matched: List[str] = []
    # жесткие правила
    if any(k in low for k in {"дом","домик","камин","бань","баня","локац","квартира","жилье","жильё","терраса","сад"}):
        matched.append("Пространство / Образ жизни")
    if any(k in low for k in {"недвиж","капитал","доход","инвест","сбереж","акции","крипт","бюджет","финанс","cash","portfolio","портфель"}):
        matched.append("Капитал / Финансы")
    # служение/социальные блага (общественный парк и т.п.) → работа/служение
    if any(k in low for k in {"бизнес","дело","прибыл","выруч","клиент","продукт","запуск","команда","служен","обществен","социаль","парк","для людей"}):
        matched.append("Работа / Служение")
    if (("секс" in low or "обнажен" in low or "обнажён" in low) and any(k in low for k in ("рис","карти","арт","творч"))) or any(k in low for k in {"рис","карти","сцен","муз","альбом","книга","арт","творч","рисую","рисовать"}):
        matched.append("Творчество / Игра / Проекты")
    if any(k in low for k in {"паспорт","граждан","виза","шенген","шэнген","внж","пмж","citizenship","visa","resid"}):
        matched.append("Документы / Гражданство / Локации")
    # здоровье включая сексуальное здоровье (если не арт-контекст)
    if any(k in low for k in {"сон","здоров","энерг","тело","спорт","zone2","hrv","пульс","вес","сауна","марафон","бег","йога","секс","оргазм","либидо"}):
        matched.append("Здоровье")
    # если документов касается — добавляем вторую метку «Пространство» (образ жизни)
    if "Документы / Гражданство / Локации" in matched and "Пространство / Образ жизни" not in matched:
        matched.append("Пространство / Образ жизни")
    # добираем общими ключами SPHERES
    if not matched:
        for sphere, keywords in SPHERES:
            if any(k in low for k in keywords):
                matched.append(sphere)
                break
    if not matched:
        matched = ["Прочее"]
    # порядок приоритета главной сферы
    priority = [
        "Пространство / Образ жизни",
        "Капитал / Финансы",
        "Работа / Служение",
        "Творчество / Игра / Проекты",
        "Документы / Гражданство / Локации",
        "Здоровье",
        "Отношения / Семья / Сообщество",
        "Прочее",
    ]
    main = next((s for s in priority if s in matched), matched[0])
    # уникализируем порядок matched с сохранением порядка
    seen = set()
    uniq = []
    for m in matched:
        if m not in seen:
            uniq.append(m)
            seen.add(m)
    return uniq, main

def classify_pillars(item: str) -> List[str]:
    low = item.lower()
    hits: List[str] = []
    for pillar, keys in PILLARS.items():
        if any(k in low for k in keys):
            hits.append(pillar)
    return hits or []

def pillar_levels(item: str, pillar: str) -> str:
    """L2 если совпало ≥2 ключа для столпа, иначе L1."""
    low = item.lower()
    keys = PILLARS[pillar]
    count = sum(1 for k in keys if k in low)
    return "L2" if count >= 2 else "L1"

def truncate(text: str, limit: int = 100) -> str:
    t = text.strip()
    return t if len(t) <= limit else (t[:limit - 1] + "…")

def build_structured(groups: Dict[str, List[str]], pillars_map: Dict[str, List[str]], pillars_lvl: Dict[str, List[str]]) -> str:
    lines: List[str] = []
    lines.append("# 🌿 Structured Dreams — навигация по сферам")
    lines.append("")
    lines.append("> Автосбор по эвристикам; проверь и поправь формулировки. Связи с целями: см. `00_vision/goals/_year_template.md` и `_monthly_template.md`.")
    lines.append("")
    # Four Pillars coverage (читабельный формат)
    lines.append("## 🧭 Four Pillars — покрытие мечт")
    total_items = sum(len(v) for v in groups.values())
    if total_items == 0:
        total_items = 1
    lines.append(f"- Всего мечт: {total_items}")
    lines.append("")
    def bar(pct: int) -> str:
        blocks = max(1, round(pct / 10))
        return "█" * blocks + "░" * (10 - blocks if blocks <= 10 else 0)
    weak: List[str] = []
    for pillar in ("Faith","Family","Friends","Service"):
        items = pillars_map.get(pillar, [])
        pct = round(100 * len(items) / total_items)
        tag = " — тонко" if len(items) == 0 else ""
        if len(items) == 0:
            weak.append(pillar)
        lines.append(f"### {pillar} — {pct}% ({len(items)}/{total_items}) {tag}")
        lines.append(f"[{bar(pct)}]")
        # уровни сигналов
        lvls = pillars_lvl.get(pillar, [])
        l2 = sum(1 for x in lvls if x == "L2")
        l1 = sum(1 for x in lvls if x == "L1")
        lines.append(f"- Сигналы: L2={l2}, L1={l1}")
        # примеры (с обрезкой)
        ex = "—" if not items else "; ".join(truncate(x) for x in items[:2])
        lines.append(f"- Примеры: {ex}")
        if len(items) == 0:
            lines.append(f"- Шаг: см. `../../02_frameworks/balance_four_pillars.md` → добавить 1 мечту/шаг в эту опору")
        lines.append("")
    if weak:
        lines.append(f"_Где тонко:_ {', '.join(weak)}")
    else:
        lines.append("_Где тонко:_ явных провалов не видно по эвристикам; проверь вручную.")
    # actionable блок на месяц (опционально делается отдельным скриптом)
    lines.append("")
    for sphere, _ in SPHERES + [("Прочее", set())]:
        lines.append(f"## {sphere}")
        items = groups.get(sphere, [])
        if not items:
            lines.append("- —")
        else:
            for it in items:
                lines.append(f"- {it}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, help="Путь к RAW-файлу мечт (md)")
    ap.add_argument("--out", required=True, help="Путь для вывода structured (md)")
    args = ap.parse_args()

    raw_path = Path(args.raw)
    out_path = Path(args.out)
    if not raw_path.exists():
        raise SystemExit(f"RAW file not found: {raw_path}")

    items = extract_items(read_lines(raw_path))
    groups: Dict[str, List[str]] = {}
    pillars_map: Dict[str, List[str]] = {}
    pillars_lvl: Dict[str, List[str]] = {}
    json_items: List[Dict[str, Any]] = []
    for it in items:
        spheres, main = classify_multi(it)
        for s in spheres:
            groups.setdefault(s, []).append(it)
        pill_hits = classify_pillars(it)
        for p in pill_hits:
            pillars_map.setdefault(p, []).append(it)
            pillars_lvl.setdefault(p, []).append(pillar_levels(it, p))
        json_items.append({
            "text": it,
            "spheres": spheres,
            "main_sphere": main,
            "pillars": pill_hits,
            "pillars_levels": {p: pillar_levels(it, p) for p in pill_hits},
        })

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_structured(groups, pillars_map, pillars_lvl), encoding="utf-8")
    # JSON рядом: same path, .json
    json_path = out_path.with_suffix(".json")
    try:
        import json as _json
        json_payload = {
            "raw": str(raw_path),
            "structured_md": str(out_path),
            "items": json_items,
            "pillars_summary": {k: {"count": len(v)} for k, v in pillars_map.items()},
        }
        json_path.write_text(_json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"JSON written to: {json_path}")
    except Exception as e:
        print(f"JSON write failed: {e}")
    print(f"Structured written to: {out_path}")

if __name__ == "__main__":
    main()


