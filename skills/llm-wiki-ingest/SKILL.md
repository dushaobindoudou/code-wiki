---
name: llm-wiki:ingest
description: 将源文档摄取到 LLM Wiki，每次触达 10-15 个页面
---

# llm-wiki:ingest

将源文档摄取到维基。每次摄取应触达 10-15 个 wiki 页面，确保知识的充分关联。

## 用法

`/wiki ingest <文件>`

- 支持格式：TXT、MD（Markdown）、PDF（需先转换为文本）

## 前置条件

1. 维基已初始化（检查 ~/.openwiki 或 --path 是否存在）
2. 源文件存在且可读
3. 可选：检查 schema/CLAUDE.md 获取特定领域的格式规范

## 流程（10-15 页触达）

### 1. 验证维基存在

- 检查 ~/.openwiki 或 --path 参数
- 如果不存在，提示用户先运行 `/wiki init`
- 可选：读取 schema/CLAUDE.md 获取格式规范

### 2. 读取源文档

- 读取文件内容
- 提取：标题、内容、格式
- 如果存在 AGENT.md，遵循其中的处理规则

### 3. 生成摘要页

- 创建：`wiki/summaries/<slug>-<日期>.md`
- 包含：源文件、摄取日期、要点（3-5 条）
- 添加 YAML frontmatter

### 4. 提取并更新实体

- 识别实体（人物、地点、组织、项目）
- 每个实体：
  - 已存在：追加新信息
  - 不存在：在 `wiki/entities/` 创建新页面

### 4.5 更新实体关系（新增）

识别实体之间的关系：
- 人物与人物：同事、合作伙伴、竞争对手
- 人物与组织：创始人、员工、投资者
- 组织与组织：合作关系、竞争关系
- 项目与代码：包含关系、依赖关系

创建/更新：`wiki/entities/relations.md` 或在实体页添加 `relations` 字段

### 5. 提取并更新概念

- 识别概念（主题、理论、想法、技术）
- 每个概念：
  - 已存在：追加新信息
  - 不存在：在 `wiki/concepts/` 创建新页面

### 5.5 更新概念关系（新增）

识别概念之间的关系：
- 父子关系（上位概念/下位概念）
- 相关概念（相似、对立、因果）
- 技术栈关系（上下游、替代方案）

创建/更新：`wiki/concepts/relations.md` 或在概念页添加 `relations` 字段

### 6. 创建/更新综合页（synthesis）（新增）

当满足以下任一条件时，创建综合分析页：
- 已累计 5+ 个同主题实体
- 已有 3+ 个概念需要整合
- 用户指定需要综合
- 源文档包含多维度信息

位置：`wiki/synthesis/<主题>-<日期>.md`
内容：该主题的汇总分析，引用所有相关实体和概念

### 7. 检查是否需要对比页（新增）

当源文档包含以下内容时，创建对比分析：
- 两个或多个实体的对比（如：人物A vs 人物B）
- 两个或多个概念的对比（如：方法A vs 方法B）
- 同一领域的不同方案

位置：`wiki/comparisons/<对比主题>.md`
格式：使用 `||` 语法创建对比表

### 8. 代码路径关联（可选）

如果源文档涉及代码项目：
- 提取提到的文件路径、模块名、函数名
- 在实体或概念页添加 `code_paths` 字段：
  ```yaml
  code_paths:
    - path: src/utils/helper.ts
      type: module
      description: 工具函数模块
  ```
- 这允许知识图谱可视化时显示代码位置

### 9. 更新 index.md

- 添加新的摘要、实体、概念到索引
- 包含关系页（relations）更新
- 综合页、对比页也需要索引

### 10. 记录到 log.md

- 格式：`## [YYYY-MM-DD] ingest | <源文件> | 触达 X 页`

## 与项目文档集成

- **读取 schema/CLAUDE.md**：获取维基的格式规范
- **读取 AGENT.md**（如存在）：获取特定任务的处理规则
- **更新时保留现有 frontmatter**：不要覆盖已有的元数据

## 输出

显示本次摄取触达的页面列表：
- 创建：X 页
- 更新：Y 页
- 总计：Z 页（目标 10-15 页）

列出所有创建/更新的页面路径，例如：
```
📝 创建: wiki/summaries/article-2024-01-15.md
👤 更新: wiki/entities/john-doe.md
📂 更新: wiki/entities/relations.md
📚 更新: wiki/concepts/llm.md
🔗 更新: wiki/concepts/relations.md
📊 创建: wiki/synthesis/ai-trends-2024-01-15.md
📋 创建: wiki/comparisons/gpt-vs-claude.md
📑 更新: index.md
📝 更新: log.md

总计：10 页（目标达成 ✓）
```