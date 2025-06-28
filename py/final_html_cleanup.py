#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终HTML清理脚本
彻底解决重复标签和结构问题
"""

import os
import re
from pathlib import Path

def clean_html_file(file_path):
    """
    清理单个HTML文件
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 计算相对路径
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
        
        # 提取title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
        title = title_match.group(1) if title_match else '页面标题'
        
        # 提取特殊的CSS和JS引用
        special_links = []
        
        # 提取highlight.js相关
        highlight_patterns = [
            r'<link[^>]*href="[^"]*highlight[^"]*"[^>]*>',
            r'<script[^>]*src="[^"]*highlight[^"]*"[^>]*></script>',
            r'<script[^>]*>\s*hljs\.highlightAll\(\);?\s*</script>'
        ]
        
        for pattern in highlight_patterns:
            matches = re.findall(pattern, content)
            special_links.extend(matches)
        
        # 提取其他特殊库（d3.js等）
        special_patterns = [
            r'<link[^>]*href="[^"]*(?:d3|chart|graph)[^"]*"[^>]*>',
            r'<script[^>]*src="[^"]*(?:d3|chart|graph)[^"]*"[^>]*></script>'
        ]
        
        for pattern in special_patterns:
            matches = re.findall(pattern, content)
            special_links.extend(matches)
        
        # 提取内联样式
        inline_styles = re.findall(r'<style[^>]*>.*?</style>', content, re.DOTALL)
        special_links.extend(inline_styles)
        
        # 提取body内容（移除所有HTML结构）
        body_content = content
        
        # 移除所有结构标签
        body_content = re.sub(r'<!DOCTYPE[^>]*>', '', body_content)
        body_content = re.sub(r'</?html[^>]*>', '', body_content)
        body_content = re.sub(r'<head[^>]*>.*?</head>', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'</?body[^>]*>', '', body_content)
        
        # 移除meta标签
        body_content = re.sub(r'<meta[^>]*>', '', body_content)
        
        # 移除title标签
        body_content = re.sub(r'<title[^>]*>.*?</title>', '', body_content)
        
        # 移除CSS和JS引用
        body_content = re.sub(r'<link[^>]*>', '', body_content)
        body_content = re.sub(r'<script[^>]*src="[^"]*"[^>]*></script>', '', body_content)
        
        # 移除所有home-button
        body_content = re.sub(r'<div class="home-button-container">.*?</div>', '', body_content, flags=re.DOTALL)
        
        # 移除所有header
        body_content = re.sub(r'<header>.*?</header>', '', body_content, flags=re.DOTALL)
        
        # 清理空白
        body_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', body_content)
        body_content = body_content.strip()
        
        # 构建新的HTML
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
        
        # 添加特殊链接
        if special_links:
            new_html += '\n    ' + '\n    '.join(special_links)
        
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
        
        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        return True
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def final_cleanup():
    """
    最终清理所有HTML文件
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"最终清理 {len(html_files)} 个HTML文件...\n")
    
    success_count = 0
    
    for file_path in html_files:
        if clean_html_file(file_path):
            relative_path = str(file_path.relative_to(project_root))
            print(f"✅ 已清理: {relative_path}")
            success_count += 1
    
    print(f"\n🎉 清理完成！成功处理了 {success_count} 个文件")
    
    # 最终验证
    print("\n" + "=" * 50)
    print("最终验证结果")
    print("=" * 50)
    
    final_verification()

def final_verification():
    """
    最终验证
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"验证 {len(html_files)} 个HTML文件...\n")
    
    issues = []
    perfect_files = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(project_root))
            file_issues = []
            
            # 检查基本结构
            if not content.strip().startswith('<!DOCTYPE html>'):
                file_issues.append('缺少DOCTYPE')
            
            if content.count('<!DOCTYPE html>') > 1:
                file_issues.append('重复DOCTYPE')
            
            if len(re.findall(r'<html[^>]*>', content)) != 1:
                file_issues.append('html标签异常')
            
            if len(re.findall(r'<head[^>]*>', content)) != 1:
                file_issues.append('head标签异常')
            
            if len(re.findall(r'<body[^>]*>', content)) != 1:
                file_issues.append('body标签异常')
            
            if 'style.css' not in content:
                file_issues.append('缺少CSS')
            
            if 'home-button' not in content:
                file_issues.append('缺少返回按钮')
            
            if '<header>' not in content and file_path.name != 'index.html':
                file_issues.append('缺少header')
            
            if file_issues:
                issues.append(f"{relative_path}: {', '.join(file_issues)}")
            else:
                perfect_files += 1
                
        except Exception as e:
            issues.append(f"{relative_path}: 读取错误 - {e}")
    
    # 显示结果
    if issues:
        print(f"❌ 发现 {len(issues)} 个文件有问题:")
        for issue in issues[:5]:  # 只显示前5个
            print(f"   - {issue}")
        if len(issues) > 5:
            print(f"   ... 还有 {len(issues) - 5} 个问题")
    
    print(f"\n✅ 完美的文件: {perfect_files} 个")
    print(f"❌ 有问题的文件: {len(issues)} 个")
    
    if len(issues) == 0:
        print("\n🎉 所有HTML文件UI风格已完全统一！")
        print("✅ 所有文件都具备：")
        print("   - 标准的HTML5 DOCTYPE声明")
        print("   - 正确的html、head、body标签结构")
        print("   - 统一的CSS样式引用")
        print("   - 返回首页按钮")
        print("   - 标准的header结构（非首页）")
        print("   - 清洁的HTML文档结构")
    else:
        print(f"\n⚠️  还需要手动检查 {len(issues)} 个问题")

if __name__ == "__main__":
    print("=" * 60)
    print("最终HTML清理和UI统一")
    print("=" * 60)
    
    final_cleanup()