# LLM Wiki 可视化工具实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 CLI 工具，可视化展示 LLM Wiki 中文档与文档之间的关系（知识图谱）

**Architecture:** Python CLI 工具，生成 D3.js 交互式 HTML 图谱

**Tech Stack:** Python 3, D3.js (via CDN)

---

## 文件结构

```
tools/
└── visualize/
    ├── __init__.py
    ├── wiki_scanner.py   # 扫描维基目录，提取节点和边
    ├── html_generator.py # 生成 D3.js HTML 图谱
    ├── cli.py            # 命令行入口
    └── template.html     # HTML 模板（D3.js 力导向图）
```

---

### Task 1: 创建工具目录结构和基础 CLI

**Files:**
- Create: `tools/visualize/__init__.py`
- Create: `tools/visualize/cli.py`

- [ ] **Step 1: 创建目录和 __init__.py**

```python
# tools/visualize/__init__.py
"""LLM Wiki 可视化工具"""

__version__ = "0.1.0"
```

- [ ] **Step 2: 创建 CLI 入口**

```python
#!/usr/bin/env python3
"""LLM Wiki 可视化工具 CLI"""

import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        description="LLM Wiki 可视化工具 - 生成知识图谱"
    )
    parser.add_argument(
        "--path",
        default=os.path.expanduser("~/.openwiki"),
        help="维基目录路径 (默认: ~/.openwiki)"
    )
    parser.add_argument(
        "--output",
        default="/tmp/wiki-graph.html",
        help="输出 HTML 文件路径"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        default=True,
        help="自动在浏览器打开 (默认: True)"
    )
    args = parser.parse_args()

    wiki_path = args.path
    if not os.path.exists(wiki_path):
        print(f"错误: 维基目录不存在: {wiki_path}")
        print("请先运行 /wiki init 初始化维基")
        sys.exit(1)

    print(f"扫描维基目录: {wiki_path}")
    # TODO: 调用扫描器

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 测试 CLI 运行**

```bash
python tools/visualize/cli.py --help
```

Expected: 显示帮助信息

- [ ] **Step 4: Commit**

```bash
git add tools/visualize/
git commit -m "feat: create visualize tool basic structure"
```

---

### Task 2: 实现维基目录扫描器

**Files:**
- Create: `tools/visualize/wiki_scanner.py`

- [ ] **Step 1: 编写扫描器代码**

```python
#!/usr/bin/env python3
"""维基目录扫描器 - 提取节点和边"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple

# 匹配 [[页面名]] 引用
LINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')

# 目录到类型的映射
DIR_TYPE_MAP = {
    "entities": "entity",
    "concepts": "concept",
    "summaries": "summary",
    "synthesis": "synthesis",
    "comparisons": "comparison",
    "wiki/entities": "entity",
    "wiki/concepts": "concept",
    "wiki/summaries": "summary",
    "wiki/synthesis": "synthesis",
    "wiki/comparisons": "comparison",
}

def get_node_type(file_path: str, wiki_path: str) -> str:
    """根据文件路径判断节点类型"""
    rel_path = os.path.relpath(file_path, wiki_path)
    parts = rel_path.split(os.sep)

    if len(parts) >= 2:
        first_dir = parts[0]
        return DIR_TYPE_MAP.get(first_dir, "unknown")
    return "unknown"

def extract_links(content: str) -> List[str]:
    """从内容中提取 [[链接]]"""
    return LINK_PATTERN.findall(content)

def scan_wiki(wiki_path: str) -> Tuple[List[Dict], List[Dict]]:
    """
    扫描维基目录，返回节点和边

    Returns:
        (nodes, edges) - 节点列表和边列表
    """
    nodes = []
    edges = []
    node_ids = set()

    wiki_path = os.path.abspath(wiki_path)

    # 遍历所有 .md 文件
    for root, dirs, files in os.walk(wiki_path):
        # 跳过非维基目录
        if "raw/sources" in root or "raw/assets" in root:
            continue

        for filename in files:
            if not filename.endswith(".md"):
                continue
            if filename in ["index.md", "log.md"]:
                continue

            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, wiki_path)

            # 读取文件内容
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            # 提取元数据（标题）
            title = extract_title(content, filename)

            # 创建节点
            node_id = rel_path
            node_ids.add(node_id)

            node_type = get_node_type(file_path, wiki_path)
            node = {
                "id": node_id,
                "title": title,
                "type": node_type,
                "path": rel_path
            }
            nodes.append(node)

            # 提取链接，创建边
            links = extract_links(content)
            for link in links:
                # 转换链接为节点 ID
                target_id = link_to_node_id(link)
                edges.append({
                    "source": node_id,
                    "target": target_id
                })

    return nodes, edges

def extract_title(content: str, filename: str) -> str:
    """从内容中提取标题"""
    # 尝试从 YAML frontmatter 提取
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # 检查是否有 title 字段
            for line in parts[1].split("\n"):
                if line.startswith("title:"):
                    return line.split("title:", 1)[1].strip().strip('"').strip("'")

    # 从第一个 # 标题提取
    for line in content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()

    # 使用文件名
    return filename[:-3]

def link_to_node_id(link: str) -> str:
    """将 [[链接]] 转换为节点 ID"""
    # 处理不同格式的链接
    link = link.strip()

    # 如果包含路径，直接使用
    if "/" in link:
        return f"wiki/{link}.md"

    # 否则添加到对应类型目录
    # 默认添加到 concepts
    return f"wiki/concepts/{link}.md"

if __name__ == "__main__":
    import json
    wiki_path = os.path.expanduser("~/.openwiki")
    nodes, edges = scan_wiki(wiki_path)
    print(json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False, indent=2))
```

- [ ] **Step 2: 测试扫描器**

```bash
python -c "from tools.visualize.wiki_scanner import scan_wiki; nodes, edges = scan_wiki('/tmp/test-wiki'); print(f'Nodes: {len(nodes)}, Edges: {len(edges)}')"
```

Expected: 输出节点和边数量（如果维基不存在则报错）

- [ ] **Step 3: Commit**

```bash
git add tools/visualize/wiki_scanner.py
git commit -m "feat: add wiki scanner to extract nodes and edges"
```

---

### Task 3: 实现 HTML 生成器

**Files:**
- Create: `tools/visualize/html_generator.py`
- Create: `tools/visualize/template.html`

- [ ] **Step 1: 创建 HTML 模板**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Wiki 知识图谱</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            overflow: hidden;
        }
        #graph {
            width: 100vw;
            height: 100vh;
        }
        .node {
            cursor: pointer;
        }
        .node circle {
            stroke: #fff;
            stroke-width: 2px;
        }
        .node text {
            font-size: 12px;
            fill: #eee;
            pointer-events: none;
        }
        .link {
            stroke: #555;
            stroke-opacity: 0.6;
        }
        .tooltip {
            position: absolute;
            background: #16213e;
            border: 1px solid #0f3460;
            padding: 10px;
            border-radius: 5px;
            font-size: 12px;
            max-width: 300px;
            display: none;
        }
        .legend {
            position: absolute;
            top: 20px;
            right: 20px;
            background: #16213e;
            padding: 15px;
            border-radius: 8px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
        }
        .legend-color {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 8px;
        }
        #info {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: #16213e;
            padding: 15px;
            border-radius: 8px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div id="graph"></div>
    <div class="tooltip" id="tooltip"></div>
    <div class="legend">
        <div style="font-weight: bold; margin-bottom: 10px;">类型</div>
        <div class="legend-item"><div class="legend-color" style="background: #4fc3f7;"></div>实体 (entity)</div>
        <div class="legend-item"><div class="legend-color" style="background: #81c784;"></div>概念 (concept)</div>
        <div class="legend-item"><div class="legend-color" style="background: #ffb74d;"></div>摘要 (summary)</div>
        <div class="legend-item"><div class="legend-color" style="background: #ba68c8;"></div>综合 (synthesis)</div>
        <div class="legend-item"><div class="legend-color" style="background: #4dd0e1;"></div>对比 (comparison)</div>
    </div>
    <div id="info">
        <div>节点: <span id="node-count">0</span></div>
        <div>边: <span id="edge-count">0</span></div>
    </div>

    <script>
        const TYPE_COLORS = {
            "entity": "#4fc3f7",
            "concept": "#81c784",
            "summary": "#ffb74d",
            "synthesis": "#ba68c8",
            "comparison": "#4dd0e1",
            "unknown": "#999"
        };

        const data = __DATA__;

        const width = window.innerWidth;
        const height = window.innerHeight;

        const svg = d3.select("#graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        // 缩放
        const g = svg.append("g");
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => {
                g.attr("transform", event.transform);
            });
        svg.call(zoom);

        // 力学模拟
        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.edges).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(30));

        // 绘制边
        const link = g.append("g")
            .selectAll("line")
            .data(data.edges)
            .join("line")
            .attr("class", "link")
            .attr("stroke-width", 1.5);

        // 绘制节点
        const node = g.append("g")
            .selectAll("g")
            .data(data.nodes)
            .join("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        node.append("circle")
            .attr("r", d => 10 + Math.min(d.inDegree || 0, 5))
            .attr("fill", d => TYPE_COLORS[d.type] || TYPE_COLORS.unknown);

        node.append("text")
            .attr("dx", 15)
            .attr("dy", 4)
            .text(d => d.title);

        // 悬停提示
        const tooltip = d3.select("#tooltip");
        node.on("mouseover", (event, d) => {
            tooltip.style("display", "block")
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY + 10) + "px")
                .html(`
                    <strong>${d.title}</strong><br>
                    <span style="color: #888;">类型: ${d.type}</span><br>
                    <span style="color: #666;">${d.path}</span>
                `);
        })
        .on("mouseout", () => {
            tooltip.style("display", "none");
        });

        // 点击跳转
        node.on("click", (event, d) => {
            // 可以打开文件
            console.log("Clicked:", d.path);
        });

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        // 更新计数
        document.getElementById("node-count").textContent = data.nodes.length;
        document.getElementById("edge-count").textContent = data.edges.length;
    </script>
</body>
</html>
```

- [ ] **Step 2: 创建 HTML 生成器**

```python
#!/usr/bin/env python3
"""HTML 生成器 - 生成 D3.js 图谱"""

import os
import json

def generate_html(nodes: list, edges: list, output_path: str = "/tmp/wiki-graph.html"):
    """生成交互式 HTML 图谱"""
    template_path = os.path.join(os.path.dirname(__file__), "template.html")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 准备数据
    graph_data = {
        "nodes": [
            {
                "id": n["id"],
                "title": n["title"],
                "type": n["type"],
                "path": n["path"]
            }
            for n in nodes
        ],
        "edges": [
            {
                "source": e["source"],
                "target": e["target"]
            }
            for e in edges
        ]
    }

    # 替换数据
    html = template.replace("__DATA__", json.dumps(graph_data, ensure_ascii=False))

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path

if __name__ == "__main__":
    # 测试
    generate_html([], [], "/tmp/test-graph.html")
    print("Generated: /tmp/test-graph.html")
```

- [ ] **Step 3: 测试生成器**

```bash
python tools/visualize/html_generator.py
```

Expected: 生成测试 HTML 文件

- [ ] **Step 4: Commit**

```bash
git add tools/visualize/template.html tools/visualize/html_generator.py
git commit -m "feat: add HTML generator with D3.js visualization"
```

---

### Task 4: 集成 CLI 与扫描器、生成器

**Files:**
- Modify: `tools/visualize/cli.py`

- [ ] **Step 1: 更新 CLI 集成各模块**

```python
#!/usr/bin/env python3
"""LLM Wiki 可视化工具 CLI"""

import argparse
import os
import sys
import webbrowser
import tempfile

from wiki_scanner import scan_wiki
from html_generator import generate_html

def main():
    parser = argparse.ArgumentParser(
        description="LLM Wiki 可视化工具 - 生成知识图谱"
    )
    parser.add_argument(
        "--path",
        default=os.path.expanduser("~/.openwiki"),
        help="维基目录路径 (默认: ~/.openwiki)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="输出 HTML 文件路径 (默认: 临时文件)"
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="不在浏览器中打开"
    )
    args = parser.parse_args()

    wiki_path = os.path.abspath(os.path.expanduser(args.path))

    if not os.path.exists(wiki_path):
        print(f"错误: 维基目录不存在: {wiki_path}")
        print("请先运行 /wiki init 初始化维基")
        sys.exit(1)

    # 检查目录结构
    required_dirs = ["wiki", "schema"]
    missing = [d for d in required_dirs if not os.path.isdir(os.path.join(wiki_path, d))]
    if missing:
        print(f"警告: 目录不完整: {missing}")
        print("可能不是有效的维基目录")

    print(f"扫描维基目录: {wiki_path}")

    # 扫描
    try:
        nodes, edges = scan_wiki(wiki_path)
        print(f"找到 {len(nodes)} 个节点, {len(edges)} 条边")
    except Exception as e:
        print(f"扫描失败: {e}")
        sys.exit(1)

    if not nodes:
        print("未找到任何页面，请先摄取文档")
        sys.exit(1)

    # 生成 HTML
    output_path = args.output
    if not output_path:
        output_path = os.path.join(tempfile.gettempdir(), "wiki-graph.html")

    generate_html(nodes, edges, output_path)
    print(f"已生成图谱: {output_path}")

    # 打开浏览器
    if not args.no_open:
        print("正在打开浏览器...")
        webbrowser.open(f"file://{output_path}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 测试完整流程**

```bash
# 创建测试维基
mkdir -p /tmp/test-wiki/wiki/entities /tmp/test-wiki/wiki/concepts

# 创建测试文件
echo "# 张三

人物介绍页，引用 [[李四]] 和 [[AI]]" > /tmp/test-wiki/wiki/entities/zhangsan.md
echo "# 李四

另一个实体页" > /tmp/test-wiki/wiki/entities/lisi.md
echo "# AI

人工智能概念，引用 [[机器学习]]" > /tmp/test-wiki/wiki/concepts/ai.md
echo "# 机器学习

ML 概念" > /tmp/test-wiki/wiki/concepts/ml.md

# 运行
python tools/visualize/cli.py --path /tmp/test-wiki
```

Expected: 生成图谱并在浏览器打开

- [ ] **Step 3: Commit**

```bash
git add tools/visualize/cli.py
git commit -m "feat: integrate CLI with scanner and generator"
```

---

### Task 5: 添加 llm-wiki:visualize Skill

**Files:**
- Create: `tools/visualize/SKILL.md` (在 skills 目录)

- [ ] **Step 1: 创建 visualize skill**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add tools/visualize/SKILL.md
git commit -m "feat: add llm-wiki:visualize skill"
```

---

### Task 6: 测试无维基目录情况

- [ ] **Step 1: 测试目录不存在**

```bash
python tools/visualize/cli.py --path /tmp/non-existent
```

Expected: 错误信息 "维基目录不存在"

- [ ] **Step 2: 测试空维基**

```bash
mkdir /tmp/empty-wiki
python tools/visualize/cli.py --path /tmp/empty-wiki
```

Expected: 提示 "未找到任何页面"

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "test: add error handling tests"
```

---

## Spec 覆盖检查

| Spec 要求 | Task |
|-----------|------|
| 扫描维基目录，列出所有页面 | Task 2 |
| 提取 [[引用]] 关系 | Task 2 |
| 生成 D3.js HTML 图谱 | Task 3 |
| 节点按类型着色 | Task 3 |
| 自动打开浏览器 | Task 4 |

---

## 执行

计划完成并已保存。

**两个执行选项：**

**1. Subagent-Driven (推荐)** - 逐任务派遣子代理，任务间审查，快速迭代

**2. Inline Execution** - 同一会话中执行，执行计划，批量执行带检查点

**选择哪种方式？**