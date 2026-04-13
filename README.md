# Code Wiki

> A personal/team knowledge base system built on Karpathy's LLM Wiki pattern

**[English](README.md)** | **[中文](README_CN.md)**

---

## Overview

Code Wiki is a Claude Code Skill for building personal/team knowledge bases. It implements Karpathy's LLM Wiki pattern, creating a structured, compounding wiki between you and your raw documents.

**Core Idea**: Knowledge is not rediscovered on every query, but built incrementally with each ingest.

### Core Features

- 🗂️ **Structured Storage**: Pure file system, no external dependencies
- 🔄 **Incremental Ingest**: Each source document touches 10-15 wiki pages
- 🔗 **Knowledge Graph**: Entity relations, concept relations, code path associations
- 🌐 **Chinese Support**: Complete Chinese commands and natural language triggers
- 🔍 **Smart Query**: Q&A with citation and save-back-to-wiki feature
- 🧹 **Health Check**: Orphan pages, link integrity, code path validation
- 📁 **Project Integration**: Create wiki in project directory for version control

---

## Quick Start

### 1. Initialize Wiki

```bash
# Default location: ~/.openwiki
/wiki init

# Create in project root (recommended for development projects)
/wiki init --path ./wiki

# Or custom directory
/wiki init --path ~/my-wiki
```

### 2. Ingest Documents

```bash
/wiki ingest ~/documents/article.md
```

Each ingest automatically:
- Creates summary page
- Extracts/updates entities (people, organizations, projects)
- Extracts/updates concepts
- Updates entity/concept relations
- Checks for synthesis/comparison page needs
- Associates code paths (if applicable)

### 3. Query Knowledge Base

```bash
/wiki query What are the latest developments in AI?
/wiki query difference between LLM and GPT
```

After query, system **will suggest saving the answer to wiki** as an insight.

### 4. Health Check

```bash
/wiki lint
```

Checks:
- Orphan pages
- Missing links
- Index consistency
- Code path validity
- Knowledge graph completeness

### 5. Visualize Knowledge Graph

```bash
/wiki visualize
```

Generates interactive HTML graph with drag & zoom support.

---

## Command Reference

| Command | Description |
|---------|-------------|
| `/wiki init` | Initialize wiki structure |
| `/wiki init --path <dir>` | Initialize in custom directory |
| `/wiki ingest <file>` | Ingest document to wiki |
| `/wiki query <question>` | Query wiki |
| `/wiki lint` | Health check |
| `/wiki visualize` | Visualize knowledge graph |
| `/wiki status` | Show wiki status |
| `/wiki help` | Show help |

### Natural Language Triggers

- "initialize wiki" → init
- "ingest this document" → ingest
- "what do you know about xxx" → query
- "difference between xxx and yyy" → query
- "check wiki health" → lint
- "show knowledge graph" → visualize

---

## Directory Structure

### Default Location (User Home)

```
~/.openwiki/
├── raw/
│   ├── sources/           # Raw documents (immutable)
│   └── assets/            # Images, resources
├── wiki/
│   ├── entities/          # Entity pages
│   ├── concepts/          # Concept pages
│   ├── summaries/         # Document summaries
│   ├── synthesis/         # Synthesis analysis
│   └── comparisons/       # Comparison analysis
├── schema/
│   └── CLAUDE.md          # Wiki behavior rules
├── index.md               # Content index
└── log.md                 # Operation log
```

### Project Directory (Recommended)

```
your-project/
├── src/                   # Project code
├── wiki/                  # Wiki directory (version controlled)
│   ├── raw/
│   ├── wiki/
│   ├── schema/
│   ├── index.md
│   └── log.md
├── .gitignore
└── README.md
```

---

## Page Format

### YAML Frontmatter

```yaml
---
title: Page Title
type: entity|concept|synthesis|comparison
tags: [tag1, tag2]
created: 2024-01-01
updated: 2024-01-15
code_paths:
  - path: src/main.ts
    type: module
    description: Entry file
related: [[entity-name]]
---
```

### Cross-References

```markdown
This is a reference to [[entities/john-doe]]
This is also a reference to [[concepts/llm]]
```

---

## Dependencies

- **No external dependencies** - Pure file system + LLM capability
- **Platform**: Claude Code, Codex, OpenCode

---

## Related Projects

- [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) - Original concept
- [gbrain](https://github.com/garrytan/gbrain) - Another knowledge base system

---

## License

MIT