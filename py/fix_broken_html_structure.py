#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML结构不完整的文件
专门处理缺少DOCTYPE、title、body等基本HTML结构的文件
"""

import os
import re
from pathlib import Path

def fix_broken_html_files():
    """
    修复HTML结构不完整的文件
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"检查 {len(html_files)} 个HTML文件的结构完整性...\n")
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
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
                js_path = '../../../js/components.js'
                home_path = '../../../index.html'
            
            # 检查是否是结构不完整的文件（没有DOCTYPE或body标签）
            if not content.strip().startswith('<!DOCTYPE html>') or '<body>' not in content:
                
                # 获取页面标题
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
                if title_match:
                    page_title = title_match.group(1)
                else:
                    # 从文件名推断标题
                    if 'project' in file_path.name:
                        page_title = '项目实战'
                    elif 'lesson' in file_path.name:
                        page_title = '课程内容'
                    elif 'exercise' in file_path.name:
                        page_title = '练习'
                    else:
                        page_title = '页面标题'
                
                # 提取现有的head内容（如果有的话）
                head_content = ''
                head_match = re.search(r'<head[^>]*>(.*?)</head>', content, re.DOTALL)
                if head_match:
                    head_content = head_match.group(1)
                    # 移除原有的head标签
                    content = re.sub(r'<head[^>]*>.*?</head>', '', content, flags=re.DOTALL)
                
                # 提取现有的body内容（如果有的话）
                body_content = ''
                if '<body>' in content or '<body ' in content:
                    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
                    if body_match:
                        body_content = body_match.group(1)
                        # 移除原有的body标签
                        content = re.sub(r'<body[^>]*>.*?</body>', '', content, flags=re.DOTALL)
                else:
                    # 如果没有body标签，将所有内容作为body内容
                    # 移除html标签
                    content = re.sub(r'</?html[^>]*>', '', content)
                    body_content = content.strip()
                
                # 构建完整的HTML结构
                new_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="stylesheet" href="{css_path}">
    <script src="{js_path}" defer></script>'''
                
                # 如果原来有其他head内容，保留它们
                if head_content.strip():
                    # 清理head内容，移除重复的meta和link标签
                    head_content = re.sub(r'<meta charset="UTF-8"[^>]*>', '', head_content)
                    head_content = re.sub(r'<meta name="viewport"[^>]*>', '', head_content)
                    head_content = re.sub(r'<title[^>]*>.*?</title>', '', head_content, flags=re.DOTALL)
                    head_content = re.sub(r'<link[^>]*href="[^"]*style\.css"[^>]*>', '', head_content)
                    head_content = re.sub(r'<script[^>]*src="[^"]*components\.js"[^>]*></script>', '', head_content)
                    
                    if head_content.strip():
                        new_content += '\n' + head_content.strip()
                
                new_content += '''\n</head>
<body>
    <div class="home-button-container">
        <a href="''' + home_path + '''" class="home-button">🏠 返回首页</a>
    </div>

    <header>
        <div class="container">
            <div class="breadcrumb"></div>
            <h1>''' + page_title + '''</h1>
            <p class="subtitle">页面描述</p>
        </div>
    </header>

''' + body_content + '''

</body>
</html>'''
                
                # 保存修复后的文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                relative_path = str(file_path.relative_to(project_root))
                print(f"✅ 已重构: {relative_path}")
                fixed_count += 1
                modified = True
            
            # 对于结构完整但缺少返回首页按钮或header的文件
            elif 'home-button' not in content or ('<header>' not in content and file_path.name != 'index.html'):
                
                # 添加返回首页按钮
                if 'home-button' not in content:
                    home_button = f'''    <div class="home-button-container">\n        <a href="{home_path}" class="home-button">🏠 返回首页</a>\n    </div>'''
                    
                    content = re.sub(
                        r'(<body[^>]*>)',
                        f'\1\n{home_button}\n',
                        content
                    )
                    modified = True
                
                # 添加header结构
                if '<header>' not in content and file_path.name != 'index.html':
                    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
                    if title_match:
                        page_title = title_match.group(1).split(' - ')[0]
                    else:
                        page_title = '页面标题'
                    
                    header_html = f'''\n    <header>\n        <div class="container">\n            <div class="breadcrumb"></div>\n            <h1>{page_title}</h1>\n            <p class="subtitle">页面描述</p>\n        </div>\n    </header>\n'''
                    
                    # 在home-button-container后添加header
                    content = re.sub(
                        r'(</div>\s*(?=\s*(?:<nav|<main|<div|<section)))',
                        f'\1{header_html}',
                        content
                    )
                    modified = True
                
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    relative_path = str(file_path.relative_to(project_root))
                    print(f"✅ 已完善: {relative_path}")
                    fixed_count += 1
                
        except Exception as e:
            relative_path = str(file_path.relative_to(project_root))
            print(f"❌ 处理文件 {relative_path} 时出错: {e}")
    
    print(f"\n🎉 结构修复完成！共处理了 {fixed_count} 个文件")
    
    # 最终验证
    print("\n" + "=" * 50)
    print("最终验证结果")
    print("=" * 50)
    
    verify_final_ui_consistency()

def verify_final_ui_consistency():
    """
    最终验证UI一致性
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    issues = {
        'missing_doctype': [],
        'missing_css': [],
        'missing_home_button': [],
        'missing_header': [],
        'missing_body': []
    }
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(project_root))
            
            # 检查DOCTYPE
            if not content.strip().startswith('<!DOCTYPE html>'):
                issues['missing_doctype'].append(relative_path)
            
            # 检查CSS引用
            if 'style.css' not in content:
                issues['missing_css'].append(relative_path)
            
            # 检查返回首页按钮
            if 'home-button' not in content:
                issues['missing_home_button'].append(relative_path)
            
            # 检查header结构（排除首页）
            if '<header>' not in content and file_path.name != 'index.html':
                issues['missing_header'].append(relative_path)
            
            # 检查body标签
            if '<body>' not in content and '<body ' not in content:
                issues['missing_body'].append(relative_path)
                
        except Exception as e:
            print(f"❌ 验证文件 {relative_path} 时出错: {e}")
    
    # 显示验证结果
    total_issues = 0
    for issue_type, files in issues.items():
        if files:
            issue_names = {
                'missing_doctype': '缺少DOCTYPE声明',
                'missing_css': '缺少CSS样式表',
                'missing_home_button': '缺少返回首页按钮',
                'missing_header': '缺少header结构',
                'missing_body': '缺少body标签'
            }
            
            print(f"❌ {issue_names[issue_type]} ({len(files)}个文件):")
            for file in files[:3]:  # 只显示前3个
                print(f"   - {file}")
            if len(files) > 3:
                print(f"   ... 还有 {len(files) - 3} 个文件")
            print()
            total_issues += len(files)
    
    if total_issues == 0:
        print("🎉 所有HTML文件的UI风格已完全统一！")
        print("✅ 所有文件都具备：")
        print("   - 标准的HTML5 DOCTYPE声明")
        print("   - 统一的CSS样式引用")
        print("   - 返回首页按钮")
        print("   - 标准的header结构")
        print("   - 完整的HTML文档结构")
    else:
        print(f"⚠️  仍有 {total_issues} 个UI问题需要检查")

if __name__ == "__main__":
    print("=" * 60)
    print("修复HTML结构不完整的文件")
    print("=" * 60)
    
    fix_broken_html_files()