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

---

## Hard Questions FAQ (User Perspective)

> This section answers the toughest questions: "Can I use this now?", "Why is it better?", and "What happens when it fails?"

### 1) Is it usable now? Can I get value in 10 minutes?

**Answer**: The current project is usable for Skill-level workflow demos (`init/ingest/query/lint/visualize`), but not yet a fully packaged production product.  
**How we address it**:
- Provide a fixed quick path: `/wiki init --path ./wiki` -> `/wiki ingest <file>` -> `/wiki query <question>` -> `/wiki lint`
- Add a minimal reproducible demo dataset with expected outputs

### 2) Why not just ask an LLM to make notes directly?

**Answer**: The key differentiation is **compounding structured knowledge**, not one-off answers:
- Persistent page taxonomy (entities/concepts/summaries/synthesis/comparisons)
- Explicit relation graph (entity/concept/code-path links)
- Query results can be saved back, so knowledge improves over time

### 3) How do you prove quality? Any benchmark?

**Answer**: No public benchmark is published yet; this is a known gap.  
**How we address it**:
- Build a small evaluation set (10-20 bilingual docs)
- Track core metrics: entity extraction precision, relation validity, citation coverage in answers, lint issue rate
- Run regression checks after rule changes

### 4) What about failures? Can it silently corrupt my wiki?

**Answer**: File-system-first storage gives auditability, but fault injection and rollback flow still need hardening.  
**How we address it**:
- Add pre-write checks, post-write lint, and structured failure logs
- Add page-level backup/snapshot strategy for critical writes
- Document a recovery runbook for conflicts/duplicates/format issues

### 5) What happens to old data when schema changes?

**Answer**: There is a schema entry point, but migration policy is still incomplete.  
**How we address it**:
- Add explicit schema versioning
- Define backward-compatibility windows and conversion rules
- Add a migration checklist (before/after validation)

### 6) How do teams avoid overwrite conflicts?

**Answer**: `./wiki` can already be version-controlled, but merge/conflict governance needs clearer standards.  
**How we address it**:
- Define naming/ownership conventions for pages
- Add PR checks for links, frontmatter validity, and conflict review
- Treat `lint` as a merge gate

### 7) What about privacy and security?

**Answer**: Local-first storage is good by default, but explicit redaction policy and processing boundary docs are still needed.  
**How we address it**:
- Add sensitive-data handling policy (PII/secrets/credentials)
- Add optional redaction before ingest
- Document model-processing boundaries and retention behavior

### 8) Why should I trust auto-generated relations?

**Answer**: No citation, no trust. Relations should be traceable or marked as low-confidence.  
**How we address it**:
- Prefer source-grounded citations in query/analysis outputs
- Mark low-confidence relations as "needs review"
- Add lint checks for unsupported core claims

### 9) Is Chinese/multilingual support really stable?

**Answer**: Chinese commands and docs are in place, but cross-lingual entity normalization is still an active improvement area.  
**How we address it**:
- Add mixed Chinese-English evaluation cases
- Build alias/term mapping (CN/EN/acronym)
- Show synonym mapping in query responses

### 10) Will maintenance collapse after a few months?

**Answer**: It will if there are no metrics and no automated gates.  
**How we address it**:
- Operationalize lint/link/integrity checks
- Define versioning cadence for rules/schema changes
- Keep runbooks and validation scripts as the source of truth

---

## 30-Day Gap-Closing Plan

### Week 1: Usability
- Ship a "10-minute happy path" demo
- Provide sample input + expected output
- Done criteria: a new user can complete the flow once without intervention

### Week 2: Quality Baseline
- Build a minimal bilingual evaluation set
- Define metrics and pass/fail thresholds
- Done criteria: one baseline report is produced and stored

### Week 3: Reliability & Recovery
- Add write guards, logs, and recovery docs
- Cover at least 3 common failure scenarios
- Done criteria: failures can be reproduced and recovered with documented steps

### Week 4: Collaboration & Governance
- Finalize schema version/migration policy
- Add team merge governance (`lint` gate + PR checklist)
- Done criteria: concurrent team changes merge cleanly with validated wiki integrity

---

## Release Mode And Testing

### Is this production-ready now?

This repository is now managed as **Docs/Skill GA** release mode.  
Definition: `docs/release/PRODUCTION-READINESS.md`

### How to run tests?

```bash
bash tools/qa/release-gate.sh
```

The script validates:
- Core file completeness
- README command coverage
- Main skill routing integrity

### Can this auto-update?

Yes. GitHub Actions workflow is included: `.github/workflows/release-gate.yml`

- `push/pull_request`: runs release gate checks automatically
- `schedule` (every Monday 01:00 UTC): runs checks and updates `docs/release/AUTO-UPDATE-HEARTBEAT.md`
- `workflow_dispatch`: manual trigger support