#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    "wiki": "unknown",  # 不单独处理 wiki 目录
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

    # 处理嵌套路径：wiki/entities/xxx.md
    if len(parts) >= 2:
        first_dir = parts[0]
        second_dir = parts[0] + "/" + parts[1] if len(parts) >= 2 else ""

        # 先检查完整路径
        if second_dir in DIR_TYPE_MAP:
            return DIR_TYPE_MAP[second_dir]
        # 再检查单层路径
        if first_dir in DIR_TYPE_MAP:
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

    # 第一遍：收集所有节点
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

    # 第二遍：提取链接，创建边（只保留有效引用）
    for root, dirs, files in os.walk(wiki_path):
        if "raw/sources" in root or "raw/assets" in root:
            continue

        for filename in files:
            if not filename.endswith(".md"):
                continue
            if filename in ["index.md", "log.md"]:
                continue

            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, wiki_path)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            # 提取链接，创建边
            links = extract_links(content)
            for link in links:
                # 转换链接为节点 ID
                target_id = link_to_node_id(link)
                # 只添加有效的边（目标节点存在）
                if target_id in node_ids:
                    edges.append({
                        "source": rel_path,
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
    link = link.strip()

    # 如果包含路径，直接使用
    if "/" in link:
        return f"wiki/{link}.md"

    # 否则添加到对应类型目录
    return f"wiki/concepts/{link}.md"

if __name__ == "__main__":
    import json
    wiki_path = os.path.expanduser("~/.openwiki")
    nodes, edges = scan_wiki(wiki_path)
    print(json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False, indent=2))