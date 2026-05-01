---
type: structural
title: "Knowledge Base Rules"
created: 2026-05-01
updated: 2026-05-01
tags: [knowledge_management, rules, wiki]
decay_class: structural
---

# Knowledge Base Rules

How the wiki works: architecture, page types, operations, formats.
Based on [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

---

## 1. Architecture — Three Layers

```
01_library/
  raw/        -> RAW (immutable sources)
  ...         -> WIKI (synthesis + compiled knowledge)
CLAUDE.md     -> SCHEMA (rules + navigation)
```

| Layer | Owner | Rule |
|-------|-------|------|
| Raw (`raw/`) | Human + LLM | Immutable. Never edit. Raw transcripts, articles, PDFs |
| Wiki (rest of `01_library/`) | LLM + Human | LLM writes and maintains. Human curates and directs |
| Schema (`CLAUDE.md` + rules) | Human + LLM | Co-evolved. Navigation, structure, workflows |

---

## 2. Structure

```
01_library/
  raw/                  <- IMMUTABLE sources (transcripts, articles, PDFs)
  index.md              <- Master catalog (updated on every ingest)
  KNOWLEDGE_BASE_RULES.md <- this file
  topics/               <- TOPIC PAGES: 1 topic = compiled knowledge + navigation
  articles/             <- SOURCE NOTES: article syntheses
  books/                <- SOURCE NOTES: book syntheses
  concepts/             <- personal concepts and frameworks
  podcasts/             <- SOURCE NOTES: podcast/video syntheses
  practices/            <- practices and exercises
  research/             <- research artifacts + consensus references
```

---

## 3. Two Page Types

### 3a. Source note — one source, one file

**1 source = 1 file.** Podcast, article, book -> synthesis with TL;DR, key ideas, links.

- **Trigger:** `/ingest` of one source
- **Where:** `articles/`, `podcasts/`, `books/` — by source category
- **Example:** `podcasts/health/attia_vo2max_longevity_tldr.md`

### 3b. Topic page — one topic, compiled knowledge from many sources

**1 topic = 1 page.** Combines knowledge from all source notes on a topic. Read the topic page — understand the topic. Want deeper — follow links to source notes.

- **Trigger:** 3+ source notes on same topic OR by request
- **Where:** always `topics/`
- **Example:** `topics/sleep.md`, `topics/protein.md`
- **Contains:** compiled conclusions + data + recommendations + links to all source notes
- **Differs from source note:** source note = "what Huberman said about sleep", topic page = "everything we know about sleep from all sources"

---

## 4. Operations

### Ingest (adding new source)

1. Save raw source in `raw/` (immutable)
2. Create source note in appropriate subfolder
3. **Topic page check:**
   - Check `topics/` — does a topic page exist for this theme?
   - **If yes** -> update topic page with new knowledge
   - **If no** -> count source notes on this topic (by tags). If 3+ -> suggest creating topic page
4. Post-processing:
   - Find 5-10 related files (by tags and keywords)
   - Add backlinks in related files
   - **Update `index.md`**
   - Append to `log.md`

**Key principle (Karpathy):** Ingest = update graph, not add isolated file.

### Query -> Save

Good answer to a question -> save as concept page or topic page.
Explorations compound, don't get lost in chat history.

### Lint (health checks)

Periodic checks:
- Orphan pages (no incoming links)
- Broken links
- Missing backlinks
- Files without tags

---

## 5. Special Files

| File | Purpose | Updated |
|------|---------|---------|
| `index.md` | Master catalog of all content | On every ingest |
| `log.md` (root) | Append-only chronology | On every event |

---

## 6. File Format

### YAML frontmatter (mandatory)

```yaml
---
type: podcast | article_synthesis | book | concept | topic | research | practice
title: "Title Here"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2, tag3]   # min 3, snake_case
id: zYYYYMMDDHHMM
confidence: 0.85            # optional
raw_source: "relative/path" # optional, link to raw/ source
---
```

### Linking

```markdown
[Descriptive text](../relative/path/to/file.md)
```

- Relative paths only
- Never wiki-links
- Backlinks mandatory

### Source note sections

1. **TL;DR** — 3-5 sentences
2. **Key Ideas** — 5-7 ideas with explanations
3. **Takeaways** — actionable items
4. **Data & Numbers** — specific metrics
5. **Related Files** — backlinks

---

## 7. Quality

### When to create a topic page
**Trigger:** 3+ source notes on a topic (determined by tags).

### When to update existing topic page
- New ingest on a topic that already has a topic page
- New data contradicts or supplements existing knowledge

### Red flags
- File without tags or with < 3 tags
- File without "Related Files" section
- Topic page without source notes
- Isolated file (no incoming links)
- `index.md` not updated after ingest
- 3+ source notes on topic but no topic page

---

## Related Files

- [Master Catalog](index.md)
- [CLAUDE.md](../CLAUDE.md)
