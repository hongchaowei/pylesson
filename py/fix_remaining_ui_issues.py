#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余的UI风格问题
专门处理CSS引用、返回首页按钮和header结构缺失的问题
"""

import os
import re
from pathlib import Path

def fix_remaining_issues():
    """
    修复剩余的UI风格问题
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"检查 {len(html_files)} 个HTML文件的剩余UI问题...\n")
    
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
                js_path = '../../js/components.js'
                home_path = '../../index.html'
            
            # 1. 修复CSS引用问题
            if 'style.css' not in content:
                # 确保有head标签
                if '<head>' not in content:
                    content = re.sub(
                        r'(<html[^>]*>)',
                        r'\1\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>页面标题</title>\n</head>',
                        content
                    )
                
                # 添加CSS引用
                css_link = f'    <link rel="stylesheet" href="{css_path}">'
                if '</head>' in content:
                    content = re.sub(
                        r'(\s*</head>)',
                        f'\n{css_link}\n\1',
                        content
                    )
                else:
                    # 如果没有</head>，在<title>后添加
                    content = re.sub(
                        r'(<title[^>]*>.*?</title>)',
                        f'\1\n{css_link}',
                        content,
                        flags=re.DOTALL
                    )
                modified = True
            
            # 2. 修复返回首页按钮
            if 'home-button' not in content:
                home_button = f'''    <div class="home-button-container">\n        <a href="{home_path}" class="home-button">🏠 返回首页</a>\n    </div>'''
                
                # 在<body>后添加
                if '<body>' in content or '<body ' in content:
                    content = re.sub(
                        r'(<body[^>]*>)',
                        f'\1\n{home_button}',
                        content
                    )
                    modified = True
                else:
                    # 如果没有body标签，添加完整的body结构
                    if '</head>' in content:
                        content = re.sub(
                            r'(</head>)',
                            f'\1\n<body>\n{home_button}',
                            content
                        )
                        # 在文件末尾添加</body>
                        if '</html>' in content:
                            content = re.sub(
                                r'(</html>)',
                                r'\n</body>\n\1',
                                content
                            )
                        else:
                            content += '\n</body>\n</html>'
                        modified = True
            
            # 3. 修复header结构（排除首页）
            if '<header>' not in content and file_path.name != 'index.html':
                # 获取页面标题
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
                if title_match:
                    page_title = title_match.group(1).split(' - ')[0]
                else:
                    page_title = '页面标题'
                
                header_html = f'''\n    <header>\n        <div class="container">\n            <div class="breadcrumb"></div>\n            <h1>{page_title}</h1>\n            <p class="subtitle">页面描述</p>\n        </div>\n    </header>'''
                
                # 在home-button-container后添加header
                if 'home-button-container' in content:
                    content = re.sub(
                        r'(</div>\s*(?=\s*(?:<nav|<main|<div|<section|$)))',
                        f'\1{header_html}\n',
                        content
                    )
                    modified = True
            
            # 4. 确保有main容器
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
            
            # 如果有修改，保存文件
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                relative_path = str(file_path.relative_to(project_root))
                print(f"✅ 已修复: {relative_path}")
                fixed_count += 1
                
        except Exception as e:
            relative_path = str(file_path.relative_to(project_root))
            print(f"❌ 处理文件 {relative_path} 时出错: {e}")
    
    print(f"\n🎉 修复完成！共处理了 {fixed_count} 个文件")
    
    # 最终验证
    print("\n" + "=" * 50)
    print("最终验证结果")
    print("=" * 50)
    
    verify_ui_consistency()

def verify_ui_consistency():
    """
    验证UI一致性
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    issues = {
        'missing_css': [],
        'missing_home_button': [],
        'missing_header': []
    }
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(project_root))
            
            # 检查CSS引用
            if 'style.css' not in content:
                issues['missing_css'].append(relative_path)
            
            # 检查返回首页按钮
            if 'home-button' not in content:
                issues['missing_home_button'].append(relative_path)
            
            # 检查header结构（排除首页）
            if '<header>' not in content and file_path.name != 'index.html':
                issues['missing_header'].append(relative_path)
                
        except Exception as e:
            print(f"❌ 验证文件 {relative_path} 时出错: {e}")
    
    # 显示验证结果
    total_issues = 0
    for issue_type, files in issues.items():
        if files:
            issue_names = {
                'missing_css': '缺少CSS样式表',
                'missing_home_button': '缺少返回首页按钮',
                'missing_header': '缺少header结构'
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
    else:
        print(f"⚠️  仍有 {total_issues} 个UI问题需要手动检查")

if __name__ == "__main__":
    print("=" * 60)
    print("修复剩余UI风格问题")
    print("=" * 60)
    
    fix_remaining_issues()