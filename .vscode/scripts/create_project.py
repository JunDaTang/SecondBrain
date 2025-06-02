#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速创建项目
交互式创建新项目文件夹和模板
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
from template_parser import generate_content_from_template

def create_project():
    """创建新项目"""
    root = get_project_root()
    
    # 获取项目名称
    try:
        project_name = input("项目名称: ").strip()
        if not project_name:
            print_colored("项目名称不能为空", Colors.RED, "❌")
            return
    except KeyboardInterrupt:
        print_colored("\n已取消创建项目", Colors.YELLOW, "🚫")
        return
    
    # 创建项目目录
    project_dir = root / 'PARA' / '01_Projects' / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # 使用项目模板生成内容
    try:
        user_inputs = {"项目名称": project_name}
        content = generate_content_from_template('/para-project', user_inputs, interactive=False)
    except Exception as e:
        print_colored(f"生成模板失败: {e}", Colors.RED, "❌")
        return
    
    # 创建index.md文件
    index_file = project_dir / 'index.md'
    
    if create_file_with_content(index_file, content):
        relative_path = project_dir.relative_to(root)
        print_colored(f"项目已创建: {relative_path}", Colors.GREEN, "✅")
        
        # 在VS Code中打开文件
        open_file_in_vscode(index_file)
    else:
        print_colored("创建项目失败", Colors.RED, "❌")

if __name__ == '__main__':
    create_project() 