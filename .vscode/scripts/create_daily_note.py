#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建今日笔记
自动创建今天的日记文件，如果已存在则直接打开
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加utils模块到路径
sys.path.append(str(Path(__file__).parent))
from utils import (
    get_project_root, 
    print_colored, 
    Colors, 
    create_file_with_content, 
    open_file_in_vscode
)

def create_daily_note():
    """创建今日笔记"""
    root = get_project_root()
    
    # 生成今日日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 文件路径
    inbox_dir = root / 'ZK' / '00-Inbox'
    file_path = inbox_dir / f'{today}.md'
    
    # 检查文件是否已存在
    if file_path.exists():
        print_colored(f"今日笔记已存在: {file_path.relative_to(root)}", Colors.YELLOW, "📄")
    else:
        # 创建笔记内容
        content = [
            f"# {today}",
            "",
            "## 今日任务",
            "",
            "- [ ] ",
            "",
            "## 收集箱",
            "",
            "",
            "",
            "## 笔记链接",
            "",
            "",
            "",
            "## 反思",
            "",
            ""
        ]
        
        # 创建文件
        if create_file_with_content(file_path, content):
            print_colored(f"已创建今日笔记: {file_path.relative_to(root)}", Colors.GREEN, "✅")
        else:
            print_colored("创建今日笔记失败", Colors.RED, "❌")
            return
    
    # 在VS Code中打开文件
    open_file_in_vscode(file_path)

if __name__ == '__main__':
    create_daily_note() 