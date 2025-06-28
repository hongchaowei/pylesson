#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门添加DOCTYPE声明的脚本
"""

import os
import re

def add_doctype_to_file(file_path):
    """为HTML文件添加DOCTYPE声明"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有DOCTYPE声明
        if content.strip().startswith('<!DOCTYPE html>'):
            return False, "已有DOCTYPE声明"
        
        # 如果文件以<html开头，在前面添加DOCTYPE
        if content.strip().startswith('<html'):
            content = '<!DOCTYPE html>\n' + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "添加DOCTYPE声明"
        else:
            return False, "文件格式异常"
            
    except Exception as e:
        return False, f"错误: {e}"

def process_all_html_files(root_dir):
    """处理所有HTML文件"""
    html_files = []
    
    # 递归查找所有HTML文件
    for root, dirs, files in os.walk(root_dir):
        # 跳过py目录
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                html_files.append(file_path)
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    fixed_count = 0
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        was_fixed, message = add_doctype_to_file(file_path)
        
        if was_fixed:
            fixed_count += 1
            print(f"✓ 修复: {rel_path} - {message}")
        else:
            if "错误" in message:
                print(f"✗ 错误: {rel_path} - {message}")
            else:
                print(f"○ 跳过: {rel_path} - {message}")
    
    print(f"\n修复完成: 共修复 {fixed_count} 个文件")
    return fixed_count

if __name__ == "__main__":
    # 获取当前脚本所在目录的上级目录作为根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    print(f"开始添加DOCTYPE声明...")
    print(f"根目录: {root_dir}")
    print("=" * 50)
    
    # 执行修复
    fixed_count = process_all_html_files(root_dir)
    
    print("\n" + "=" * 50)
    print(f"总共修复了 {fixed_count} 个文件的DOCTYPE声明")