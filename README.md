# Second Brain Starter v2.0

A ready-to-use knowledge base template for Claude Code + Obsidian, based on [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) architecture.

## What's Inside

```
00_vision/     — dreams, goals, personal strategy
01_library/    — knowledge base (the core)
  raw/         — immutable sources (transcripts, articles, PDFs)
  topics/      — compiled knowledge pages (1 topic = many sources)
  articles/    — article syntheses
  books/       — book syntheses
  podcasts/    — podcast/video syntheses
  concepts/    — personal concepts
  practices/   — practices and exercises
  research/    — research artifacts
  index.md     — master catalog
  KNOWLEDGE_BASE_RULES.md — how the wiki works
04_therapy/    — private (optional)
05_personal/   — health, personal
06_projects/   — active projects
log.md         — append-only event log
CLAUDE.md      — AI instructions
```

## Quick Start

1. **Fork/clone** this repo
2. **Open in Claude Code:** `cd second-brain-starter && claude`
3. **Ingest your first source:** `/ingest https://youtube.com/watch?v=...`
4. Claude Code will create raw transcript + synthesis + update index

## Architecture (Karpathy LLM Wiki)

Three layers:
- **Raw** (`01_library/raw/`) — immutable source material. Never edited.
- **Wiki** (rest of `01_library/`) — LLM-generated synthesis. Two page types:
  - **Source note** — 1 source = 1 file (what author X said about topic Y)
  - **Topic page** — 1 topic = compiled knowledge from ALL sources
- **Schema** (`CLAUDE.md` + `.claude/rules/`) — rules for the AI

### How Ingest Works

```
New source -> 01_library/raw/ (immutable copy)
                    |
                    v
          01_library/synthesis (source note)
                    |
                    v
          Update: index.md + related files + topic pages + log.md
```

One ingest should touch 5-15 files (not just create one isolated file).

### When Topic Pages Are Created

After 3+ source notes on the same topic, create a topic page in `topics/` that compiles all knowledge into one document. Reading a topic page = understanding the topic.

## Key Files

| File | Purpose |
|------|---------|
| [`CLAUDE.md`](CLAUDE.md) | AI instructions — edit to customize |
| [`01_library/KNOWLEDGE_BASE_RULES.md`](01_library/KNOWLEDGE_BASE_RULES.md) | Wiki contract — how knowledge is organized |
| [`01_library/index.md`](01_library/index.md) | Master catalog — auto-updated on ingest |
| [`log.md`](log.md) | Event log — append-only history |

## Skills (Claude Code slash commands)

| Command | What it does |
|---------|-------------|
| `/ingest <URL or text>` | Add source to knowledge base |

## Customization

1. **Edit `CLAUDE.md`** — add your communication preferences, project context
2. **Edit `.claude/rules/`** — add domain-specific rules
3. **Add `.claude/commands/`** — create custom skills

## Works With

- **Claude Code** (primary) — terminal AI assistant
- **Obsidian** (optional) — visual navigation, graph view
- **Git** — version control for your knowledge

## Credits

- Architecture: [Andrej Karpathy — LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Template: [@tonyazhuuki](https://github.com/tonyazhuuki)
