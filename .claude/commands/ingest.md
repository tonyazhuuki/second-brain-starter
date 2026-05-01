# Ingest — Smart Source Router

Add source to Second Brain: **$ARGUMENTS**

## Step 1: Detect Source Type

| Signal | Type | Action |
|--------|------|--------|
| `youtube.com` or `youtu.be` | YouTube | Get transcript -> full analysis |
| `.pdf` extension | PDF | Read -> synthesize |
| `http` URL | Article | Fetch -> synthesize |
| Plain text | Note | Save directly |

## Step 2: Save Raw Source

Save to `01_library/raw/` (appropriate subfolder):

```yaml
---
type: raw_source
source_url: "URL"
created: YYYY-MM-DD
raw: true
---
```

## Step 3: Create Source Note

Create synthesis in `01_library/` (appropriate subfolder).

Required sections:
1. **TL;DR** — 3-5 sentences
2. **Key Ideas** — 5-7 ideas with explanations
3. **Takeaways** — actionable items
4. **Data & Numbers** — specific metrics
5. **Related Files** — backlinks

YAML must include `raw_source:` pointing to the raw file.

## Step 4: Post-Processing (MANDATORY)

### 4a. Find related files (5-10)
Search by tags and key terms across vault.

### 4b. Add backlinks to related files
Each related file gets a link back to the new file.

### 4c. Topic page check
- Check `01_library/topics/` — topic page exists for this theme?
- **If yes** -> update it with new knowledge
- **If no** -> count source notes on topic. If 3+ -> suggest creating topic page

### 4d. Update index.md
Add new file to `01_library/index.md` in appropriate section.

### 4e. Append to log.md

```markdown
## [YYYY-MM-DD] ingest | Title
- Type: youtube / article / pdf / note
- Path: path/to/synthesis.md
- Raw: path/to/raw/source.md
- Related updated: file1.md, file2.md
- Tags: tag1, tag2, tag3
```
