---
name: llm-wiki:visualize
description: 可视化 LLM Wiki 知识图谱
---

# llm-wiki:visualize

可视化维基中文档与文档之间的关系（知识图谱）。

## 用法

`/wiki visualize`

- 自动扫描 ~/.openwiki
- 生成交互式 HTML 图谱
- 在浏览器中打开

`/wiki visualize --path <目录>`

- 指定维基路径

`/wiki visualize --no-open`

- 生成 HTML 但不打开浏览器

## 依赖

- Python 3
- D3.js (通过 CDN)

## 节点类型颜色

- 实体 (entities) = 蓝色
- 概念 (concepts) = 绿色
- 摘要 (summaries) = 橙色
- 综合 (synthesis) = 紫色
- 对比 (comparisons) = 青色

## 功能

- 力导向图布局
- 按类型着色
- 节点大小反映入度
- 悬停显示详情
- 支持拖拽、缩放

## 调用方式

在 Claude Code 中使用：
```
使用 Skill 工具调用: Skill(skill="llm-wiki:visualize")
```

或直接运行 CLI：
```bash
python tools/visualize/cli.py --path ~/.openwiki
```