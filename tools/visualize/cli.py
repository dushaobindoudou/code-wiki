#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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