---
name: llm-wiki
description: LLM Wiki - 个人/团队知识库。子命令：init, ingest, query, lint, schema。
---

# LLM Wiki Skill

基于 Karpathy 的 LLM Wiki 架构构建的个人/团队知识库。

## 命令

| 命令 | 子 Skill | 说明 |
|------|----------|------|
| `/wiki init` | llm-wiki:init | 初始化维基到 ~/.openwiki |
| `/wiki ingest <文件>` | llm-wiki:ingest | 摄取文档到维基 |
| `/wiki query <问题>` | llm-wiki:query | 查询维基 |
| `/wiki lint` | llm-wiki:lint | 健康检查 |
| `/wiki status` | (内置) | 显示维基状态 |
| `/wiki help` | (内置) | 显示帮助 |

## 触发模式

- "初始化维基" → llm-wiki:init
- "摄取" → llm-wiki:ingest
- "查询" / "分析" → llm-wiki:query
- "检查" / "健康" → llm-wiki:lint

## 维基位置

默认：`~/.openwiki`
自定义：`/wiki init --path <目录>`

## 架构

此 skill 负责将命令路由到子 skill：
- 使用 Skill 工具调用：`Skill(skill="llm-wiki:init")`、`Skill(skill="llm-wiki:ingest")` 等