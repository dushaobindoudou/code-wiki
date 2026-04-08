---
name: llm-wiki:init
description: Initialize LLM Wiki directory structure at ~/.openwiki
---

# llm-wiki:init

Initialize the wiki directory structure.

## Usage

`/wiki init [--path <directory>]`

- Without arguments: initializes at `~/.openwiki`
- With `--path <dir>`: initializes at specified directory

## Directory Structure Created

```
<wiki-path>/
├── raw/
│   ├── sources/           # Original documents
│   └── assets/            # Images, resources
├── wiki/
│   ├── entities/          # Entity pages
│   ├── concepts/          # Concept pages
│   ├── summaries/         # Document summaries
│   ├── synthesis/         # Synthesis analyses
│   └── comparisons/       # Comparison analyses
├── schema/
│   └── CLAUDE.md          # Wiki behavior rules
├── index.md               # Content index
└── log.md                 # Operation log
```

## Process

1. Determine wiki path (default: ~/.openwiki, or --path argument)
2. Create all directories
3. Generate schema/CLAUDE.md with default wiki rules
4. Generate initial index.md with table of contents
5. Generate initial log.md with timestamp
6. Confirm success to user

## Schema/CLAUDE.md Template

```markdown
# LLM Wiki Agent Instructions

## Role
You are a wiki administrator maintaining a structured, accumulating knowledge base.

## Directory Structure
- entities/ — Entity pages (people, places, organizations)
- concepts/ — Concept pages (topics, theories)
- summaries/ — Source document summaries
- synthesis/ — Synthesis analyses
- comparisons/ — Comparison analyses

## Page Format
- Top-level title: [[pagename]]
- All pages must include YAML frontmatter
- Cross-references: [[entities/name]] or [[concepts/topic]]

## Ingest Flow
1. Read source document, extract key entities and concepts
2. Write summary page with: source, date, key points
3. Update related entity/concept pages (append new info)
4. Update index.md
5. Record to log.md

## Query Response Rules
- Must reference relevant pages [[pagename]]
- Encourage saving exploration results back to wiki
```

## Success Output

Show the created structure and confirm wiki is ready.