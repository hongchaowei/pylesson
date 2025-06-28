#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一exercises.html和lesson.html的结构和样式
确保exercises.html具有与lesson.html相同的功能和外观
"""

import os
import re
from pathlib import Path

def standardize_exercises_structure():
    """
    统一所有exercises.html文件的结构，使其与lesson.html保持一致
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
            
            # 计算相对路径深度
            relative_path = file_path.relative_to(project_root)
            depth = len(relative_path.parts) - 1
            css_path = '../' * depth + 'css/style.css'
            js_path = '../' * depth + 'js/components.js'
            
            new_content = content
            changes_made = False
            
            # 1. 确保有highlight.js的初始化脚本
            if 'highlight.js' in content and 'hljs.highlightAll()' not in content:
                # 在highlight.js script标签后添加初始化脚本
                highlight_pattern = r'(<script src="https://cdnjs\.cloudflare\.com/ajax/libs/highlight\.js/[^"]+/highlight\.min\.js"></script>)'
                if re.search(highlight_pattern, content):
                    replacement = r'\1\n    <script>hljs.highlightAll();</script>'
                    new_content = re.sub(highlight_pattern, replacement, new_content)
                    changes_made = True
                    print(f"✅ 添加highlight.js初始化: {relative_path}")
            
            # 2. 修复home-button结构问题
            if 'home-button' in content:
                # 查找并修复错误的home-button结构
                wrong_pattern = r'</header>\s*\n\s*<a href="[^"]+" class="home-button">[^<]+</a>\s*</div>'
                if re.search(wrong_pattern, new_content):
                    # 移除错误的home-button
                    new_content = re.sub(wrong_pattern, '</header>', new_content)
                    changes_made = True
                
                # 确保home-button在正确位置（body开始后，header前）
                if '<div class="home-button-container">' not in new_content:
                    home_button_html = '''    <div class="home-button-container">
        <a href="../../index.html" class="home-button">🏠 返回首页</a>
    </div>
'''
                    
                    # 在<body>后添加home-button
                    if '<body>' in new_content:
                        new_content = new_content.replace('<body>', f'<body>\n{home_button_html}')
                        changes_made = True
                        print(f"✅ 修复home-button位置: {relative_path}")
            
            # 3. 确保有正确的HTML结构
            if '<body>' not in content:
                # 如果没有body标签，需要重构HTML结构
                if '</head>' in content:
                    # 在</head>后添加<body>和正确的结构
                    home_button_html = '''\n<body>
    <div class="home-button-container">
        <a href="../../index.html" class="home-button">🏠 返回首页</a>
    </div>

    <header>
        <div class="container">
            <div class="breadcrumb"></div>
            <h1>练习题</h1>
            <p class="subtitle">巩固所学知识的练习题集</p>
        </div>
    </header>

'''
                    
                    new_content = new_content.replace('</head>', f'</head>{home_button_html}')
                    changes_made = True
                    print(f"✅ 添加完整HTML结构: {relative_path}")
            
            # 4. 确保main标签有正确的class
            if '<main class="container">' not in content and '<main' in content:
                new_content = re.sub(r'<main[^>]*>', '<main class="container">', new_content)
                changes_made = True
                print(f"✅ 修复main标签class: {relative_path}")
            
            # 5. 统一section的class名称
            if 'exercises-intro' in content:
                new_content = new_content.replace('exercises-intro', 'lesson-content')
                changes_made = True
            if 'exercise-section' in content:
                new_content = new_content.replace('exercise-section', 'lesson-content')
                changes_made = True
            
            # 6. 确保文件末尾有</body>和</html>标签
            if '</body>' not in content:
                if content.strip().endswith('</html>'):
                    new_content = new_content.replace('</html>', '\n</body>\n</html>')
                    changes_made = True
                elif not content.strip().endswith('</body>'):
                    new_content = new_content.rstrip() + '\n\n</body>\n</html>'
                    changes_made = True
            
            # 写回文件
            if changes_made:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ 标准化结构: {relative_path}")
                fixed_count += 1
            else:
                print(f"ℹ️  无需修改: {relative_path}")
                
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {e}")
    
    print(f"\n🎉 完成！总共标准化了 {fixed_count} 个文件的结构。")

if __name__ == '__main__':
    standardize_exercises_structure()