#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复lesson文件的格式和结构问题
"""

import os
import re
from pathlib import Path

def final_fix_lessons():
    """最终修复所有lesson HTML文件的格式和结构问题"""
    
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
            
            original_content = content
            
            # 1. 确保在<body>标签后有nav-container div
            if '<div class="nav-container"></div>' not in content:
                # 在<body>标签后添加nav-container
                content = re.sub(
                    r'(<body>)\s*(<header>)',
                    r'\1\n    <div class="nav-container"></div>\n\n    \2',
                    content
                )
            
            # 2. 修复JavaScript引用的格式
            # 确保breadcrumb.js和animations.js在单独的行上
            content = re.sub(
                r'(<script src="../../js/breadcrumb\.js"></script>)\s*(<script src="../../js/animations\.js"></script>)',
                r'\1\n    \2',
                content
            )
            
            # 3. 清理多余的空行
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            # 4. 确保正确的缩进
            content = re.sub(r'\n</body>', '\n\n</body>', content)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(lesson_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"修复 {lesson_file.relative_to(root_dir)}")
                fixed_count += 1
            else:
                print(f"跳过 {lesson_file.relative_to(root_dir)} - 无需修复")
                
        except Exception as e:
            print(f"处理文件 {lesson_file} 时出错: {e}")
    
    print(f"\n最终修复完成！共修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    final_fix_lessons()