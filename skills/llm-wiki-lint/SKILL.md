---
name: llm-wiki:lint
description: LLM Wiki 健康检查，包括知识图谱一致性验证
---

# llm-wiki:lint

维基健康检查。

## 用法

`/wiki lint`

## 前置条件

维基已初始化。

## 检查项目

### 1. 孤儿页面

- 找出没有 inbound 链接的页面
- 列出孤立的实体/概念/summaries/synthesis/comparisons

### 2. 缺失链接

- 找出提到但没有独立页面的概念
- 建议创建新概念页

### 3. 空目录

- 找出空的 entities/concepts/summaries/synthesis/comparisons 目录
- 标记待检查

### 4. Index 一致性

- 验证 index.md 与实际内容匹配
- 列出差异

### 5. 日志格式

- 验证 log.md 条目格式正确
- 检查是否有触达页面数记录

### 6. 代码路径有效性（新增）

检查 entities/concepts 页中的 `code_paths` 字段：
- 路径是否存在（使用文件路径检查）
- 文件类型是否正确（.ts, .js, .py, .md 等）
- 标记失效的路径为警告

示例输出：
```
🔍 代码路径检查:
   ✅ wiki/entities/project-alpha.md: src/main.ts 存在
   ⚠️ wiki/concepts/auth.md: path: server/auth.js 不存在
```

### 7. 知识图谱完整性（新增）

- 检查 `wiki/entities/relations.md` 是否存在并更新
- 检查 `wiki/concepts/relations.md` 是否存在并更新
- 检查是否有实体/概念缺少关系定义
- 建议添加关系以增强图谱连通性
- 检查 code_paths 是否与对应代码文件实际关联

示例输出：
```
🕸️ 知识图谱完整性:
   ⚠️ wiki/entities/relations.md 不存在或为空
   ✅ 5 个实体已有关系定义
   ⚠️ 3 个概念缺少关系（concepts/llm, concepts/rag, concepts/agent）
```

## 输出

每项检查结果报告：
- 状态：✅ 通过 / ⚠️ 警告 / ❌ 错误
- 详情
- 修复建议（如有）

## 自动修复选项

显示结果后，询问是否：
- 删除孤儿页面
- 创建缺失的概念页面
- 重建索引
- 创建/更新 relations.md
- 清理失效的 code_paths
- 标记需要添加关系的实体/概念

## 与项目文档集成

- 如果维基目录包含 schema/CLAUDE.md，读取其中的格式规范
- 根据规范验证 YAML frontmatter 格式