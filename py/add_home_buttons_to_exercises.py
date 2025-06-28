#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有exercises.html文件添加统一的返回首页按钮
确保每个exercises.html文件都有一个home-button样式的返回首页按钮
"""

import os
import re
from pathlib import Path

def add_home_buttons_to_exercises():
    """
    为所有exercises.html文件添加返回首页按钮
    """
    # 项目根目录
    project_root = Path(r'c:\Users\Administrator\Desktop\测试')
    
    # 查找所有exercises.html文件
    exercises_files = list(project_root.rglob('exercises.html'))
    
    added_count = 0
    
    for file_path in exercises_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经有home-button
            if 'home-button-container' in content or 'class="home-button"' in content:
                print(f"ℹ️  文件已有返回首页按钮: {file_path.relative_to(project_root)}")
                continue
            
            # 计算相对路径深度来确定正确的index.html路径
            relative_path = file_path.relative_to(project_root)
            depth = len(relative_path.parts) - 1  # 减1因为文件本身不算目录层级
            index_path = '../' * depth + 'index.html'
            
            # 创建home-button HTML
            home_button_html = f'''<div class="home-button-container">
    <a href="{index_path}" class="home-button">🏠 返回首页</a>
</div>
'''
            
            new_content = content
            
            # 尝试在<body>标签后添加
            if '<body>' in content:
                new_content = content.replace('<body>', f'<body>\n{home_button_html}')
            # 如果没有<body>标签，在</head>后添加
            elif '</head>' in content:
                new_content = content.replace('</head>', f'</head>\n{home_button_html}')
            # 如果连</head>都没有，在第一个主要内容标签前添加
            elif '<main' in content:
                new_content = re.sub(r'(<main[^>]*>)', f'{home_button_html}\\1', content)
            else:
                print(f"⚠️  无法确定插入位置: {file_path.relative_to(project_root)}")
                continue
            
            # 检查是否需要添加CSS引用
            if 'components.js' not in content:
                # 计算components.js的相对路径
                js_path = '../' * depth + 'js/components.js'
                # 在</head>前添加script标签
                script_tag = f'    <script src="{js_path}" defer></script>\n'
                if '</head>' in new_content:
                    new_content = new_content.replace('</head>', f'{script_tag}</head>')
                else:
                    # 如果没有</head>，在<html>后添加完整的head部分
                    head_section = f'''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>练习题 - Python金融编程课程</title>
{script_tag}</head>
'''
                    new_content = new_content.replace('<html lang="zh-CN">', f'<html lang="zh-CN">\n{head_section}')
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 添加返回首页按钮: {file_path.relative_to(project_root)}")
            added_count += 1
                
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {e}")
    
    print(f"\n🎉 完成！总共为 {added_count} 个文件添加了返回首页按钮。")

if __name__ == '__main__':
    add_home_buttons_to_exercises()