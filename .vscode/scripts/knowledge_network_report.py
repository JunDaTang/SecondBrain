#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识网络报告
生成知识库的统计报告，分析笔记连接性
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
    extract_wiki_links
)

def knowledge_network_report():
    """生成知识网络报告"""
    root = get_project_root()
    
    print_colored("知识网络统计:", Colors.GREEN, "📊")
    
    # 获取所有markdown文件
    all_files = find_markdown_files(root)
    
    if not all_files:
        print_colored("未找到任何markdown文件", Colors.GRAY, "📭")
        return
    
    total_files = len(all_files)
    total_links = 0
    backlinks_count = Counter()
    
    # 分析每个文件的链接
    for file in all_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                links = extract_wiki_links(content)
                total_links += len(links)
                
                # 统计被链接的文件
                for link in links:
                    backlinks_count[link.strip()] += 1
                    
        except Exception as e:
            continue
    
    # 显示基础统计
    print_colored(f"总笔记数: {total_files}", Colors.CYAN, "📄")
    print_colored(f"总链接数: {total_links}", Colors.CYAN, "🔗")
    
    if total_files > 0:
        avg_links = round(total_links / total_files, 2)
        print_colored(f"平均每篇: {avg_links} 个链接", Colors.CYAN, "📊")
    
    print()
    
    # 显示热门笔记（被链接最多的）
    print_colored("热门笔记 (被链接最多):", Colors.YELLOW, "🔥")
    
    if backlinks_count:
        top_notes = backlinks_count.most_common(5)
        for note, count in top_notes:
            print_colored(f"{note}: {count}次被引用", Colors.MAGENTA, "📌")
    else:
        print_colored("未找到链接", Colors.GRAY, "📭")
    
    print()
    
    # 连接性分析
    linked_notes = len(backlinks_count)
    orphan_count = total_files - linked_notes
    
    if linked_notes > 0:
        connectivity = round((linked_notes / total_files) * 100, 1)
        print_colored(f"连接性: {connectivity}% ({linked_notes}/{total_files} 个笔记被链接)", Colors.BLUE, "🕸️")
    
    if orphan_count > 0:
        print_colored(f"孤立笔记: {orphan_count} 个", Colors.YELLOW, "🏝️")
    
    # 网络健康度评估
    print()
    if connectivity >= 80:
        print_colored("网络健康度: 优秀 - 笔记连接紧密", Colors.GREEN, "💚")
    elif connectivity >= 60:
        print_colored("网络健康度: 良好 - 建议增加更多链接", Colors.YELLOW, "💛")
    elif connectivity >= 40:
        print_colored("网络健康度: 一般 - 需要加强笔记间的连接", Colors.YELLOW, "🧡")
    else:
        print_colored("网络健康度: 较差 - 建议重新组织笔记结构", Colors.RED, "❤️")

if __name__ == '__main__':
    knowledge_network_report() 