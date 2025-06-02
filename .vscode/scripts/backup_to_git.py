#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备份到Git
快速提交所有更改到Git仓库
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
    is_git_repo,
    run_git_command
)

def backup_to_git():
    """备份到Git"""
    root = get_project_root()
    
    # 检查是否为Git仓库
    if not is_git_repo():
        print_colored("未找到Git仓库，请先运行: git init", Colors.RED, "❌")
        return
    
    # 添加所有文件
    success, output = run_git_command(['add', '.'])
    if not success:
        print_colored(f"Git add 失败: {output}", Colors.RED, "❌")
        return
    
    # 生成提交信息
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    commit_message = f"备份: {timestamp}"
    
    # 提交更改
    success, output = run_git_command(['commit', '-m', commit_message])
    if not success:
        if "nothing to commit" in output:
            print_colored("没有需要提交的更改", Colors.YELLOW, "📭")
        else:
            print_colored(f"Git commit 失败: {output}", Colors.RED, "❌")
        return
    
    print_colored("已备份到Git", Colors.GREEN, "✅")
    
    # 如果有远程仓库，询问是否推送
    success, remote_output = run_git_command(['remote', '-v'])
    if success and remote_output.strip():
        print_colored("检测到远程仓库，可以运行 'git push' 推送到远程", Colors.CYAN, "💡")

if __name__ == '__main__':
    backup_to_git() 