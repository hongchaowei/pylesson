#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复exercises.html文件的所有问题
确保与lesson.html完全一致的结构和功能
"""

import os
import re
from pathlib import Path

def final_fix_exercises():
    """
    最终修复所有exercises.html文件的问题
    """
    # 项目根目录
    project_root = Path(r'c:\Users\Administrator\Desktop\测试')
    
    # 查找所有exercises.html文件
    exercises_files = list(project_root.rglob('exercises.html'))
    
    fixed_count = 0
    
    for file_path in exercises_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = file_path.relative_to(project_root)
            new_content = content
            changes_made = False
            
            # 1. 添加代码高亮功能（如果缺少）
            if 'highlight.js' not in content:
                # 在components.js后添加highlight.js
                components_pattern = r'(<script src="[^"]*components\.js" defer></script>)'
                if re.search(components_pattern, content):
                    highlight_html = '''\n    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/atom-one-dark.min.css">\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>\n    <script>hljs.highlightAll();</script>'''
                    replacement = f'\\1{highlight_html}'
                    new_content = re.sub(components_pattern, replacement, new_content)
                    changes_made = True
                    print(f"✅ 添加代码高亮: {relative_path}")
            
            # 2. 统一section class名称
            section_replacements = {
                'exercises-intro': 'lesson-content',
                'exercise-section': 'lesson-content',
                'exercises-content': 'lesson-content',
                'exercise-content': 'lesson-content'
            }
            
            for old_class, new_class in section_replacements.items():
                if old_class in new_content:
                    new_content = new_content.replace(f'class="{old_class}"', f'class="{new_class}"')
                    changes_made = True
                    print(f"✅ 统一section class: {relative_path} ({old_class} -> {new_class})")
            
            # 3. 确保有lesson-content class的section
            if 'lesson-content' not in new_content and '<section' in new_content:
                # 将第一个section改为lesson-content
                new_content = re.sub(r'<section[^>]*>', '<section class="lesson-content">', new_content, count=1)
                changes_made = True
                print(f"✅ 添加lesson-content class: {relative_path}")
            
            # 4. 确保highlight.js初始化脚本存在
            if 'highlight.js' in new_content and 'hljs.highlightAll()' not in new_content:
                highlight_pattern = r'(<script src="https://cdnjs\.cloudflare\.com/ajax/libs/highlight\.js/[^"]+/highlight\.min\.js"></script>)'
                if re.search(highlight_pattern, new_content):
                    replacement = r'\1\n    <script>hljs.highlightAll();</script>'
                    new_content = re.sub(highlight_pattern, replacement, new_content)
                    changes_made = True
                    print(f"✅ 添加highlight.js初始化: {relative_path}")
            
            # 写回文件
            if changes_made:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ 最终修复: {relative_path}")
                fixed_count += 1
            else:
                print(f"ℹ️  无需修改: {relative_path}")
                
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {e}")
    
    print(f"\n🎉 完成！总共修复了 {fixed_count} 个文件。")

if __name__ == '__main__':
    final_fix_exercises()