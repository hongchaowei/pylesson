#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终极修复HTML文件结构问题
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment

def extract_content_from_html(content):
    """
    从HTML内容中提取有用信息
    """
    # 提取标题
    title_match = re.search(r'<title[^>]*>([^<]*)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "页面标题"
    
    # 提取所有样式
    styles = []
    style_matches = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    for style in style_matches:
        if style.strip():
            styles.append(style.strip())
    
    # 提取特殊脚本引用
    special_scripts = set()
    script_matches = re.findall(r'<script[^>]*src=["\']([^"\'>]*)["\'][^>]*></script>', content, re.IGNORECASE)
    for script in script_matches:
        if 'highlight' in script or 'd3' in script or 'chart' in script or 'plotly' in script:
            special_scripts.add(script)
    
    # 提取内联脚本
    inline_scripts = []
    inline_script_matches = re.findall(r'<script[^>]*>([^<]*(?:(?!</script>)<[^<]*)*)</script>', content, re.DOTALL | re.IGNORECASE)
    for script in inline_script_matches:
        if script.strip() and 'hljs.highlightAll()' not in script:
            inline_scripts.append(script.strip())
    
    # 提取body内容（去掉重复的结构）
    body_content = ""
    
    # 尝试多种方式提取body内容
    body_matches = re.findall(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if body_matches:
        # 取最长的body内容
        body_content = max(body_matches, key=len)
    else:
        # 如果没有完整的body标签，尝试提取主要内容
        # 去掉head部分
        temp_content = re.sub(r'<head>.*?</head>', '', content, flags=re.DOTALL | re.IGNORECASE)
        temp_content = re.sub(r'<!DOCTYPE[^>]*>', '', temp_content, flags=re.IGNORECASE)
        temp_content = re.sub(r'<html[^>]*>', '', temp_content, flags=re.IGNORECASE)
        temp_content = re.sub(r'</html>', '', temp_content, flags=re.IGNORECASE)
        temp_content = re.sub(r'<body[^>]*>', '', temp_content, flags=re.IGNORECASE)
        temp_content = re.sub(r'</body>', '', temp_content, flags=re.IGNORECASE)
        body_content = temp_content.strip()
    
    # 清理body内容中的重复结构
    if body_content:
        # 移除重复的home button
        home_button_pattern = r'<div class="home-button-container">.*?</div>'
        home_buttons = re.findall(home_button_pattern, body_content, re.DOTALL)
        if len(home_buttons) > 1:
            # 保留第一个，移除其他
            for i in range(1, len(home_buttons)):
                body_content = body_content.replace(home_buttons[i], '', 1)
        
        # 移除重复的header
        header_pattern = r'<header>.*?</header>'
        headers = re.findall(header_pattern, body_content, re.DOTALL)
        if len(headers) > 1:
            # 保留第一个，移除其他
            for i in range(1, len(headers)):
                body_content = body_content.replace(headers[i], '', 1)
    
    return {
        'title': title,
        'styles': styles,
        'special_scripts': list(special_scripts),
        'inline_scripts': inline_scripts,
        'body_content': body_content
    }

def rebuild_html_file(file_path):
    """
    重建单个HTML文件
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取内容
        extracted = extract_content_from_html(content)
        
        # 构建新的HTML结构
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('    <meta charset="UTF-8">')
        html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'    <title>{extracted["title"]}</title>')
        html_parts.append('    <link rel="stylesheet" href="../../css/style.css">')
        
        # 添加特殊脚本
        for script in extracted['special_scripts']:
            html_parts.append(f'    <script src="{script}"></script>')
        
        # 添加highlight.js初始化（如果有highlight.js）
        if any('highlight' in script for script in extracted['special_scripts']):
            html_parts.append('    <script>hljs.highlightAll();</script>')
        
        # 添加样式
        if extracted['styles']:
            html_parts.append('    <style>')
            for style in extracted['styles']:
                html_parts.append(f'        {style}')
            html_parts.append('    </style>')
        
        # 添加内联脚本
        for script in extracted['inline_scripts']:
            html_parts.append('    <script>')
            html_parts.append(f'        {script}')
            html_parts.append('    </script>')
        
        html_parts.append('</head>')
        html_parts.append('<body>')
        
        # 添加返回首页按钮（除了index.html）
        if file_path.name != 'index.html':
            html_parts.append('    <div class="home-button-container">')
            html_parts.append('        <a href="../../index.html" class="home-button">🏠 返回首页</a>')
            html_parts.append('    </div>')
            html_parts.append('')
            html_parts.append('    <header>')
            html_parts.append('        <h1>Python金融数据分析与机器学习</h1>')
            html_parts.append('        <nav>')
            html_parts.append('            <ul>')
            html_parts.append('                <li><a href="../../index.html">首页</a></li>')
            html_parts.append('                <li><a href="../../syllabus.html">课程大纲</a></li>')
            html_parts.append('                <li><a href="../../knowledge_graph.html">知识图谱</a></li>')
            html_parts.append('            </ul>')
            html_parts.append('        </nav>')
            html_parts.append('    </header>')
            html_parts.append('')
        
        # 添加主要内容
        if extracted['body_content']:
            # 确保内容不包含重复的结构元素
            clean_content = extracted['body_content']
            
            # 移除可能的重复DOCTYPE
            clean_content = re.sub(r'<!DOCTYPE[^>]*>', '', clean_content, flags=re.IGNORECASE)
            
            # 移除可能的重复html标签
            clean_content = re.sub(r'</?html[^>]*>', '', clean_content, flags=re.IGNORECASE)
            
            # 移除可能的重复head部分
            clean_content = re.sub(r'<head>.*?</head>', '', clean_content, flags=re.DOTALL | re.IGNORECASE)
            
            # 移除可能的重复body标签
            clean_content = re.sub(r'</?body[^>]*>', '', clean_content, flags=re.IGNORECASE)
            
            html_parts.append(clean_content.strip())
        
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        # 写入文件
        new_content = '\n'.join(html_parts)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
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
    
    print(f"终极修复 {len(html_files)} 个HTML文件...\n")
    
    success_count = 0
    
    for file_path in html_files:
        if rebuild_html_file(file_path):
            relative_path = str(file_path.relative_to(project_root))
            print(f"✅ 已重建: {relative_path}")
            success_count += 1
    
    print(f"\n🎉 完成！共重建了 {success_count} 个文件")
    
    # 最终验证
    print("\n" + "=" * 50)
    print("最终验证结果")
    print("=" * 50)
    
    verify_all_files()

def verify_all_files():
    """
    验证所有文件
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
            
            if content.count('<!DOCTYPE html>') > 1:
                file_issues.append(f'重复DOCTYPE({content.count("<!DOCTYPE html>")})')
            
            if content.count('<html') > 1:
                file_issues.append(f'重复html标签({content.count("<html")})')
            
            if content.count('<head>') > 1:
                file_issues.append(f'重复head标签({content.count("<head>")})')
            
            if content.count('<body>') > 1:
                file_issues.append(f'重复body标签({content.count("<body>")})')
            
            if content.count('<head>') == 0:
                file_issues.append('缺少head标签')
            
            if content.count('<body>') == 0:
                file_issues.append('缺少body标签')
            
            if 'style.css' not in content:
                file_issues.append('缺少CSS')
            
            if 'home-button' not in content and file_path.name != 'index.html':
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
        for issue in issues[:10]:  # 显示前10个
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... 还有 {len(issues) - 10} 个问题")
    
    if len(issues) == 0:
        print("\n🎉 所有HTML文件UI风格已完全统一！")
        print("✅ 所有文件都具备：")
        print("   - 标准的HTML5 DOCTYPE声明")
        print("   - 正确的html、head、body标签结构")
        print("   - 统一的CSS样式引用")
        print("   - 返回首页按钮（非首页文件）")
        print("   - 标准的header结构（非首页文件）")
        print("   - 清洁的HTML文档结构")
        print("   - 无重复标签和引用")
    else:
        print(f"\n⚠️  还有 {len(issues)} 个问题需要处理")

if __name__ == "__main__":
    print("=" * 60)
    print("终极HTML结构修复")
    print("=" * 60)
    
    main()