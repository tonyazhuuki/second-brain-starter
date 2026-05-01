# Second Brain — Claude Code Instructions

## Boundaries

- NEVER delete existing content without explicit request
- NEVER use wiki-links `[[file]]` — only `[text](relative/path.md)`
- NEVER use absolute paths `/Users/...` in links
- NEVER edit files in `01_library/raw/` — immutable source layer
- NEVER edit past entries in `log.md` — append-only
- NEVER skip backlinks: if A links to B -> B must link back to A

---

## Project Structure

```
00_vision/     — dreams, goals, principles
01_library/    — knowledge base: raw sources + synthesis + topics + research
04_therapy/    — private (optional)
05_personal/   — health, calls, personal
06_projects/   — active projects
log.md         — append-only chronological event log
tools/         — scripts and utilities
```

---

## Knowledge Base Architecture (Karpathy LLM Wiki)

Three layers:
1. **Raw** (`01_library/raw/`) — immutable sources. Never edit.
2. **Wiki** (`01_library/` rest) — synthesis, topics, concepts. LLM writes, human curates.
3. **Schema** (this file + `.claude/rules/`) — rules and navigation.

Two page types:
- **Source note** — 1 source = 1 file (podcast, article, book synthesis)
- **Topic page** — 1 topic = compiled knowledge from many sources

Full rules: [KNOWLEDGE_BASE_RULES.md](01_library/KNOWLEDGE_BASE_RULES.md)

---

## Key Context Files

| File | Purpose |
|------|---------|
| `01_library/KNOWLEDGE_BASE_RULES.md` | Wiki contract: architecture, operations, formats |
| `01_library/index.md` | Master catalog (update on every ingest) |
| `log.md` | Append-only event log |

---

## Linking Standard

```markdown
[Descriptive text](../relative/path/to/file.md)
```

- Relative paths only (never absolute)
- Never wiki-links `[[file]]`
- Backlinks mandatory: A links B -> B links A

---

## YAML Frontmatter (every content file)

```yaml
---
type: podcast | article_synthesis | book | concept | topic | research | practice
title: "Title Here"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag_one, tag_two, tag_three]   # min 3, snake_case
id: zYYYYMMDDHHMM
confidence: 0.85       # optional, 0.0-1.0
decay_class: reference # optional: reference | structural | living
---
```

---

## File Operations

1. **Read before edit** — always
2. **Use Edit tool** for targeted changes, not Write
3. **Preserve all content** when adding new
4. **Show plan** before structural changes

---

## Related Files

- [Knowledge Base Rules](01_library/KNOWLEDGE_BASE_RULES.md)
- [Master Catalog](01_library/index.md)
