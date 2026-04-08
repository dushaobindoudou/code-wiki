# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an LLM Wiki skill project - a personal/team knowledge base system built on Karpathy's LLM Wiki architecture. The goal is to create a publicly released skill that helps users build and maintain a structured, accumulating knowledge base using Claude Code.

## Architecture

The skill uses a main skill + sub-skill pattern:

```
llm-wiki (main entry)
├── llm-wiki:init       # Initialize wiki structure
├── llm-wiki:ingest     # Ingest source documents
├── llm-wiki:query      # Query and chat
├── llm-wiki:lint       # Health checks
└── llm-wiki:schema    # Schema management (optional)
```

Wiki directory structure (user-specified or default `~/wiki`):
- `raw/sources/` - Original documents (immutable)
- `raw/assets/` - Images and resources
- `wiki/entities/` - Entity pages (people, places, organizations)
- `wiki/concepts/` - Concept pages (topics, theories)
- `wiki/summaries/` - Source document summaries
- `wiki/synthesis/` - Synthesis analyses
- `wiki/comparisons/` - Comparison analyses
- `schema/CLAUDE.md` - LLM wiki behavior rules
- `index.md` - Content index (auto-maintained)
- `log.md` - Operation log

## Key Files

- **Specification**: `docs/superpowers/specs/2026-04-08-llm-wiki-skill-design.md` - Full design document for this skill
- **Claude settings**: `.claude/settings.local.json` - Contains permissions for WebFetch and specific bash commands

## Current State

This project is in the design phase. The specification (`2026-04-08-llm-wiki-skill-design.md`) defines the complete architecture, but no implementation code exists yet.

## Commands

No build commands available yet - implementation not started.

To implement this project:
1. Read the spec at `docs/superpowers/specs/2026-04-08-llm-wiki-skill-design.md`
2. Use the writing-plans skill to create an implementation plan
3. Implement the skill following the plan