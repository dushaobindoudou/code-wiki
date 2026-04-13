---
name: code-wiki
description: Code Wiki - 个人/团队知识库（支持中文指令：初始化、摄取、查询、检查）。子命令：init, ingest, query, lint, schema, visualize。
---

# Code Wiki Skill

基于 Karpathy 的 Code Wiki 架构构建的个人/团队知识库。

## 命令（中文优化）

| 命令 | 子 Skill | 说明 |
|------|----------|------|
| `/wiki init` | code-wiki:init | 初始化维基到 ~/.openwiki |
| `/wiki 初始化` | code-wiki:init | 初始化维基 |
| `/wiki ingest <文件>` | code-wiki:ingest | 摄取文档到维基 |
| `/wiki 摄取 <文件>` | code-wiki:ingest | 摄取文档 |
| `/wiki query <问题>` | code-wiki:query | 查询维基 |
| `/wiki 查询 <问题>` | code-wiki:query | 查询维基 |
| `/wiki lint` | code-wiki:lint | 健康检查 |
| `/wiki 检查` | code-wiki:lint | 健康检查 |
| `/wiki visualize` | code-wiki:visualize | 可视化知识图谱 |
| `/wiki status` | (内置) | 显示维基状态 |
| `/wiki help` | (内置) | 显示帮助 |

## 触发模式（中文优化）

- "初始化维基" / "初始化wiki" / "建一个维基" → code-wiki:init
- "摄取" / "摄入" / "把xxx摄入" / "添加文档" → code-wiki:ingest
- "查询" / "问我xxx" / "关于xxx你知道什么" / "分析xxx" → code-wiki:query
- "检查" / "健康" / "维护" / "整理维基" → code-wiki:lint
- "可视化" / "图谱" / "知识图谱" → code-wiki:visualize
- "查看规范" / "wiki规则" → code-wiki:schema

## 维基位置

默认：`~/.openwiki`
自定义：`/wiki init --path <目录>`

**项目内创建（推荐开发项目使用）**：
```bash
/wiki init --path ./wiki
```
这样可以将维基创建在项目根目录下的 `wiki/` 文件夹，便于提交到代码仓库。

## 架构

此 skill 负责将命令路由到子 skill：
- 使用 Skill 工具调用：`Skill(skill="code-wiki:init")`、`Skill(skill="code-wiki:ingest")` 等

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