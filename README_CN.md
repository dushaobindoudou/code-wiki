# LLM Wiki Skill

> 基于 Karpathy 的 LLM Wiki 架构构建的个人/团队知识库系统

## 概述

LLM Wiki Skill 是一个用于构建个人/团队知识库的 Claude Code Skill。它采用 Karpathy 的 LLM Wiki 模式，创建一个位于用户和原始文档之间的结构化、累积的维基系统。

### 核心理念

知识不是每次查询时重新发现，而是在每次摄取时累积构建。

### 核心特性

- 🗂️ **结构化存储**：纯文件系统，无外部依赖
- 🔄 **增量摄取**：每次源文档摄取触达 10-15 个维基页面
- 🔗 **知识图谱**：实体关系、概念关系、代码路径关联
- 🌐 **中文优化**：完整的中文命令和自然语言触发
- 🔍 **智能查询**：带引用存回功能的问答系统
- 🧹 **健康检查**：孤儿页面、链接完整性、代码路径验证

---

## 快速开始

### 1. 初始化维基

```bash
# 使用默认位置 ~/.openwiki
/wiki init

# 在项目根目录下创建（推荐开发项目使用，便于提交到仓库）
/wiki init --path ./wiki

# 或指定自定义目录
/wiki init --path ~/my-wiki
/wiki 初始化
```

### 2. 摄取文档

```bash
/wiki ingest ~/documents/article.md
/wiki 摄取 ~/documents/notes.md
```

每次摄取会自动：
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

查询后，系统会**建议将答案存回维基**作为洞察。

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
│   ├── raw/
│   ├── wiki/
│   ├── schema/
│   ├── index.md
│   └── log.md
├── .gitignore
└── README.md
```

在项目内创建维基的好处：
- 可以将知识库与项目代码一起版本控制
- 团队成员共享项目知识
- 方便 CI/CD 集成

---

## 页面格式

### YAML Frontmatter

```yaml
---
title: 页面标题
type: entity|concept|synthesis|comparison
tags: [标签1, 标签2]
created: 2024-01-01
updated: 2024-01-15
code_paths:           # 代码关联（可选）
  - path: src/main.ts
    type: module
    description: 入口文件
related: [[entity-name]]
---
```

### 跨引用

```markdown
这是一个对 [[entities/john-doe]] 的引用
这也是对 [[concepts/llm]] 的引用
```

---

## 与项目文档集成

当维基目录包含以下文件时，LLM 会自动读取并遵循：

- **CLAUDE.md** - 项目级规范，定义维基结构和页面格式
- **AGENT.md** - 代理级规范，定义特定任务处理流程

---

## 最佳实践

### 项目内维基工作流

```bash
# 1. 在项目根目录创建维基
/wiki init --path ./wiki

# 2. 将 wiki 目录添加到 Git
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

### 图片处理

- 使用 Obsidian Web Clipper 获取文章
- 设置附件文件夹为 `raw/assets/`
- 使用 Ctrl+Shift+D 下载所有图片到本地

### Git 版本控制

```bash
cd your-project/wiki
git init
git add .
git commit -m "feat: 初始化项目维基"
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