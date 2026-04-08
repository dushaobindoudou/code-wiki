# LLM Wiki Skill 设计文档

**日期**: 2026-04-08
**基于**: Karpathy 的 LLM Wiki 架构 (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

---

## 1. 概述

创建一个公开发布的 skill，帮助用户基于 LLM Wiki 架构构建个人/团队知识库。

**核心特性**:
- 脚手架：快速初始化维基结构
- 运维命令：ingest / query / lint 等
- 知识管理：维护实体关系、跨引用、矛盾标记

**交互方式**: 混合式（命令 + 对话）
**存储**: 纯文件系统（Markdown + index.md）

---

## 2. 架构设计

### 2.1 Skill 结构

采用 **主 skill + 子 skill** 模式：

```
llm-wiki (主入口)
├── llm-wiki:init       # 初始化维基结构
├── llm-wiki:ingest     # 摄取源文档
├── llm-wiki:query      # 查询和对话
├── llm-wiki:lint       # 健康检查
└── llm-wiki:schema    # Schema 管理（可选）
```

### 2.2 目录结构

用户维基目录（用户指定或默认 `~/wiki`）：

```
wiki/
├── raw/                    # 原始文档（不可变）
│   ├── sources/           # 用户添加的源文档
│   └── assets/             # 图片等资源
├── wiki/                   # LLM 生成的维基内容
│   ├── entities/           # 实体页（人物、地点、组织等）
│   ├── concepts/          # 概念页（主题、理论等）
│   ├── summaries/         # 源文档摘要
│   ├── synthesis/         # 综合分析
│   ├── comparisons/      # 对比分析
│   └── overview.md       # 维基总览
├── schema/                 # 模式定义
│   └── CLAUDE.md         # LLM 维基行为规范
├── index.md               # 内容索引（自动维护）
└── log.md                 # 操作日志
```

### 2.3 关键文件格式

**index.md** 示例：

```markdown
# Wiki Index

## Entities
- [[entities/person-1]] — 人物描述摘要
- [[entities/org-1]] — 组织描述摘要

## Concepts
- [[concepts/ai]] — AI 概念汇总

## Sources
- [[summaries/article-2026-01]] — 源文档摘要
```

**log.md** 示例：

```markdown
## [2026-04-08] ingest | Article: LLM Wiki Pattern
## [2026-04-08] query | 什么是 LLM Wiki 的核心价值？
## [2026-04-08] lint | 健康检查完成，发现 2 个孤儿页面
```

---

## 3. 功能设计

### 3.1 llm-wiki:init

**功能**: 初始化维基目录结构

**交互**:
- 用户调用 `/wiki init` 或 "初始化我的维基"
- 可选参数：`--path <directory>` 指定维基目录
- 无参数时使用默认 `~/wiki`

**输出**:
- 创建上述目录结构
- 生成初始 `schema/CLAUDE.md`
- 生成初始 `index.md` 和 `log.md`

### 3.2 llm-wiki:ingest

**功能**: 摄取源文档到维基

**交互**:
- 用户调用 `/wiki ingest <file>` 或 "摄取这篇文章"
- 支持：Markdown、PDF、TXT、URL（需先下载）
- 对话模式：摄取后与用户确认关键要点

**处理流程**:
1. 读取源文档
2. 提取关键信息（实体、概念、要点）
3. 生成摘要页 (`summaries/`)
4. 更新相关实体页/概念页
5. 更新 `index.md`
6. 记录到 `log.md`

**约束**:
- 源文档放在 `raw/sources/`，永不修改
- 每次 ingest 至少更新 3+ 个维基页面

### 3.3 llm-wiki:query

**功能**: 查询维基并生成答案

**交互**:
- 用户调用 `/wiki query <question>` 或直接提问
- LLM 先查 `index.md` 定位相关页面
- 读取相关页面，综合答案
- 答案可选择存回维基（生成新页面）

**输出格式**:
- Markdown（默认）
- 对比表（使用 `||` 语法）
- 可选：Marp 幻灯片、matplotlib 图表

**特殊规则**:
- 好的答案必须包含引用 `[[page-name]]`
- 鼓励将探索结果存回维基

### 3.4 llm-wiki:lint

**功能**: 健康检查

**交互**:
- 用户调用 `/wiki lint` 或 "检查维基健康"

**检查项**:
1. 孤儿页面（无 inbound 链接）
2. 矛盾内容（同一概念的不同说法）
3. 过时信息（新源已覆盖但未更新）
4. 缺失链接（提到的概念无独立页面）
5. 数据缺口（可补充的问题/搜索方向）

**输出**:
- 问题列表及修复建议
- 可一键修复（LLM 自动处理）

### 3.5 llm-wiki:schema（可选）

**功能**: 管理/编辑维基的行为规范

**交互**:
- 用户调用 `/wiki schema edit` 修改 CLAUDE.md
- 用户调用 `/wiki schema show` 查看当前规范

---

## 4. Schema 设计 (CLAUDE.md)

维基的 CLAUDE.md 是让 LLM 正确扮演"维基管理员"角色的核心。包含：

```markdown
# LLM Wiki Agent Instructions

## 你的角色
你是维基管理员，负责维护一个结构化、知识累积的知识库。

## 目录结构规范
- entities/ — 实体页
- concepts/ — 概念页
- summaries/ — 源文档摘要
- ...

## 页面格式规范
- 顶级标题用 [[pagename]] 格式
- 所有页面必须包含 YAML frontmatter
- 跨引用使用 [[entities/name]] 或 [[concepts/topic]]

## Ingest 流程
1. 阅读源文档，提取关键实体和概念
2. 写摘要页，包含：来源、日期、关键要点
3. 更新相关实体/概念页（追加新信息）
4. 更新 index.md
5. 记录到 log.md

## Query 响应规范
- 必须引用相关页面 [[pagename]]
- 鼓励将探索结果存回维基

## Lint 检查清单
- 每次操作后检查 orphan links
- 标记矛盾内容用 > [!warning]
```

---

## 5. 命令路由设计

主 skill `llm-wiki` 负责命令路由：

```
/wiki init [--path <dir>]     → llm-wiki:init
/wiki ingest <file>           → llm-wiki:ingest
/wiki query <question>        → llm-wiki:query
/wiki lint                    → llm-wiki:lint
/wiki status                  → 显示维基状态
/wiki help                    → 显示帮助
```

对话触发：
- "初始化维基" → init
- "摄取这篇文档" → ingest
- "帮我分析xxx" → query
- "检查维基健康" → lint

---

## 6. 依赖和约束

- **无外部依赖**：纯文件系统 + LLM 能力
- **平台**：Claude Code, Codex, OpenCode（通用）
- **源文档格式**：Markdown, TXT, PDF, 纯文本
- **可选增强**：
  - `qmd` 搜索（大规模后）
  - Obsidian 集成（使用 Obsidian 作为 IDE）

---

## 7. 后续扩展

MVP 后可考虑：
- 多语言支持
- 导出为静态站点（GitHub Pages）
- 版本历史对比
- 多用户协作模式

---

## 8. 验收标准

1. 用户运行 `/wiki init` 能创建完整目录结构
2. 用户摄取一篇文档后，维基包含：摘要页 + 更新的实体/概念页 + index 更新 + log 记录
3. 用户提问能正确引用维基内容，且答案可存回维基
4. `/wiki lint` 能发现并修复至少 3 类问题
5. 多个子 skill 能独立工作，也可组合使用