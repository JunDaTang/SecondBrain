#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理临时文件
清理系统生成的临时文件和缓存
"""

import sys
from pathlib import Path

# 添加utils模块到路径
sys.path.append(str(Path(__file__).parent))
from utils import (
    get_project_root, 
    print_colored, 
    Colors
)

def cleanup_temp_files():
    """清理临时文件"""
    root = get_project_root()
    
    print_colored("清理临时文件...", Colors.YELLOW, "🧹")
    
    # 定义临时文件模式
    temp_patterns = [
        '*.tmp',
        '*.bak', 
        '*~',
        'Thumbs.db',
        '.DS_Store',
        '*.swp',
        '*.swo',
        '.tmp*'
    ]
    
    cleaned_count = 0
    
    # 递归查找临时文件
    for pattern in temp_patterns:
        for temp_file in root.rglob(pattern):
            try:
                # 跳过.git目录中的文件
                if '.git' in temp_file.parts:
                    continue
                    
                temp_file.unlink()
                print_colored(f"删除: {temp_file.name}", Colors.GRAY)
                cleaned_count += 1
            except Exception as e:
                print_colored(f"删除失败 {temp_file.name}: {e}", Colors.RED)
    
    # 清理空的__pycache__目录
    for pycache_dir in root.rglob('__pycache__'):
        try:
            if pycache_dir.is_dir() and not any(pycache_dir.iterdir()):
                pycache_dir.rmdir()
                print_colored(f"删除空目录: {pycache_dir.name}", Colors.GRAY)
                cleaned_count += 1
        except Exception as e:
            print_colored(f"删除目录失败 {pycache_dir.name}: {e}", Colors.RED)
    
    print_colored(f"清理完成，删除了 {cleaned_count} 个文件/目录", Colors.GREEN, "✅")

if __name__ == '__main__':
    cleanup_temp_files() 