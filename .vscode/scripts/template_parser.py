#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板解析器
用于读取和处理 VS Code markdown.code-snippets 中的模板
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

def get_snippets_file_path() -> Path:
    """获取代码片段文件路径"""
    current_dir = Path(__file__).parent
    return current_dir.parent / 'markdown.code-snippets'

def load_snippets() -> Dict:
    """加载代码片段文件"""
    snippets_file = get_snippets_file_path()
    if not snippets_file.exists():
        raise FileNotFoundError(f"代码片段文件不存在: {snippets_file}")
    
    with open(snippets_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_vs_code_variables(text: str) -> str:
    """处理 VS Code 变量，替换为实际值"""
    now = datetime.now()
    
    # VS Code 变量映射
    variables = {
        '${CURRENT_YEAR}': now.strftime('%Y'),
        '${CURRENT_MONTH}': now.strftime('%m'),
        '${CURRENT_DATE}': now.strftime('%d'),
        '${CURRENT_HOUR}': now.strftime('%H'),
        '${CURRENT_MINUTE}': now.strftime('%M'),
        '${CURRENT_SECOND}': now.strftime('%S'),
    }
    
    # 替换变量
    for var, value in variables.items():
        text = text.replace(var, value)
    
    return text

def extract_placeholders(body: List[str]) -> Dict[int, Dict[str, str]]:
    """提取模板中的所有占位符信息"""
    placeholders = {}
    
    for line in body:
        # 查找 ${数字:描述} 格式的占位符
        matches = re.findall(r'\$\{(\d+):([^}]+)\}', line)
        for match in matches:
            index, description = match
            placeholders[int(index)] = {
                'type': 'input',
                'description': description,
                'default': ''
            }
        
        # 查找选择型占位符 ${数字|选项1,选项2,选项3|}
        choice_matches = re.findall(r'\$\{(\d+)\|([^}]+)\|\}', line)
        for match in choice_matches:
            index, choices = match
            choice_list = [choice.strip() for choice in choices.split(',')]
            placeholders[int(index)] = {
                'type': 'choice',
                'description': f'选择 ({"/".join(choice_list)})',
                'choices': choice_list,
                'default': choice_list[0] if choice_list else ''
            }
        
        # 查找简单占位符 $数字
        simple_matches = re.findall(r'\$(\d+)(?![:\|}])', line)
        for match in simple_matches:
            index = int(match)
            if index != 0 and index not in placeholders:  # $0 是结束符，跳过
                placeholders[index] = {
                    'type': 'input',
                    'description': f'输入项 {index}',
                    'default': ''
                }
    
    return placeholders

def collect_user_inputs(placeholders: Dict[int, Dict[str, str]], 
                        provided_inputs: Dict[str, str] = None) -> Dict[int, str]:
    """收集用户输入"""
    if provided_inputs is None:
        provided_inputs = {}
    
    user_values = {}
    
    # 按索引顺序处理占位符
    for index in sorted(placeholders.keys()):
        placeholder = placeholders[index]
        description = placeholder['description']
        placeholder_type = placeholder['type']
        
        # 首先检查是否在提供的输入中有匹配的值
        value = None
        for key, val in provided_inputs.items():
            if key.lower() in description.lower() or description.lower() in key.lower():
                value = val
                break
        
        # 如果没有找到匹配值，进行交互式输入
        if value is None:
            if placeholder_type == 'choice':
                choices = placeholder['choices']
                print(f"  [{index}] {description}")
                for i, choice in enumerate(choices, 1):
                    print(f"    {i}. {choice}")
                
                while True:
                    try:
                        choice_input = input(f"    请选择 (1-{len(choices)}, 默认: 1): ").strip()
                        if not choice_input:
                            value = choices[0]
                            break
                        choice_index = int(choice_input) - 1
                        if 0 <= choice_index < len(choices):
                            value = choices[choice_index]
                            break
                        else:
                            print(f"    请输入 1-{len(choices)} 之间的数字")
                    except ValueError:
                        print("    请输入有效的数字")
                    except KeyboardInterrupt:
                        value = choices[0]
                        break
            else:
                default = placeholder.get('default', '')
                prompt = f"  [{index}] {description}"
                if default:
                    prompt += f" (默认: {default})"
                prompt += ": "
                
                try:
                    user_input = input(prompt).strip()
                    value = user_input if user_input else default
                except KeyboardInterrupt:
                    value = default
        
        user_values[index] = value or ""
    
    return user_values

def process_template_placeholders(body: List[str], user_inputs: Dict[str, str] = None, 
                                interactive: bool = True) -> List[str]:
    """处理模板占位符"""
    # 提取所有占位符
    placeholders = extract_placeholders(body)
    
    # 收集用户输入
    if interactive and placeholders:
        print_colored = globals().get('print_colored', print)
        if callable(print_colored):
            print_colored("请填写模板参数:", "\033[96m", "📝")
        else:
            print("📝 请填写模板参数:")
        
        user_values = collect_user_inputs(placeholders, user_inputs)
    else:
        user_values = {}
        # 对于非交互模式，使用提供的输入或默认值
        for index, placeholder in placeholders.items():
            value = ""
            if user_inputs:
                # 尝试匹配输入
                for key, val in user_inputs.items():
                    if key.lower() in placeholder['description'].lower():
                        value = val
                        break
            user_values[index] = value or placeholder.get('default', f"[{placeholder['description']}]")
    
    # 处理模板内容
    processed_body = []
    for line in body:
        processed_line = line
        
        # 处理 VS Code 变量
        processed_line = process_vs_code_variables(processed_line)
        
        # 处理占位符
        def replace_indexed_placeholder(match):
            index = int(match.group(1))
            return user_values.get(index, "")
        
        # 处理各种格式的占位符
        processed_line = re.sub(r'\$\{(\d+):[^}]+\}', replace_indexed_placeholder, processed_line)
        processed_line = re.sub(r'\$\{(\d+)\|[^}]+\|\}', replace_indexed_placeholder, processed_line)
        processed_line = re.sub(r'\$(\d+)(?![:\|}])', replace_indexed_placeholder, processed_line)
        
        # 处理结束占位符 $0
        processed_line = processed_line.replace('$0', '')
        
        processed_body.append(processed_line)
    
    return processed_body

def get_template_by_prefix(prefix: str) -> Optional[Dict]:
    """根据前缀获取模板"""
    try:
        snippets = load_snippets()
        for name, snippet in snippets.items():
            if snippet.get('prefix') == prefix:
                return snippet
        return None
    except Exception as e:
        print(f"获取模板失败: {e}")
        return None

def generate_content_from_template(prefix: str, user_inputs: Dict[str, str] = None, 
                                 interactive: bool = True) -> List[str]:
    """根据模板前缀生成内容"""
    template = get_template_by_prefix(prefix)
    if not template:
        raise ValueError(f"未找到前缀为 '{prefix}' 的模板")
    
    body = template.get('body', [])
    return process_template_placeholders(body, user_inputs, interactive)

def get_available_templates() -> Dict[str, str]:
    """获取所有可用的模板"""
    try:
        snippets = load_snippets()
        templates = {}
        for name, snippet in snippets.items():
            prefix = snippet.get('prefix', '')
            description = snippet.get('description', name)
            templates[prefix] = description
        return templates
    except Exception as e:
        print(f"获取模板列表失败: {e}")
        return {}

if __name__ == '__main__':
    # 测试代码
    print("可用模板:")
    templates = get_available_templates()
    for prefix, desc in templates.items():
        print(f"  {prefix}: {desc}")
    
    print("\n生成基础模板:")
    try:
        user_inputs = {"标题": "测试笔记"}
        content = generate_content_from_template('/basic', user_inputs, interactive=False)
        for line in content:
            print(line)
    except Exception as e:
        print(f"生成失败: {e}") 