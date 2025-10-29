#!/usr/bin/env python3
"""
TypeScript语法检查脚本
用于验证Vue组件的TypeScript语法是否正确
"""

import re
import sys
from pathlib import Path

def extract_script_content(vue_file_path):
    """从Vue文件中提取<script>标签内容"""
    with open(vue_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配<script>标签内容
    script_pattern = r'<script[^>]*>\s*(.*?)\s*</script>'
    matches = re.findall(script_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if matches:
        return matches[0]
    return None

def check_duplicate_keys(script_content):
    """检查JavaScript对象中的重复键"""
    # 查找对象定义
    object_pattern = r'\w+\s*:\s*\{[^}]*\}'
    objects = re.findall(object_pattern, script_content)
    
    errors = []
    
    for obj in objects:
        # 提取键值对
        key_value_pattern = r'(\w+)\s*:\s*[^,}\n]+'
        key_values = re.findall(key_value_pattern, obj)
        
        # 检查重复键
        seen_keys = set()
        for key in key_values:
            if key in seen_keys:
                errors.append(f"重复的键: '{key}'")
            seen_keys.add(key)
    
    return errors

def check_syntax_issues(script_content):
    """检查常见的语法问题"""
    errors = []
    
    # 检查是否有重复的键（这是之前导致错误的原因）
    duplicate_errors = check_duplicate_keys(script_content)
    errors.extend(duplicate_errors)
    
    # 检查是否有未闭合的括号
    open_braces = script_content.count('{')
    close_braces = script_content.count('}')
    if open_braces != close_braces:
        errors.append(f"括号不匹配: 开括号 {open_braces}, 闭括号 {close_braces}")
    
    # 检查是否有未闭合的引号
    single_quotes = script_content.count("'")
    double_quotes = script_content.count('"')
    if single_quotes % 2 != 0:
        errors.append("单引号不匹配")
    if double_quotes % 2 != 0:
        errors.append("双引号不匹配")
    
    return errors

def main():
    vue_file = Path("src/components/ChartsView.vue")
    
    if not vue_file.exists():
        print(f"❌ 文件不存在: {vue_file}")
        return 1
    
    print(f"🔍 检查文件: {vue_file}")
    
    script_content = extract_script_content(vue_file)
    if not script_content:
        print("❌ 未找到<script>标签内容")
        return 1
    
    print("✅ 成功提取<script>标签内容")
    
    # 检查语法问题
    errors = check_syntax_issues(script_content)
    
    if errors:
        print("❌ 发现语法错误:")
        for error in errors:
            print(f"   - {error}")
        return 1
    else:
        print("✅ 未发现明显的语法错误")
        
        # 检查是否修复了重复键的问题
        if "trakt: 'Trakt'" in script_content:
            # 统计trakt出现的次数
            trakt_count = script_content.count("trakt: 'Trakt'")
            if trakt_count > 1:
                print(f"⚠️  发现重复的'trakt'键，出现次数: {trakt_count}")
                return 1
            else:
                print("✅ 重复键问题已修复")
        
        return 0

if __name__ == "__main__":
    sys.exit(main())