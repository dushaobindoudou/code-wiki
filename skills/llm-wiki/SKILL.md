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