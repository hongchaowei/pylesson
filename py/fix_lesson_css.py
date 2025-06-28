#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复lesson文件缺少CSS引用的问题
"""

import os
import re
from pathlib import Path

def fix_lesson_css():
    """为所有lesson HTML文件添加CSS样式表引用"""
    
    # 项目根目录
    root_dir = Path(r'c:\Users\Administrator\Desktop\测试')
    
    # 查找所有lesson*.html文件
    lesson_files = []
    for part_dir in root_dir.glob('part*'):
        if part_dir.is_dir():
            for module_dir in part_dir.glob('module*'):
                if module_dir.is_dir():
                    for lesson_file in module_dir.glob('lesson*.html'):
                        lesson_files.append(lesson_file)
    
    print(f"找到 {len(lesson_files)} 个lesson文件")
    
    # 修复每个文件
    fixed_count = 0
    for lesson_file in lesson_files:
        try:
            # 读取文件内容
            with open(lesson_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经有CSS引用
            if 'style.css' in content:
                print(f"跳过 {lesson_file.relative_to(root_dir)} - 已有CSS引用")
                continue
            
            # 计算相对路径深度
            # lesson文件在 part*/module*/ 目录下，需要回到根目录
            relative_path = "../../css/style.css"
            
            # 在</head>标签前添加CSS引用
            css_link = f'    <link rel="stylesheet" href="{relative_path}">\n'
            
            # 查找</head>标签的位置
            head_pattern = r'(\s*)</head>'
            replacement = f'{css_link}\\1</head>'
            
            new_content = re.sub(head_pattern, replacement, content)
            
            # 如果内容有变化，写回文件
            if new_content != content:
                with open(lesson_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"修复 {lesson_file.relative_to(root_dir)}")
                fixed_count += 1
            else:
                print(f"未找到</head>标签: {lesson_file.relative_to(root_dir)}")
                
        except Exception as e:
            print(f"处理文件 {lesson_file} 时出错: {e}")
    
    print(f"\n修复完成！共修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    fix_lesson_css()