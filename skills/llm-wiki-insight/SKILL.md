---
name: code-wiki:insight
description: 手动创建洞察/综合分析页面（支持中文：洞察、综合）
---

# code-wiki:insight

手动创建洞察/综合分析页面，将有价值的见解存回维基。

## 用法

```bash
/wiki insight <主题>
/wiki synthesis <主题>
/wiki 综合 <主题>
/wiki 洞察 <主题>
```

## 触发模式

- "创建洞察" / "添加洞察" / "记录洞察" → insight
- "综合分析" / "创建综合" / "做综合" → insight
- "把xxx存回维基" → insight

## 流程

### 1. 确定主题

- 用户指定主题，或从之前对话中提取
- 检查是否已存在相关 synthesis 页面

### 2. 收集相关信息

从维基中收集：
- 相关实体页面
- 相关概念页面
- 相关 summaries
- 已有 comparisons（如有）

### 3. 生成洞察内容

**必须包含**：
- YAML frontmatter
- 主题标签
- 核心观点（3-5 条）
- 相关实体引用 [[entities/xxx]]
- 相关概念引用 [[concepts/xxx]]
- 引用来源（如有）

**可选包含**：
- 代码路径关联
- 时间线或演进分析
- 对比分析（可引用 comparisons/）

### 4. 写入文件

位置：`wiki/synthesis/<主题>-<日期>.md`

### 5. 更新 index.md

添加新洞察到索引。

## 洞察类型建议

| 类型 | 命名格式 | 说明 |
|------|----------|------|
| 分析类 | synthesis/analysis-<主题>-<日期> | 深度分析 |
| 总结类 | synthesis/summary-<主题>-<日期> | 主题总结 |
| 趋势类 | synthesis/trends-<主题>-<日期> | 趋势分析 |
| 教程类 | synthesis/guide-<主题>-<日期> | 操作指南 |

## 输出

```
✅ 洞察已创建：wiki/synthesis/<主题>-<日期>.md
📑 已更新：index.md
```

## 与 Query 集成

Query 回答后**必须**询问用户是否将答案存回维基：
- 用户同意 → 自动调用 insight skill
- 创建 synthesis 页面，包含问题、答案、引用来源