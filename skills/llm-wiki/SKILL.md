---
name: llm-wiki
description: LLM Wiki - 个人/团队知识库（支持中文指令：初始化、摄取、查询、检查）。子命令：init, ingest, query, lint, schema, visualize。
---

# LLM Wiki Skill

基于 Karpathy 的 LLM Wiki 架构构建的个人/团队知识库。

## 命令（中文优化）

| 命令 | 子 Skill | 说明 |
|------|----------|------|
| `/wiki init` | llm-wiki:init | 初始化维基到 ~/.openwiki |
| `/wiki 初始化` | llm-wiki:init | 初始化维基 |
| `/wiki ingest <文件>` | llm-wiki:ingest | 摄取文档到维基 |
| `/wiki 摄取 <文件>` | llm-wiki:ingest | 摄取文档 |
| `/wiki query <问题>` | llm-wiki:query | 查询维基 |
| `/wiki 查询 <问题>` | llm-wiki:query | 查询维基 |
| `/wiki lint` | llm-wiki:lint | 健康检查 |
| `/wiki 检查` | llm-wiki:lint | 健康检查 |
| `/wiki visualize` | llm-wiki:visualize | 可视化知识图谱 |
| `/wiki status` | (内置) | 显示维基状态 |
| `/wiki help` | (内置) | 显示帮助 |

## 触发模式（中文优化）

- "初始化维基" / "初始化wiki" / "建一个维基" → llm-wiki:init
- "摄取" / "摄入" / "把xxx摄入" / "添加文档" → llm-wiki:ingest
- "查询" / "问我xxx" / "关于xxx你知道什么" / "分析xxx" → llm-wiki:query
- "检查" / "健康" / "维护" / "整理维基" → llm-wiki:lint
- "可视化" / "图谱" / "知识图谱" → llm-wiki:visualize
- "查看规范" / "wiki规则" → llm-wiki:schema

## 维基位置

默认：`~/.openwiki`
自定义：`/wiki init --path <目录>`

## 架构

此 skill 负责将命令路由到子 skill：
- 使用 Skill 工具调用：`Skill(skill="llm-wiki:init")`、`Skill(skill="llm-wiki:ingest")` 等

## 与项目文档集成

当维基目录包含 `AGENT.md` 或 `CLAUDE.md` 时，LLM 会自动读取并遵循其中的规范：

- **CLAUDE.md**（项目级）：定义维基的整体结构、页面格式规范
- **AGENT.md**（代理级）：定义特定任务的处理流程
- **使用方式**：确保维基目录的 `schema/` 子目录包含这些文件，LLM 会自动加载

## 知识图谱代码关联

此 skill 支持将代码路径与维基实体关联：
- 在实体/概念页面添加 `code_paths` 字段
- 通过 `/wiki visualize` 可视化时显示代码位置
- Lint 检查会验证代码路径有效性