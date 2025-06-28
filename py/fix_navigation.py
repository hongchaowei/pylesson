#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复网站导航问题的脚本
自动为所有HTML页面添加导航栏和面包屑导航
"""

import os
import re
from pathlib import Path

def get_relative_path(file_path, target_dir):
    """计算相对路径"""
    file_path = Path(file_path)
    target_dir = Path(target_dir)
    
    # 计算从文件到目标目录的相对路径
    try:
        rel_path = os.path.relpath(target_dir, file_path.parent)
        return rel_path.replace('\\', '/')
    except ValueError:
        # 如果在不同驱动器上，返回绝对路径
        return str(target_dir).replace('\\', '/')

def fix_html_file(file_path, base_dir):
    """修复单个HTML文件的导航"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 计算相对路径
        css_path = get_relative_path(file_path, os.path.join(base_dir, 'css'))
        js_path = get_relative_path(file_path, os.path.join(base_dir, 'js'))
        
        # 检查是否已经有导航相关的脚本
        if 'load-nav.js' in content:
            print(f"跳过 {file_path} - 已经包含导航脚本")
            return False
        
        # 修复head部分 - 添加JavaScript引用
        head_pattern = r'(<link rel="stylesheet" href="[^"]*style\.css"[^>]*>)'
        if re.search(head_pattern, content):
            replacement = f'''\1
    <script src="{js_path}/load-nav.js" defer></script>
    <script src="{js_path}/components.js" defer></script>'''
            content = re.sub(head_pattern, replacement, content)
        
        # 修复body开始部分 - 添加导航容器
        body_pattern = r'(<body[^>]*>)\s*(<header>)'
        if re.search(body_pattern, content):
            replacement = r'\1\n    <div class="nav-container"></div>\n    \n    \2'
            content = re.sub(body_pattern, replacement, content)
        
        # 在header内添加面包屑
        header_container_pattern = r'(<header>\s*<div class="container">)\s*(<h1>)'
        if re.search(header_container_pattern, content):
            replacement = r'\1\n            <div class="breadcrumb"></div>\n            \2'
            content = re.sub(header_container_pattern, replacement, content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已修复: {file_path}")
        return True
        
    except Exception as e:
        print(f"修复 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent
    print(f"基础目录: {base_dir}")
    
    # 需要修复的目录列表
    directories_to_fix = [
        'part1_python_basics',
        'part2_data_analysis', 
        'part3_finance_applications',
        'part4_advanced_topics'
    ]
    
    total_fixed = 0
    total_files = 0
    
    for directory in directories_to_fix:
        dir_path = base_dir / directory
        if not dir_path.exists():
            print(f"目录不存在: {dir_path}")
            continue
            
        print(f"\n处理目录: {directory}")
        
        # 查找所有HTML文件
        html_files = list(dir_path.rglob('*.html'))
        
        for html_file in html_files:
            total_files += 1
            if fix_html_file(html_file, base_dir):
                total_fixed += 1
    
    print(f"\n修复完成!")
    print(f"总文件数: {total_files}")
    print(f"已修复: {total_fixed}")
    print(f"跳过: {total_files - total_fixed}")

if __name__ == '__main__':
    main()