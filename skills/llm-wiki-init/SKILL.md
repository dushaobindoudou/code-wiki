---
name: code-wiki:init
description: 初始化 Code Wiki 目录结构（项目优先）
---

# code-wiki:init

初始化维基目录结构。

## 用法

```bash
/wiki init                    # 在当前项目 ./wiki 创建
/wiki init --path <目录>     # 指定目录创建
/wiki init --global          # 强制在 ~/.openwiki 创建
```

## 维基位置查找顺序

1. **当前目录 `./wiki`** - 优先
2. **上级目录 `../wiki`** - 次优先
3. **`~/.openwiki`** - 最后 fallback（仅当 --global 时才直接使用）

## 流程

### 1. 确定维基路径

```
如果指定 --path → 使用指定路径
否则如果 ./wiki 存在 → 使用 ./wiki
否则如果 ../wiki 存在 → 使用 ../wiki
否则如果 ~/.openwiki 存在 → 使用 ~/.openwiki
否则 → 创建 ./wiki（当前目录）
```

### 2. 创建目录结构

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

### 3. 生成默认文件

- `schema/CLAUDE.md` - 默认维基规范
- `index.md` - 目录大纲
- `log.md` - 带时间戳

### 4. 确认成功

显示创建的目录结构，确认维基已就绪。

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

## 页面格式
- 顶级标题：[[页面名]]
- 所有页面必须包含 YAML frontmatter
- 跨引用：[[entities/名称]] 或 [[concepts/主题]]
```

## 输出

显示创建的目录结构，确认维基已就绪。

例如：
```
✅ Code Wiki 已初始化

位置: /path/to/project/wiki/
├── raw/
│   ├── sources/
│   └── assets/
├── wiki/
│   ├── entities/
│   ├── concepts/
│   ├── summaries/
│   ├── synthesis/
│   └── comparisons/
├── schema/
│   └── CLAUDE.md
├── index.md
└── log.md
```