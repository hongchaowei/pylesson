#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复exercises.html文件缺少CSS样式的问题
为所有exercises.html文件添加style.css引用，并修复HTML结构
"""

import os
import re
from pathlib import Path

def fix_exercises_css():
    """
    为所有exercises.html文件添加CSS样式表引用并修复HTML结构
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
            
            # 检查是否已经有CSS引用
            if 'style.css' in content:
                print(f"ℹ️  文件已有CSS引用: {file_path.relative_to(project_root)}")
                continue
            
            # 计算相对路径深度来确定正确的CSS路径
            relative_path = file_path.relative_to(project_root)
            depth = len(relative_path.parts) - 1  # 减1因为文件本身不算目录层级
            css_path = '../' * depth + 'css/style.css'
            
            # 创建CSS链接标签
            css_link = f'    <link rel="stylesheet" href="{css_path}">\n'
            
            new_content = content
            
            # 检查HTML结构并修复
            if '</head>' in content:
                # 正常情况：在</head>前添加CSS链接
                new_content = content.replace('</head>', f'{css_link}</head>')
            elif '<head>' in content and '<div class="home-button-container">' in content:
                # 特殊情况：缺少</head>标签，需要在home-button-container前添加</head>
                # 先添加CSS链接，然后添加</head>
                pattern = r'(<script[^>]*></script>\s*)(\s*<div class="home-button-container">)'
                replacement = f'\\1{css_link}</head>\\2'
                new_content = re.sub(pattern, replacement, content)
            elif '<head>' in content:
                # 其他情况：在最后一个head内容后添加CSS和</head>
                # 找到最后一个script或link标签
                last_head_content = re.findall(r'(<(?:script|link)[^>]*(?:></script>|>))', content)
                if last_head_content:
                    last_tag = last_head_content[-1]
                    new_content = content.replace(last_tag, f'{last_tag}\n{css_link}</head>\n')
                else:
                    # 如果head中没有其他内容，直接在<head>后添加
                    new_content = content.replace('<head>', f'<head>\n{css_link}</head>\n')
            else:
                print(f"⚠️  无法确定HTML结构: {file_path.relative_to(project_root)}")
                continue
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 添加CSS引用并修复HTML结构: {file_path.relative_to(project_root)}")
            fixed_count += 1
                
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {e}")
    
    print(f"\n🎉 完成！总共为 {fixed_count} 个文件添加了CSS样式引用。")

if __name__ == '__main__':
    fix_exercises_css()