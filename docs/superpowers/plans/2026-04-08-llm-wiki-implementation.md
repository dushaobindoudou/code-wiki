# LLM Wiki Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a published LLM Wiki skill with 5 sub-skills for personal/team knowledge base management

**Architecture:** Main skill handles command routing, sub-skills implement individual operations. Wiki stored at `~/.openwiki` by default.

**Tech Stack:** Superpowers skill system (SKILL.md format)

---

## File Structure

```
skills/
├── llm-wiki/                    # Main entry skill
│   └── SKILL.md                 # Command routing
├── llm-wiki-init/              # Initialize wiki
│   └── SKILL.md
├── llm-wiki-ingest/            # Ingest documents
│   └── SKILL.md
├── llm-wiki-query/             # Query and chat
│   └── SKILL.md
├── llm-wiki-lint/              # Health checks
│   └── SKILL.md
└── llm-wiki-schema/            # Schema management (optional)
    └── SKILL.md
```

---

### Task 1: Create llm-wiki Main Skill (Command Routing)

**Files:**
- Create: `skills/llm-wiki/SKILL.md`

- [ ] **Step 1: Create the skill file**

```markdown
---
name: llm-wiki
description: LLM Wiki - personal/team knowledge base. Sub-commands: init, ingest, query, lint, schema.
---

# LLM Wiki Skill

A personal/team knowledge base built on Karpathy's LLM Wiki architecture.

## Commands

| Command | Sub-skill | Description |
|---------|-----------|-------------|
| `/wiki init` | llm-wiki:init | Initialize wiki at ~/.openwiki |
| `/wiki ingest <file>` | llm-wiki:ingest | Ingest a document into wiki |
| `/wiki query <question>` | llm-wiki:query | Query the wiki |
| `/wiki lint` | llm-wiki:lint | Health check |
| `/wiki status` | (built-in) | Show wiki status |
| `/wiki help` | (built-in) | Show help |

## Trigger Patterns

- "初始化维基" → llm-wiki:init
- "摄取" → llm-wiki:ingest
- "查询" / "分析" → llm-wiki:query
- "检查" / "健康" → llm-wiki:lint

## Wiki Location

Default: `~/.openwiki`
Override: `/wiki init --path <directory>`

## Architecture

This skill routes commands to sub-skills:
- Use Skill tool to invoke: `Skill(skill="llm-wiki:init")`, `Skill(skill="llm-wiki:ingest")`, etc.
```

- [ ] **Step 2: Verify skill format**

Check the skill has valid YAML frontmatter and markdown content.

- [ ] **Step 3: Commit**

```bash
git add skills/llm-wiki/SKILL.md
git commit -m "feat: add llm-wiki main skill with command routing"
```

---

### Task 2: Create llm-wiki:init Skill

**Files:**
- Create: `skills/llm-wiki-init/SKILL.md`

- [ ] **Step 1: Create the init skill**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add skills/llm-wiki-init/SKILL.md
git commit -m "feat: add llm-wiki:init skill for wiki initialization"
```

---

### Task 3: Create llm-wiki:ingest Skill

**Files:**
- Create: `skills/llm-wiki-ingest/SKILL.md`

- [ ] **Step 1: Create the ingest skill**

```markdown
---
name: llm-wiki:ingest
description: Ingest source documents into LLM Wiki
---

# llm-wiki:ingest

Ingest source documents into the wiki.

## Usage

`/wiki ingest <file>`

- Supported formats: TXT, MD (Markdown)

## Pre-requisites

1. Wiki must be initialized (check if ~/.openwiki or --path exists)
2. Source file must exist and be readable

## Process

1. **Validate wiki exists**
   - Check ~/.openwiki or --path argument
   - If not found, prompt user to run `/wiki init` first

2. **Read source document**
   - Read file content
   - Extract: title, content, format

3. **Generate summary page**
   - Create: `wiki/summaries/<slug>-<date>.md`
   - Include: source file, ingest date, key points (3-5 bullets)

4. **Extract and update entities**
   - Identify entities (people, places, organizations)
   - For each entity:
     - If exists: append new information
     - If not: create new page in `wiki/entities/`

5. **Extract and update concepts**
   - Identify concepts (topics, theories, ideas)
   - For each concept:
     - If exists: append new information
     - If not: create new page in `wiki/concepts/`

6. **Update index.md**
   - Add new summaries, entities, concepts to index

7. **Record to log.md**
   - Format: `## [YYYY-MM-DD] ingest | <source-file>`

## Output

- Show created/updated pages
- Confirm wiki updated
```

- [ ] **Step 2: Commit**

```bash
git add skills/llm-wiki-ingest/SKILL.md
git commit -m "feat: add llm-wiki:ingest skill for document ingestion"
```

---

### Task 4: Create llm-wiki:query Skill

**Files:**
- Create: `skills/llm-wiki-query/SKILL.md`

- [ ] **Step 1: Create the query skill**

```markdown
---
name: llm-wiki:query
description: Query and chat with LLM Wiki knowledge base
---

# llm-wiki:query

Query the wiki and generate answers.

## Usage

`/wiki query <question>`

Or simply ask a question directly - the skill detects query intent.

## Pre-requisites

Wiki must have content (at least one ingested document).

## Process

1. **Find relevant pages**
   - Read index.md to locate relevant sections
   - Identify which entities/concepts/summaries relate to the question

2. **Read relevant content**
   - Load referenced pages
   - Synthesize information

3. **Generate answer**
   - Answer in Markdown
   - Include citations: [[pagename]]
   - Offer to save exploration results back to wiki

4. **Optional: Save to wiki**
   - If user wants, create new page in appropriate directory
   - Update index.md
   - Record to log.md

## Output Formats

- Markdown (default)
- Comparison tables using `||` syntax
- Summary lists

## Response Rules

- MUST cite relevant pages [[pagename]]
- Encourage saving useful exploration results
- If wiki is empty, prompt to ingest documents first
```

- [ ] **Step 2: Commit**

```bash
git add skills/llm-wiki-query/SKILL.md
git commit -m "feat: add llm-wiki:query skill for wiki queries"
```

---

### Task 5: Create llm-wiki:lint Skill

**Files:**
- Create: `skills/llm-wiki-lint/SKILL.md`

- [ ] **Step 1: Create the lint skill**

```markdown
---
name: llm-wiki:lint
description: Health check for LLM Wiki
---

# llm-wiki:lint

Health check for the wiki.

## Usage

`/wiki lint`

## Pre-requisites

Wiki must be initialized.

## Checks Performed

1. **Orphan pages**
   - Find pages with no inbound links
   - List orphaned entities/concepts

2. **Missing links**
   - Find mentioned concepts without dedicated pages
   - Suggest creating new concept pages

3. **Empty sections**
   - Find empty entity/concept directories
   - Flag for review

4. **Index consistency**
   - Verify index.md matches actual content
   - List discrepancies

5. **Log format**
   - Verify log.md entries are properly formatted

## Output

Report each check result with:
- Status: ✅ pass / ⚠️ warning / ❌ error
- Details
- Suggested fixes (if any)

## Auto-fix Options

After showing results, offer to:
- Remove orphan pages
- Create missing concept pages
- Rebuild index
```

- [ ] **Step 2: Commit**

```bash
git add skills/llm-wiki-lint/SKILL.md
git commit -m "feat: add llm-wiki:lint skill for health checks"
```

---

### Task 6: Create llm-wiki:schema Skill (Optional)

**Files:**
- Create: `skills/llm-wiki-schema/SKILL.md`

- [ ] **Step 1: Create the schema skill**

```markdown
---
name: llm-wiki:schema
description: Manage LLM Wiki behavior rules (CLAUDE.md)
---

# llm-wiki:schema

Manage the wiki's behavior rules.

## Usage

- `/wiki schema show` - Display current schema
- `/wiki schema edit` - Edit schema (opens in editor)

## Pre-requisites

Wiki must be initialized.

## Commands

### show
Display current schema/CLAUDE.md content.

### edit
Open schema/CLAUDE.md in editor for modification.
After save, confirm the schema is valid.

## Schema Location

`<wiki-path>/schema/CLAUDE.md`
```

- [ ] **Step 2: Commit**

```bash
git add skills/llm-wiki-schema/SKILL.md
git commit -m "feat: add llm-wiki:schema skill for schema management"
```

---

### Task 7: Integration Test

**Files:**
- Integration test in worktree

- [ ] **Step 1: Initialize test wiki**

Run `/wiki init --path /tmp/test-wiki` in a test scenario.

- [ ] **Step 2: Test ingest**

Create a sample.txt and run `/wiki ingest /tmp/sample.txt --path /tmp/test-wiki`.

- [ ] **Step 3: Test query**

Run `/wiki query what is this about?` with the test wiki.

- [ ] **Step 4: Test lint**

Run `/wiki lint` with the test wiki.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "test: integration test completed"
```

---

## Spec Coverage Check

| Spec Requirement | Task |
|-----------------|------|
| llm-wiki 主入口 + 命令路由 | Task 1 |
| init 初始化目录结构 | Task 2 |
| ingest 摄取文档 | Task 3 |
| query 查询对话 | Task 4 |
| lint 健康检查 | Task 5 |
| schema 管理（可选）| Task 6 |
| 集成测试 | Task 7 |

---

## Execution

Plan complete and saved.

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**