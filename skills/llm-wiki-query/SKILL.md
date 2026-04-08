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