# Code Wiki

> A personal/team knowledge base system built on Karpathy's LLM Wiki pattern

[中文](#中文) | [English](#english)

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
/wiki 初始化
```

### 2. Ingest Documents

```bash
/wiki ingest ~/documents/article.md
/wiki 摄取 ~/documents/notes.md
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
/wiki 查询 LLM和GPT的区别
/wiki 分析这个项目的架构
```

After query, system **will suggest saving the answer to wiki** as an insight.

### 4. Health Check

```bash
/wiki lint
/wiki 检查
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

### Chinese Commands

| Command | Description |
|---------|-------------|
| `/wiki 初始化` | Initialize wiki |
| `/wiki 摄取 <file>` | Ingest document |
| `/wiki 查询 <question>` | Query wiki |
| `/wiki 检查` | Health check |

### Natural Language Triggers

- "initialize wiki" / "初始化维基" → init
- "ingest this document" / "摄取这篇文档" → ingest
- "what do you know about xxx" / "关于xxx你知道什么" → query
- "difference between xxx and yyy" / "xxx和yyy有什么区别" → query
- "check wiki health" / "检查维基健康" → lint
- "show knowledge graph" / "查看知识图谱" → visualize

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

### Project Directory (Recommended for Dev Projects)

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

Benefits of project wiki:
- Version control knowledge with project code
- Team collaboration on shared knowledge
- CI/CD integration support

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
code_paths:           # Code association (optional)
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

## Integration with Project Docs

When wiki directory contains these files, LLM will automatically read and follow:

- **CLAUDE.md** - Project-level rules, defines wiki structure and page format
- **AGENT.md** - Agent-level rules, defines specific task processing flows

---

## Best Practices

### Project Wiki Workflow

```bash
# 1. Create wiki in project root
/wiki init --path ./wiki

# 2. Add to Git
cd your-project
echo "wiki/.git" >> .gitignore
git add wiki/ .gitignore
git commit -m "feat: add project wiki"

# 3. Daily usage
/wiki ingest ./docs/design.md
/wiki query What is the project architecture?
/wiki lint

# 4. Commit wiki updates
git add wiki/
git commit -m "docs: update project knowledge base"
```

### Git Version Control

```bash
cd your-project/wiki
git init
git add .
git commit -m "feat: initialize project wiki"
```

### Workflow Suggestions

1. Ingest sources one at a time
2. Check summaries after each ingest
3. Run lint regularly
4. Save valuable Q&A results back to wiki
5. Commit wiki updates with project code

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

# 中文

## 概述

Code Wiki 是一个用于构建个人/团队知识库的 Claude Code Skill。它基于 Karpathy 的 LLM Wiki 模式，在用户和原始文档之间创建结构化、累积的维基系统。

**核心理念**：知识不是每次查询时重新发现，而是每次摄取时累积构建。

### 核心特性

- 🗂️ **结构化存储**：纯文件系统，无外部依赖
- 🔄 **增量摄取**：每次源文档摄取触达 10-15 个维基页面
- 🔗 **知识图谱**：实体关系、概念关系、代码路径关联
- 🌐 **中文优化**：完整的中文命令和自然语言触发
- 🔍 **智能查询**：带引用存回功能的问答系统
- 🧹 **健康检查**：孤儿页面、链接完整性、代码路径验证
- 📁 **项目集成**：支持在项目目录创建维基，便于版本控制

---

## 快速开始

### 1. 初始化维基

```bash
# 默认位置 ~/.openwiki
/wiki init

# 在项目根目录创建（推荐开发项目使用）
/wiki init --path ./wiki

# 指定自定义目录
/wiki init --path ~/my-wiki
/wiki 初始化
```

### 2. 摄取文档

```bash
/wiki ingest ~/documents/article.md
/wiki 摄取 ~/documents/notes.md
```

每次摄取自动执行：
- 创建摘要页
- 提取/更新实体（人物、组织、项目）
- 提取/更新概念
- 更新实体/概念关系
- 检查是否需要创建综合分析或对比页
- 关联代码路径（如涉及）

### 3. 查询知识库

```bash
/wiki query 关于AI的最新发展
/wiki 查询 LLM和GPT的区别
/wiki 分析这个项目的架构
```

查询后，系统**会建议将答案存回维基**作为洞察。

### 4. 健康检查

```bash
/wiki lint
/wiki 检查
```

检查项：
- 孤儿页面
- 缺失链接
- Index 一致性
- 代码路径有效性
- 知识图谱完整性

### 5. 可视化知识图谱

```bash
/wiki visualize
```

生成交互式 HTML 图谱，支持拖拽、缩放。

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `/wiki init` | 初始化维基结构 |
| `/wiki init --path <dir>` | 在指定目录创建维基 |
| `/wiki ingest <file>` | 摄取文档到维基 |
| `/wiki query <question>` | 查询维基 |
| `/wiki lint` | 健康检查 |
| `/wiki visualize` | 可视化知识图谱 |
| `/wiki status` | 显示维基状态 |
| `/wiki help` | 显示帮助 |

### 中文命令

| 命令 | 说明 |
|------|------|
| `/wiki 初始化` | 初始化维基结构 |
| `/wiki 摄取 <file>` | 摄取文档到维基 |
| `/wiki 查询 <question>` | 查询维基 |
| `/wiki 检查` | 健康检查 |

### 自然语言触发

- "初始化维基" → init
- "摄取这篇文档" → ingest
- "关于xxx你知道什么" → query
- "xxx和yyy有什么区别" → query
- "检查维基健康" → lint
- "查看知识图谱" → visualize

---

## 目录结构

### 默认位置（用户主目录）

```
~/.openwiki/
├── raw/
│   ├── sources/           # 原始文档（不可变）
│   └── assets/            # 图片、资源
├── wiki/
│   ├── entities/          # 实体页
│   ├── concepts/          # 概念页
│   ├── summaries/         # 文档摘要
│   ├── synthesis/         # 综合分析
│   └── comparisons/       # 对比分析
├── schema/
│   └── CLAUDE.md          # 维基行为规范
├── index.md               # 内容索引
└── log.md                 # 操作日志
```

### 项目内创建（推荐开发项目）

```
your-project/
├── src/                   # 项目代码
├── wiki/                  # 维基目录（可提交到仓库）
├── .gitignore
└── README.md
```

项目内创建的好处：
- 可将知识库与项目代码一起版本控制
- 团队成员共享项目知识
- 支持 CI/CD 集成

---

## 最佳实践

### 项目维基工作流

```bash
# 1. 在项目根目录创建维基
/wiki init --path ./wiki

# 2. 添加到 Git
cd your-project
echo "wiki/.git" >> .gitignore
git add wiki/ .gitignore
git commit -m "feat: 添加项目维基"

# 3. 日常使用
/wiki ingest ./docs/design.md
/wiki query 项目架构是什么
/wiki lint

# 4. 提交维基更新
git add wiki/
git commit -m "docs: 更新项目知识库"
```

### 工作流建议

1. 源文件逐个摄取
2. 每次摄取后检查摘要
3. 定期运行 lint 检查
4. 有价值的问答结果及时存回维基
5. 将维基更新与项目代码一起提交

---

## 依赖

- **无外部依赖** - 纯文件系统 + LLM 能力
- **平台**：Claude Code, Codex, OpenCode

---

## 相关项目

- [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) - 原始理念
 - 参考实现
- [gbrain](https://github.com/garrytan/gbrain) - 另一个知识库系统

---

## License

MIT