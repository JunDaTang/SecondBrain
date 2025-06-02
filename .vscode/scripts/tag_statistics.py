#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签统计
统计所有笔记中标签的使用频率
"""

import sys
from pathlib import Path
from collections import Counter

# 添加utils模块到路径
sys.path.append(str(Path(__file__).parent))
from utils import (
    get_project_root, 
    print_colored, 
    Colors, 
    find_markdown_files,
    extract_tags_from_content
)

def tag_statistics():
    """标签统计"""
    root = get_project_root()
    
    print_colored("标签使用统计:", Colors.GREEN, "🏷️")
    
    # 获取所有markdown文件
    all_files = find_markdown_files(root)
    
    if not all_files:
        print_colored("未找到任何markdown文件", Colors.GRAY, "📭")
        return
    
    # 收集所有标签
    all_tags = []
    
    for file in all_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                tags = extract_tags_from_content(content)
                all_tags.extend(tags)
        except Exception as e:
            continue
    
    if not all_tags:
        print_colored("未找到标签", Colors.GRAY, "📭")
        return
    
    # 统计标签频率
    tag_counter = Counter(all_tags)
    
    # 按使用频率排序显示
    for tag, count in tag_counter.most_common():
        print_colored(f"#{tag}: {count}次", Colors.CYAN)
    
    print()
    print_colored(f"共发现 {len(tag_counter)} 个不同标签，总使用 {len(all_tags)} 次", Colors.BLUE)

if __name__ == '__main__':
    tag_statistics() 