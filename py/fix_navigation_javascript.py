#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复导航JavaScript脚本
更新所有HTML文件中的导航加载JavaScript，使其正确处理新的模块链接路径
"""

import os
import re
import glob

def fix_navigation_javascript():
    """
    修复所有HTML文件中的导航JavaScript代码
    """
    print("开始修复导航JavaScript代码...")
    
    # 查找所有HTML文件
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html') and file != 'nav.html':
                html_files.append(os.path.join(root, file))
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    fixed_count = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含导航加载代码
            if 'loadNavigation' not in content:
                continue
            
            # 计算文件相对于根目录的深度
            depth = html_file.replace('.\\', '').replace('./', '').count(os.sep)
            nav_path = '../' * depth + 'nav.html'
            root_path = '../' * depth
            
            # 查找现有的JavaScript代码块
            js_pattern = r'function loadNavigation\(\)[\s\S]*?\.catch\([^;]*;\s*\}'
            
            if re.search(js_pattern, content):
                # 新的JavaScript代码
                new_js_code = f'''function loadNavigation() {{
    fetch('{nav_path}')
        .then(response => response.text())
        .then(html => {{
            // 更新导航中的链接路径
            let updatedHtml = html;
            
            // 处理根目录文件链接（index.html, syllabus.html等）
            updatedHtml = updatedHtml.replace(/href="index\\.html"/g, 'href="{root_path}index.html"');
            updatedHtml = updatedHtml.replace(/href="\\.\\/([^/]*\\.html)"/g, 'href="{root_path}$1"');
            
            // 处理模块路径链接（已经是完整相对路径，只需要添加根路径前缀）
            updatedHtml = updatedHtml.replace(/href="\\.\\/part([^"]*)"/g, 'href="{root_path}part$1"');
            
            document.getElementById('navigation-container').innerHTML = updatedHtml;
            
            // 添加移动端菜单切换功能
            const menuToggle = document.getElementById('menuToggle');
            const navMenu = document.querySelector('.nav-menu');
            if (menuToggle && navMenu) {{
                menuToggle.addEventListener('click', function() {{
                    navMenu.classList.toggle('active');
                }});
            }}
        }})
        .catch(error => console.error('导航加载失败:', error));
}}'''
                
                # 替换JavaScript代码
                content = re.sub(js_pattern, new_js_code, content)
                
                # 写回文件
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_count += 1
                print(f"✓ 修复: {html_file} (深度: {depth})")
            
        except Exception as e:
            print(f"✗ 处理文件失败 {html_file}: {e}")
    
    print(f"\n修复完成！总共修复了 {fixed_count} 个文件")
    return fixed_count > 0

def test_sample_files():
    """
    测试几个示例文件的导航代码
    """
    print("\n测试示例文件...")
    
    test_files = [
        './index.html',
        './part1_python_basics/module1/lesson1.html'
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n检查文件: {test_file}")
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找fetch语句
            fetch_match = re.search(r"fetch\('([^']*)'\)", content)
            if fetch_match:
                print(f"  fetch路径: {fetch_match.group(1)}")
            
            # 查找href替换语句
            href_matches = re.findall(r'href="[^"]*"', content)
            if href_matches:
                print(f"  找到 {len(href_matches)} 个href替换")

if __name__ == "__main__":
    print("=== 导航JavaScript修复工具 ===")
    
    # 修复JavaScript代码
    if fix_navigation_javascript():
        # 测试示例文件
        test_sample_files()
        print("\n修复完成！现在导航链接应该在所有页面中都能正确工作。")
    else:
        print("没有找到需要修复的文件。")
        # 即使没有修复，也测试一下现有文件
        test_sample_files()