#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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