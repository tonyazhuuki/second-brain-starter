---
type: meta
title: "Raw Sources — Immutable Layer"
created: 2026-05-01
tags: [meta, raw, immutable]
decay_class: structural
---

# raw/ — Immutable Sources

> **DO NOT EDIT.** Raw sources are never modified after creation. LLM reads only.

## Structure

```
raw/
  articles/     — original articles (web clippings, markdown)
  podcasts/     — raw podcast transcripts (before analysis)
  pdfs/         — PDF documents
  transcripts/  — voice notes, calls, lectures
  clips/        — screenshots, quotes, excerpts
```

## Rules

1. **Immutable.** Once a file enters raw/ — it is never edited.
2. **Synthesis separately.** Analyses live in `01_library/` alongside (articles/, podcasts/, etc.)
3. **Naming:** `YYYY-MM-DD_source_title.md`
4. **YAML frontmatter:** type: raw_source, source_url, created, raw: true

## Why raw exists

Synthesis doesn't always capture every nuance. Raw = full text for re-reading and discussing ideas.
