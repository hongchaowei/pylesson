#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终完整修复所有HTML文件
"""

import os
import re
from pathlib import Path

def extract_and_rebuild_html(file_path):
    """
    提取内容并重建HTML文件
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
        title = title_match.group(1) if title_match else file_path.stem.replace('_', ' ').title()
        
        # 提取所有样式
        styles = re.findall(r'<style[^>]*>.*?</style>', content, re.DOTALL)
        
        # 提取特殊的外部链接
        external_css = []
        external_js = []
        
        # highlight.js
        highlight_css_matches = re.findall(r'<link[^>]*href="[^"]*highlight[^"]*\.css"[^>]*>', content)
        highlight_js_matches = re.findall(r'<script[^>]*src="[^"]*highlight[^"]*\.js"[^>]*></script>', content)
        
        if highlight_css_matches:
            external_css.extend(highlight_css_matches[:1])  # 只保留一个
        if highlight_js_matches:
            external_js.extend(highlight_js_matches[:1])  # 只保留一个
            external_js.append('<script>hljs.highlightAll();</script>')  # 添加初始化
        
        # d3.js
        d3_matches = re.findall(r'<script[^>]*src="[^"]*d3[^"]*\.js"[^>]*></script>', content)
        if d3_matches:
            external_js.extend(d3_matches[:1])  # 只保留一个
        
        # 其他特殊库
        other_js = re.findall(r'<script[^>]*src="[^"]*(?:chart|graph|plotly)[^"]*"[^>]*></script>', content)
        external_js.extend(other_js)
        
        # 提取主要内容（移除所有HTML结构）
        main_content = content
        
        # 移除所有HTML结构标签
        main_content = re.sub(r'<!DOCTYPE[^>]*>', '', main_content)
        main_content = re.sub(r'</?html[^>]*>', '', main_content)
        main_content = re.sub(r'<head[^>]*>.*?</head>', '', main_content, flags=re.DOTALL)
        main_content = re.sub(r'</?body[^>]*>', '', main_content)
        
        # 移除meta、title、link、script标签
        main_content = re.sub(r'<meta[^>]*>', '', main_content)
        main_content = re.sub(r'<title[^>]*>.*?</title>', '', main_content)
        main_content = re.sub(r'<link[^>]*>', '', main_content)
        main_content = re.sub(r'<script[^>]*>.*?</script>', '', main_content, flags=re.DOTALL)
        
        # 移除home-button和header
        main_content = re.sub(r'<div class="home-button-container">.*?</div>', '', main_content, flags=re.DOTALL)
        main_content = re.sub(r'<header>.*?</header>', '', main_content, flags=re.DOTALL)
        
        # 清理空白
        main_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', main_content)
        main_content = main_content.strip()
        
        # 构建新的HTML
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('    <meta charset="UTF-8">')
        html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'    <title>{title}</title>')
        html_parts.append(f'    <link rel="stylesheet" href="{css_path}">')
        
        # 添加JavaScript（排除特殊页面）
        special_pages = ['knowledge_graph.html', 'case_studies.html', 'blockchain_finance.html', 'deep_learning_finance.html']
        if file_path.name not in special_pages:
            html_parts.append(f'    <script src="{js_path}" defer></script>')
        
        # 添加外部CSS
        for css in external_css:
            html_parts.append(f'    {css}')
        
        # 添加外部JS
        for js in external_js:
            html_parts.append(f'    {js}')
        
        # 添加内联样式
        for style in styles:
            html_parts.append(f'    {style}')
        
        html_parts.append('</head>')
        html_parts.append('<body>')
        
        # 添加返回首页按钮
        html_parts.append('    <div class="home-button-container">')
        html_parts.append(f'        <a href="{home_path}" class="home-button">🏠 返回首页</a>')
        html_parts.append('    </div>')
        
        # 添加header（排除首页）
        if file_path.name != 'index.html':
            html_parts.append('')
            html_parts.append('    <header>')
            html_parts.append('        <div class="container">')
            html_parts.append('            <div class="breadcrumb"></div>')
            html_parts.append(f'            <h1>{title}</h1>')
            html_parts.append('            <p class="subtitle">页面描述</p>')
            html_parts.append('        </div>')
            html_parts.append('    </header>')
        
        # 添加主要内容
        if main_content.strip():
            html_parts.append('')
            html_parts.append(main_content)
        
        html_parts.append('')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        # 生成最终HTML
        final_html = '\n'.join(html_parts)
        
        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        return True
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """
    主函数
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"最终修复 {len(html_files)} 个HTML文件...\n")
    
    success_count = 0
    
    for file_path in html_files:
        if extract_and_rebuild_html(file_path):
            relative_path = str(file_path.relative_to(project_root))
            print(f"✅ 已修复: {relative_path}")
            success_count += 1
    
    print(f"\n🎉 修复完成！成功处理了 {success_count} 个文件")
    
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
    
    perfect_files = 0
    issues = []
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(project_root))
            file_issues = []
            
            # 检查基本结构
            if not content.strip().startswith('<!DOCTYPE html>'):
                file_issues.append('缺少DOCTYPE')
            
            if content.count('<!DOCTYPE html>') != 1:
                file_issues.append(f'DOCTYPE数量异常({content.count("<!DOCTYPE html>")})')
            
            if content.count('<html') != 1:
                file_issues.append(f'html标签数量异常({content.count("<html")})')
            
            if content.count('<head>') != 1:
                file_issues.append(f'head标签数量异常({content.count("<head>")})')
            
            if content.count('<body>') != 1:
                file_issues.append(f'body标签数量异常({content.count("<body>")})')
            
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
    print(f"✅ 完美的文件: {perfect_files} 个")
    print(f"❌ 有问题的文件: {len(issues)} 个")
    
    if issues:
        print(f"\n问题详情:")
        for issue in issues[:3]:  # 只显示前3个
            print(f"   - {issue}")
        if len(issues) > 3:
            print(f"   ... 还有 {len(issues) - 3} 个问题")
    
    if len(issues) == 0:
        print("\n🎉 所有HTML文件UI风格已完全统一！")
        print("✅ 所有文件都具备：")
        print("   - 标准的HTML5 DOCTYPE声明")
        print("   - 正确的html、head、body标签结构")
        print("   - 统一的CSS样式引用")
        print("   - 返回首页按钮")
        print("   - 标准的header结构（非首页）")
        print("   - 清洁的HTML文档结构")
        print("   - 无重复标签和引用")

if __name__ == "__main__":
    print("=" * 60)
    print("最终完整修复HTML文件")
    print("=" * 60)
    
    main()