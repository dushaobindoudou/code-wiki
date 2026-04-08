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