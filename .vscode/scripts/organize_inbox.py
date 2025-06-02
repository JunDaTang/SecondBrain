#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整理收集箱
查看收集箱中的所有文件及其创建时间，提供整理建议
"""

import sys
from pathlib import Path

# 添加utils模块到路径
sys.path.append(str(Path(__file__).parent))
from utils import (
    get_project_root, 
    print_colored, 
    Colors, 
    format_file_age
)

def organize_inbox():
    """整理收集箱"""
    root = get_project_root()
    inbox_dir = root / 'ZK' / '00-Inbox'
    
    print_colored("收集箱文件列表:", Colors.GREEN, "🗂️")
    
    # 查找所有md文件
    md_files = list(inbox_dir.glob('*.md'))
    
    if not md_files:
        print_colored("收集箱为空", Colors.GRAY, "📭")
    else:
        # 按修改时间排序（最新的在前）
        md_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        for file in md_files:
            age = format_file_age(file)
            print_colored(f"{file.name} ({age})", Colors.YELLOW, "📄")
    
    print()
    print_colored("💡 建议：定期将收集箱内容归类到 10-Literature 或 20-Permanent", Colors.CYAN)

if __name__ == '__main__':
    organize_inbox() 