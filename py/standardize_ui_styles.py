#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一所有HTML文件的UI风格
确保所有页面遵循一致的设计标准和样式规范
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set

def fix_html_structure(file_path: Path, content: str) -> str:
    """
    修复HTML文件的结构问题
    """
    modified = False
    
    # 计算相对路径到根目录
    depth = len(file_path.parts) - 1
    if depth == 1:  # 根目录文件
        css_path = './css/style.css'
        js_path = './js/components.js'
        home_path = 'index.html'
    elif depth == 2:  # 一级子目录
        css_path = '../css/style.css'
        js_path = '../js/components.js'
        home_path = '../index.html'
    else:  # 二级或更深子目录
        css_path = '../../css/style.css'
        js_path = '../../js/components.js'
        home_path = '../../index.html'
    
    # 1. 确保有正确的DOCTYPE和html标签
    if not content.strip().startswith('<!DOCTYPE html>'):
        content = '<!DOCTYPE html>\n' + content
        modified = True
    
    # 2. 确保有基本的meta标签
    if 'charset="UTF-8"' not in content:
        content = re.sub(
            r'(<head[^>]*>)',
            r'\1\n    <meta charset="UTF-8">',
            content
        )
        modified = True
    
    if 'viewport' not in content:
        content = re.sub(
            r'(<meta charset="UTF-8">)',
            r'\1\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            content
        )
        modified = True
    
    # 3. 确保引用CSS样式表
    if 'style.css' not in content:
        # 在</head>前添加CSS引用
        css_link = f'    <link rel="stylesheet" href="{css_path}">'
        content = re.sub(
            r'(\s*</head>)',
            f'\n{css_link}\n\1',
            content
        )
        modified = True
    
    # 4. 确保引用JavaScript文件（排除特殊页面）
    special_pages = ['knowledge_graph.html', 'case_studies.html', 'blockchain_finance.html', 'deep_learning_finance.html']
    if 'components.js' not in content and file_path.name not in special_pages:
        js_script = f'    <script src="{js_path}" defer></script>'
        content = re.sub(
            r'(<title[^>]*>.*?</title>)',
            f'\1\n{js_script}',
            content,
            flags=re.DOTALL
        )
        modified = True
    
    # 5. 确保有返回首页按钮
    if 'home-button' not in content:
        home_button = f'''    <div class="home-button-container">
        <a href="{home_path}" class="home-button">🏠 返回首页</a>
    </div>'''
        
        # 在<body>后添加
        content = re.sub(
            r'(<body[^>]*>)',
            f'\1\n{home_button}',
            content
        )
        modified = True
    
    # 6. 确保有header结构（排除首页）
    if '<header>' not in content and file_path.name != 'index.html':
        # 获取页面标题
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
        if title_match:
            page_title = title_match.group(1).split(' - ')[0]
        else:
            page_title = '页面标题'
        
        header_html = f'''<header>
        <div class="container">
            <div class="breadcrumb"></div>
            <h1>{page_title}</h1>
            <p class="subtitle">页面描述</p>
        </div>
    </header>'''
        
        # 在home-button-container后添加header
        content = re.sub(
            r'(</div>\s*(?=\s*(?:<nav|<main|<div|<section)))',
            f'\1\n\n{header_html}\n',
            content
        )
        modified = True
    
    # 7. 确保有main容器
    if '<main' not in content and '<section' in content:
        # 查找第一个section并包装在main中
        content = re.sub(
            r'(\s*<section)',
            r'\n    <main class="container">\1',
            content,
            count=1
        )
        # 在最后一个section后添加</main>
        content = re.sub(
            r'(</section>)(?!.*</section>)',
            r'\1\n    </main>',
            content
        )
        modified = True
    
    # 8. 为包含代码的页面添加代码高亮
    if ('<pre>' in content or '<code>' in content) and 'highlight.js' not in content:
        highlight_css = '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/atom-one-dark.min.css">'
        highlight_js = '    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>'
        highlight_init = '    <script>hljs.highlightAll();</script>'
        
        # 添加CSS
        content = re.sub(
            r'(\s*<link rel="stylesheet" href="[^"]*style\.css"[^>]*>)',
            f'\1\n{highlight_css}',
            content
        )
        
        # 添加JS
        content = re.sub(
            r'(\s*<link rel="stylesheet" href="[^"]*atom-one-dark\.min\.css"[^>]*>)',
            f'\1\n{highlight_js}\n{highlight_init}',
            content
        )
        modified = True
    
    return content if modified else None

def standardize_all_html_files():
    """
    标准化所有HTML文件的UI风格
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"开始标准化 {len(html_files)} 个HTML文件的UI风格...\n")
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # 修复文件结构
            fixed_content = fix_html_structure(file_path, original_content)
            
            if fixed_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                relative_path = str(file_path.relative_to(project_root))
                print(f"✅ 已标准化: {relative_path}")
                fixed_count += 1
            
        except Exception as e:
            relative_path = str(file_path.relative_to(project_root))
            print(f"❌ 处理文件 {relative_path} 时出错: {e}")
    
    print(f"\n🎉 UI风格标准化完成！共修复了 {fixed_count} 个文件")

def analyze_html_files():
    """
    分析所有HTML文件的UI风格和结构
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"\n分析 {len(html_files)} 个HTML文件的UI风格...\n")
    
    issues = {
        'missing_css': [],
        'missing_js': [],
        'missing_home_button': [],
        'missing_header': [],
        'missing_main': [],
        'missing_highlight_js': []
    }
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(project_root))
            
            # 检查各种UI元素
            if 'style.css' not in content:
                issues['missing_css'].append(relative_path)
            
            if 'components.js' not in content and file_path.name not in ['knowledge_graph.html', 'case_studies.html', 'blockchain_finance.html', 'deep_learning_finance.html']:
                issues['missing_js'].append(relative_path)
            
            if 'home-button' not in content:
                issues['missing_home_button'].append(relative_path)
            
            if '<header>' not in content and file_path.name != 'index.html':
                issues['missing_header'].append(relative_path)
            
            if '<main' not in content:
                issues['missing_main'].append(relative_path)
            
            if ('<pre>' in content or '<code>' in content) and 'highlight.js' not in content:
                issues['missing_highlight_js'].append(relative_path)
                
        except Exception as e:
            print(f"❌ 分析文件 {relative_path} 时出错: {e}")
    
    # 显示分析结果
    total_issues = 0
    for issue_type, files in issues.items():
        if files:
            issue_names = {
                'missing_css': '缺少CSS样式表',
                'missing_js': '缺少JavaScript文件',
                'missing_home_button': '缺少返回首页按钮',
                'missing_header': '缺少header结构',
                'missing_main': '缺少main容器',
                'missing_highlight_js': '缺少代码高亮'
            }
            
            print(f"❌ {issue_names[issue_type]} ({len(files)}个文件):")
            for file in files[:5]:  # 只显示前5个
                print(f"   - {file}")
            if len(files) > 5:
                print(f"   ... 还有 {len(files) - 5} 个文件")
            print()
            total_issues += len(files)
    
    if total_issues == 0:
        print("🎉 所有HTML文件的UI风格都已标准化！")
    else:
        print(f"⚠️  发现 {total_issues} 个UI风格问题")
    
    return total_issues

if __name__ == "__main__":
    print("=" * 60)
    print("HTML文件UI风格标准化工具")
    print("=" * 60)
    
    # 分析当前状态
    issues_before = analyze_html_files()
    
    if issues_before > 0:
        print("\n" + "=" * 60)
        print("开始修复UI风格问题...")
        print("=" * 60)
        
        # 标准化所有HTML文件
        standardize_all_html_files()
        
        print("\n" + "=" * 60)
        print("修复后的分析结果")
        print("=" * 60)
        
        # 再次分析
        analyze_html_files()
    else:
        print("\n✅ 所有文件已经符合UI标准，无需修复！")