#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复lesson文件缺少JavaScript引用和清理内联代码的问题
"""

import os
import re
from pathlib import Path

def fix_lesson_js():
    """为所有lesson HTML文件添加animations.js引用并清理内联代码"""
    
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
            
            # 1. 添加animations.js引用（如果没有的话）
            if 'animations.js' not in content:
                # 在</body>标签前添加animations.js引用
                js_script = '    <script src="../../js/animations.js"></script>\n'
                
                # 查找</body>标签的位置
                body_pattern = r'(\s*)</body>'
                replacement = f'{js_script}\\1</body>'
                
                content = re.sub(body_pattern, replacement, content)
            
            # 2. 移除内联的返回首页按钮代码
            # 匹配从<script>到</script>的内联代码块，包含"返回首页"的
            inline_script_pattern = r'\s*<script>\s*document\.addEventListener\(.*?返回首页.*?</script>\s*'
            content = re.sub(inline_script_pattern, '', content, flags=re.DOTALL)
            
            # 3. 清理多余的空行
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            # 4. 修复CSS引用的格式问题（确保在新行上）
            content = re.sub(r'(</script>)\s*(<link rel="stylesheet")', r'\1\n    \2', content)
            
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
    
    print(f"\n修复完成！共修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    fix_lesson_js()