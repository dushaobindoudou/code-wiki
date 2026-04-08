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