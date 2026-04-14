---
name: wiki:query
description: 查询 Code Wiki 知识库并对话，强化存回维基功能
---

# code-wiki:query

查询维基并生成答案。

## 用法

`/wiki query <问题>`

或直接提问 - skill 会自动识别查询意图。

## 触发模式（中文）

以下中文表达会触发 query：
- "关于xxx你知道什么"
- "给我分析一下xxx"
- "xxx 和 yyy 有什么区别"
- "总结一下xxx"
- "讲讲xxx"
- "对比一下xxx和yyy"
- "xxx的优缺点是什么"

## 前置条件

维基已有内容（至少已摄取一篇文档）。

## 流程

### 1. 查找相关页面

- 读取 index.md 定位相关章节
- 识别哪些实体/概念/摘要/synthesis/comparisons 与问题相关
- 可选：读取 schema/CLAUDE.md 获取特定领域的回答规范

### 2. 读取相关内容

- 加载引用的页面
- 综合信息
- 检查是否有相关的代码路径关联（code_paths）

### 3. 生成答案

- 用 Markdown 回答
- 包含引用：[[页面名]]
- **必须**询问："是否将这个答案存回维基作为洞察？"
- 如果用户同意，创建一个新的 synthesis 或 comparison 页面
- 如果用户的问题是"xxx和yyy区别"，自动建议创建对比页

### 4. 存回维基

如果用户同意存回：
- 在 `wiki/synthesis/` 创建分析页（分析类问题）
- 在 `wiki/comparisons/` 创建对比页（对比类问题）
- 在 `wiki/entities/` 或 `wiki/concepts/` 创建新页面（新实体/概念）
- 更新 index.md
- 记录到 log.md：`## [YYYY-MM-DD] query | <问题> | 存回维基`

## 存回维基的洞察类型

根据问题类型，建议创建：
- **分析类** → `synthesis/analysis-<主题>.md`
- **对比类** → `comparisons/<A>-vs-<B>.md`
- **人物类** → `entities/<人名>.md`（如是新人物）
- **概念类** → `concepts/<概念>.md`（如是新概念）
- **项目类** → `entities/<项目名>.md`（如涉及代码项目，添加 code_paths）

## 输出格式

- Markdown（默认）
- 对比表（使用 `||` 语法）
- 摘要列表
- 可选：Marp 幻灯片（`/wiki query --slides <问题>`）
- 可选：图表（matplotlib）

## 响应规则

- 必须引用相关页面 [[页面名]]
- **必须**建议将答案存回维基（不是可选，是必须）
- 如果维基为空，提示先摄取文档
- 对于"xxx和yyy区别"类问题，自动创建对比页并建议存回

## 与项目文档集成

- **读取 schema/CLAUDE.md**：获取维基的页面格式规范
- **读取 AGENT.md**（如存在）：获取特定查询类型的处理规则
- 如果问题涉及代码，可以引用 code_paths 字段中的路径