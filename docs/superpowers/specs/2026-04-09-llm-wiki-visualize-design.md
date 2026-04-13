# LLM Wiki 可视化工具设计文档

**日期**: 2026-04-09

---

## 1. 概述

创建一个 CLI 工具，可视化展示 LLM Wiki 中文档与文档之间的关系（知识图谱）。

---

## 2. 架构设计

### 工具名称

`llm-wiki:visualize` 或作为 `llm-wiki` 主 skill 的子命令

### 技术方案

- **语言**: Python（轻量依赖）
- **输出**: 静态 HTML + JavaScript（使用 D3.js 力导向图）
- **数据源**: 实时扫描维基目录

---

## 3. 功能设计

### 3.1 命令

```bash
/wiki visualize           # 生成图谱并打开浏览器
/wiki visualize --path <dir>  # 指定维基路径
```

### 3.2 数据提取

从维基目录提取：
- **节点**: 所有 Markdown 文件
- **边**: 文件中的 `[[页面名]]` 引用
- **节点类型**: 根据文件路径判断（entities/concepts/summaries/synthesis/comparisons）

### 3.3 可视化

使用 D3.js 力导向图：
- 节点颜色区分类型
- 节点大小根据入度（被引用次数）
- 悬停显示页面摘要
- 点击跳转到源文件
- 支持拖拽、缩放

### 3.4 输出

- 生成临时 HTML 文件
- 自动在浏览器打开
- 关闭浏览器后自动清理临时文件

---

## 4. 文件结构

```
tools/
└── visualize/
    ├── visualize.py      # 主脚本
    └── template.html     # HTML 模板（D3.js）
```

---

## 5. 验收标准

1. 扫描维基目录，列出所有页面
2. 提取页面间的 `[[引用]]` 关系
3. 生成交互式 HTML 图谱
4. 节点按类型着色（entities=蓝，concepts=绿，summaries=橙，synthesis=紫，comparisons=青）
5. 自动在浏览器打开