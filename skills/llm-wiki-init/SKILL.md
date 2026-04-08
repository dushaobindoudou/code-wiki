---
name: llm-wiki:init
description: 初始化 LLM Wiki 目录结构到 ~/.openwiki
---

# llm-wiki:init

初始化维基目录结构。

## 用法

`/wiki init [--path <目录>]`

- 无参数：初始化到 `~/.openwiki`
- 有参数：初始化到指定目录

## 创建的目录结构

```
<维基路径>/
├── raw/
│   ├── sources/           # 原始文档
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

## 流程

1. 确定维基路径（默认 ~/.openwiki，或 --path 参数）
2. 创建所有目录
3. 生成 schema/CLAUDE.md（默认维基规范）
4. 生成初始 index.md（目录大纲）
5. 生成初始 log.md（带时间戳）
6. 确认成功

## Schema/CLAUDE.md 模板

```markdown
# LLM Wiki Agent 说明

## 角色
你是维基管理员，负责维护结构化、累积的知识库。

## 目录结构
- entities/ — 实体页（人物、地点、组织）
- concepts/ — 概念页（主题、理论）
- summaries/ — 源文档摘要
- synthesis/ — 综合分析
- comparisons/ — 对比分析

## 页面格式
- 顶级标题：[[页面名]]
- 所有页面必须包含 YAML frontmatter
- 跨引用：[[entities/名称]] 或 [[concepts/主题]]

## 摄取流程
1. 阅读源文档，提取关键实体和概念
2. 写摘要页，包含：来源、日期、要点
3. 更新相关实体/概念页（追加新信息）
4. 更新 index.md
5. 记录到 log.md

## 查询响应规则
- 必须引用相关页面 [[页面名]]
- 鼓励将探索结果存回维基
```

## 成功输出

显示创建的目录结构，确认维基已就绪。