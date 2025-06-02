#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找孤立笔记
找出没有被其他笔记链接的"孤岛"笔记
"""

import sys
from pathlib import Path

# 添加utils模块到路径
sys.path.append(str(Path(__file__).parent))
from utils import (
    get_project_root, 
    print_colored, 
    Colors, 
    find_markdown_files,
    extract_wiki_links
)

def find_orphaned_notes():
    """查找孤立笔记"""
    root = get_project_root()
    
    print_colored("孤立笔记 (没有被其他笔记链接):", Colors.RED, "🏝️")
    
    # 获取所有markdown文件
    all_files = find_markdown_files(root)
    
    if not all_files:
        print_colored("未找到任何markdown文件", Colors.GRAY, "📭")
        return
    
    # 收集所有被链接的文件名
    linked_files = set()
    
    for file in all_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                links = extract_wiki_links(content)
                for link in links:
                    linked_files.add(link.strip())
        except Exception as e:
            continue
    
    # 找出孤立笔记
    orphaned_files = []
    for file in all_files:
        # 检查文件名（不含扩展名）是否被链接
        basename = file.stem
        if basename not in linked_files:
            orphaned_files.append(file)
    
    if orphaned_files:
        for file in sorted(orphaned_files, key=lambda f: f.name):
            print_colored(file.name, Colors.YELLOW, "📄")
        
        print()
        print_colored(f"共发现 {len(orphaned_files)} 个孤立笔记", Colors.YELLOW)
    else:
        print_colored("没有发现孤立笔记", Colors.GREEN, "✅")

if __name__ == '__main__':
    find_orphaned_notes() 