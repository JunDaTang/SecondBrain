#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识管理系统工具模块
提供彩色输出、文件操作等通用功能
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class Colors:
    """ANSI颜色代码"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(text: str, color: str = Colors.WHITE, emoji: str = "") -> None:
    """打印彩色文本"""
    if emoji:
        print(f"{emoji} {color}{text}{Colors.END}")
    else:
        print(f"{color}{text}{Colors.END}")

def get_project_root() -> Path:
    """获取项目根目录"""
    current = Path.cwd()
    # 寻找包含.vscode目录的父目录
    while current != current.parent:
        if (current / '.vscode').exists():
            return current
        current = current.parent
    return Path.cwd()

def find_markdown_files(directory: Path, exclude_dirs: List[str] = None) -> List[Path]:
    """查找所有markdown文件"""
    if exclude_dirs is None:
        exclude_dirs = ['Assets', '.git', '.vscode']
    
    md_files = []
    for md_file in directory.rglob('*.md'):
        # 检查是否在排除的目录中
        if not any(exclude_dir in md_file.parts for exclude_dir in exclude_dirs):
            md_files.append(md_file)
    
    return md_files

def extract_tags_from_content(content: str) -> List[str]:
    """从markdown内容中提取标签"""
    tags = []
    # 匹配YAML front matter中的tags
    yaml_match = re.search(r'tags:\s*\[([^\]]+)\]', content)
    if yaml_match:
        tag_list = yaml_match.group(1).split(',')
        for tag in tag_list:
            tag = tag.strip(' "\'')
            if tag:
                tags.append(tag)
    return tags

def extract_wiki_links(content: str) -> List[str]:
    """提取双向链接[[]]"""
    pattern = r'\[\[([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    return [match.strip() for match in matches]

def open_file_in_vscode(file_path: Path) -> None:
    """在VS Code当前窗口中打开文件"""
    try:
        subprocess.run(['code', '--reuse-window', str(file_path)], check=True)
    except subprocess.CalledProcessError:
        print_colored(f"无法打开文件: {file_path}", Colors.RED, "❌")
    except FileNotFoundError:
        print_colored("未找到VS Code命令，请确保VS Code已安装并添加到PATH", Colors.RED, "❌")

def create_file_with_content(file_path: Path, content: List[str]) -> bool:
    """创建文件并写入内容"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        return True
    except Exception as e:
        print_colored(f"创建文件失败: {e}", Colors.RED, "❌")
        return False

def format_file_age(file_path: Path) -> str:
    """格式化文件年龄显示"""
    try:
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        age = datetime.now() - mtime
        if age.days > 0:
            return f"{age.days}天前"
        elif age.seconds > 3600:
            hours = age.seconds // 3600
            return f"{hours}小时前"
        else:
            return "今天"
    except:
        return "未知"

def is_git_repo() -> bool:
    """检查是否为Git仓库"""
    return (get_project_root() / '.git').exists()

def run_git_command(command: List[str]) -> tuple[bool, str]:
    """执行Git命令"""
    try:
        result = subprocess.run(
            ['git'] + command,
            cwd=get_project_root(),
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
    except FileNotFoundError:
        return False, "Git未安装或不在PATH中" 