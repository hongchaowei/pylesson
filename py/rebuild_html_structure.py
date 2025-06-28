#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彻底重建HTML文件结构
提取内容并重新构建标准的HTML结构
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment

def extract_content_from_html(content):
    """
    从混乱的HTML中提取有用的内容
    """
    # 提取title
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else '页面标题'
    
    # 提取所有有用的head内容（除了基本标签）
    head_extras = []
    
    # 提取highlight.js相关的CSS和JS
    highlight_css = re.findall(r'<link[^>]*href="[^"]*highlight[^"]*"[^>]*>', content)
    highlight_js = re.findall(r'<script[^>]*src="[^"]*highlight[^"]*"[^>]*></script>', content)
    highlight_init = re.findall(r'<script[^>]*>\s*hljs\.highlightAll\(\);?\s*</script>', content)
    
    head_extras.extend(highlight_css)
    head_extras.extend(highlight_js)
    head_extras.extend(highlight_init)
    
    # 提取其他特殊的CSS和JS（如d3.js等）
    special_css = re.findall(r'<link[^>]*href="[^"]*(?:d3|chart|graph)[^"]*"[^>]*>', content)
    special_js = re.findall(r'<script[^>]*src="[^"]*(?:d3|chart|graph)[^"]*"[^>]*></script>', content)
    
    head_extras.extend(special_css)
    head_extras.extend(special_js)
    
    # 提取内联样式
    inline_styles = re.findall(r'<style[^>]*>.*?</style>', content, re.DOTALL)
    head_extras.extend(inline_styles)
    
    # 提取body内容（移除重复的结构）
    body_content = content
    
    # 移除所有HTML结构标签
    body_content = re.sub(r'<!DOCTYPE[^>]*>', '', body_content)
    body_content = re.sub(r'</?html[^>]*>', '', body_content)
    body_content = re.sub(r'<head[^>]*>.*?</head>', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'</?body[^>]*>', '', body_content)
    
    # 移除重复的home-button和header
    home_buttons = re.findall(r'<div class="home-button-container">.*?</div>', body_content, re.DOTALL)
    headers = re.findall(r'<header>.*?</header>', body_content, re.DOTALL)
    
    # 移除所有home-button和header
    body_content = re.sub(r'<div class="home-button-container">.*?</div>', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'<header>.*?</header>', '', body_content, flags=re.DOTALL)
    
    # 清理多余的空行和空白
    body_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', body_content)
    body_content = body_content.strip()
    
    return title, head_extras, body_content

def rebuild_html_files():
    """
    重建所有HTML文件
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"重建 {len(html_files)} 个HTML文件的结构...\n")
    
    rebuilt_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
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
            
            # 提取内容
            title, head_extras, body_content = extract_content_from_html(content)
            
            # 构建新的HTML结构
            new_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{css_path}">'''
            
            # 添加JavaScript（排除特殊页面）
            special_pages = ['knowledge_graph.html', 'case_studies.html', 'blockchain_finance.html', 'deep_learning_finance.html']
            if file_path.name not in special_pages:
                new_html += f'\n    <script src="{js_path}" defer></script>'
            
            # 添加额外的head内容
            if head_extras:
                new_html += '\n    ' + '\n    '.join(head_extras)
            
            new_html += '\n</head>\n<body>'
            
            # 添加返回首页按钮
            new_html += f'''\n    <div class="home-button-container">\n        <a href="{home_path}" class="home-button">🏠 返回首页</a>\n    </div>'''
            
            # 添加header（排除首页）
            if file_path.name != 'index.html':
                new_html += f'''\n\n    <header>\n        <div class="container">\n            <div class="breadcrumb"></div>\n            <h1>{title}</h1>\n            <p class="subtitle">页面描述</p>\n        </div>\n    </header>'''
            
            # 添加主要内容
            if body_content.strip():
                new_html += f'\n\n{body_content}'
            
            new_html += '\n\n</body>\n</html>'
            
            # 保存重建的文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            relative_path = str(file_path.relative_to(project_root))
            print(f"✅ 已重建: {relative_path}")
            rebuilt_count += 1
            
        except Exception as e:
            relative_path = str(file_path.relative_to(project_root))
            print(f"❌ 重建文件 {relative_path} 时出错: {e}")
    
    print(f"\n🎉 重建完成！共处理了 {rebuilt_count} 个文件")
    
    # 最终验证
    print("\n" + "=" * 50)
    print("重建后验证结果")
    print("=" * 50)
    
    verify_rebuilt_structure()

def verify_rebuilt_structure():
    """
    验证重建后的结构
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"验证 {len(html_files)} 个HTML文件...\n")
    
    issues = {
        'missing_doctype': [],
        'duplicate_tags': [],
        'missing_css': [],
        'missing_home_button': [],
        'missing_header': [],
        'structure_errors': []
    }
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(project_root))
            
            # 检查DOCTYPE
            if not content.strip().startswith('<!DOCTYPE html>'):
                issues['missing_doctype'].append(relative_path)
            
            # 检查重复标签
            if content.count('<!DOCTYPE html>') > 1:
                issues['duplicate_tags'].append(f"{relative_path}: 重复DOCTYPE")
            if len(re.findall(r'<html[^>]*>', content)) > 1:
                issues['duplicate_tags'].append(f"{relative_path}: 重复html标签")
            if len(re.findall(r'<head[^>]*>', content)) > 1:
                issues['duplicate_tags'].append(f"{relative_path}: 重复head标签")
            if len(re.findall(r'<body[^>]*>', content)) > 1:
                issues['duplicate_tags'].append(f"{relative_path}: 重复body标签")
            
            # 检查CSS引用
            if 'style.css' not in content:
                issues['missing_css'].append(relative_path)
            
            # 检查返回首页按钮
            if 'home-button' not in content:
                issues['missing_home_button'].append(relative_path)
            
            # 检查header结构（排除首页）
            if '<header>' not in content and file_path.name != 'index.html':
                issues['missing_header'].append(relative_path)
            
            # 检查基本结构
            if '<html' not in content or '</html>' not in content:
                issues['structure_errors'].append(f"{relative_path}: 缺少html标签")
            if '<head>' not in content or '</head>' not in content:
                issues['structure_errors'].append(f"{relative_path}: 缺少head标签")
            if '<body>' not in content or '</body>' not in content:
                issues['structure_errors'].append(f"{relative_path}: 缺少body标签")
                
        except Exception as e:
            issues['structure_errors'].append(f"{relative_path}: 读取错误 - {e}")
    
    # 显示验证结果
    total_issues = 0
    for issue_type, issue_list in issues.items():
        if issue_list:
            issue_names = {
                'missing_doctype': '缺少DOCTYPE声明',
                'duplicate_tags': '重复标签',
                'missing_css': '缺少CSS样式表',
                'missing_home_button': '缺少返回首页按钮',
                'missing_header': '缺少header结构',
                'structure_errors': '结构错误'
            }
            
            print(f"❌ {issue_names[issue_type]} ({len(issue_list)}个问题):")
            for issue in issue_list[:3]:  # 只显示前3个
                print(f"   - {issue}")
            if len(issue_list) > 3:
                print(f"   ... 还有 {len(issue_list) - 3} 个问题")
            print()
            total_issues += len(issue_list)
    
    if total_issues == 0:
        print("🎉 所有HTML文件结构重建成功！")
        print("✅ 所有文件都具备：")
        print("   - 标准的HTML5 DOCTYPE声明")
        print("   - 唯一且正确的html、head、body标签")
        print("   - 统一的CSS样式引用")
        print("   - 返回首页按钮")
        print("   - 标准的header结构（非首页）")
        print("   - 清洁的HTML文档结构")
    else:
        print(f"⚠️  仍有 {total_issues} 个问题需要检查")

if __name__ == "__main__":
    print("=" * 60)
    print("彻底重建HTML文件结构")
    print("=" * 60)
    
    rebuild_html_files()