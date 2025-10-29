#!/usr/bin/env python3
"""
批量检查所有Vue文件的TypeScript语法问题
"""

import re
import sys
from pathlib import Path

def extract_script_content(vue_file_path):
    """从Vue文件中提取<script>标签内容"""
    try:
        with open(vue_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None, f"读取文件失败: {e}"
    
    # 匹配<script>标签内容
    script_pattern = r'<script[^>]*>\s*(.*?)\s*</script>'
    matches = re.findall(script_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if matches:
        return matches[0], None
    return None, "未找到<script>标签"

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
    
    if not script_content:
        return errors
    
    # 检查是否有重复的键
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

def check_vue_file(vue_file_path):
    """检查单个Vue文件"""
    print(f"\n🔍 检查文件: {vue_file_path}")
    
    script_content, error = extract_script_content(vue_file_path)
    if error:
        print(f"   ⚠️  {error}")
        return True  # 没有<script>标签不是错误
    
    if not script_content:
        print("   ✅ 无<script>标签内容（可能是模板文件）")
        return True
    
    # 检查语法问题
    errors = check_syntax_issues(script_content)
    
    if errors:
        print("   ❌ 发现语法错误:")
        for error in errors:
            print(f"     - {error}")
        return False
    else:
        print("   ✅ 语法检查通过")
        return True

def main():
    src_dir = Path("src")
    vue_files = list(src_dir.rglob("*.vue"))
    
    if not vue_files:
        print("❌ 未找到Vue文件")
        return 1
    
    print(f"📁 找到 {len(vue_files)} 个Vue文件")
    
    all_passed = True
    for vue_file in vue_files:
        if not check_vue_file(vue_file):
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 所有Vue文件语法检查通过！")
        return 0
    else:
        print("❌ 部分Vue文件存在语法错误")
        return 1

if __name__ == "__main__":
    sys.exit(main())