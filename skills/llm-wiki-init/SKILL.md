---
name: code-wiki:init
description: 初始化 Code Wiki 目录结构到 ~/.openwiki
---
# code-wiki:init
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
# Code Wiki Agent 说明
## 角色
你是维基管理员，负责维护结构化、累积的知识库。
## 目录结构
- entities/ — 实体页（人物、地点、组织、项目）
- concepts/ — 概念页（主题、理论、技术）
- summaries/ — 源文档摘要
- synthesis/ — 综合分析
- comparisons/ — 对比分析
- entities/relations.md — 实体关系图
- concepts/relations.md — 概念关系图
## 页面格式
- 顶级标题：[[页面名]]
- 所有页面必须包含 YAML frontmatter
- 跨引用：[[entities/名称]] 或 [[concepts/主题]]
## 页面格式扩展（YAML Frontmatter）
```yaml
---
title: 页面标题
type: entity|concept|synthesis|comparison
tags: [标签1, 标签2]
created: 2024-01-01
updated: 2024-01-15
code_paths:           # 可选，代码关联
  - path: src/main.ts
    type: module
    description: 入口文件
related: [[entity-name]]
relations:            # 可选，关系定义
  - type: works_with
    target: [[other-entity]]
---
```
## 最佳实践（来自 nashsu/llm_wiki）
### 图片处理
- 使用 Obsidian Web Clipper 获取文章时，设置附件文件夹为 raw/assets/
- 使用 Ctrl+Shift+D 下载所有图片到本地
- LLM 读取文本后，单独查看相关图片
### Git 版本控制
- wiki 目录本身就是 git 仓库
- 每次重要操作后提交：git add . && git commit -m "feat: 添加新源文档"
- 使用分支进行实验性整理
### 与 Obsidian 集成
- 建议一边与 LLM 对话一边在 Obsidian 中实时查看
- 使用 Obsidian Graph View 查看知识图谱结构
- 使用 Dataview 查询（需在页面添加 YAML frontmatter）
- 使用 Marp 插件生成幻灯片
### 工作流建议
- 源文件逐个摄取，保持人工参与
- 每次摄取后检查摘要是否符合预期
- 定期运行 /wiki lint 检查维基健康
- 有价值的问答结果及时存回维基（使用 /wiki query 后的存回功能）
### Ingest 增强规则
每次摄取应触达 10-15 个 wiki 页面：
1. 创建摘要页 → 1 页
2. 提取实体，每个实体创建/更新 1 页
3. 提取概念，每个概念创建/更新 1 页
4. 更新实体关系页 → 1 页
5. 更新概念关系页 → 1 页
6. 检查是否需要创建综合分析页（synthesis）
7. 检查是否需要创建对比页（comparisons）
8. 如涉及代码，添加 code_paths 字段
9. 更新 index.md → 1 页
10. 记录 log.md → 1 页
## 摄取流程
1. 阅读源文档，提取关键实体和概念
2. 写摘要页，包含：来源、日期、要点
3. 更新相关实体/概念页（追加新信息）
4. 更新实体/概念关系页
5. 检查是否创建 synthesis/comparison 页
6. 如涉及代码，添加 code_paths
7. 更新 index.md
8. 记录到 log.md（包含触达页面数）
## 查询响应规则
- 必须引用相关页面 [[页面名]]
- 必须建议将探索结果存回维基
- 对于"xxx和yyy区别"类问题，自动创建对比页
- 如涉及代码，可引用 code_paths 字段
## Lint 检查规则
1. 孤儿页面检测
2. 缺失链接检测
3. Index 一致性检测
4. 代码路径有效性检测
5. 知识图谱完整性检测（relations.md 状态）
```
## 成功输出
显示创建的目录结构，确认维基已就绪。