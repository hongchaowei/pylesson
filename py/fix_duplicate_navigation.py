#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复重复导航问题的脚本
1. 移除内联的导航加载脚本
2. 确保只保留一个导航系统
3. 统一使用load-nav.js来加载导航
"""

import os
import re
import glob

def fix_duplicate_navigation():
    # 查找所有HTML文件
    html_files = []
    for pattern in ['part*/module*/*.html', '*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. 移除内联的导航加载脚本（jQuery版本）
            # 匹配从 <script> 到 </script> 包含 nav-container.load 的整个脚本块
            inline_nav_pattern = r'<script>\s*\$\(function\(\)\s*\{[\s\S]*?nav-container[\s\S]*?</script>'
            content = re.sub(inline_nav_pattern, '', content, flags=re.MULTILINE)
            
            # 2. 移除其他形式的内联导航脚本
            inline_nav_pattern2 = r'<script[^>]*>[\s\S]*?\$\([\s\S]*?nav-container[\s\S]*?</script>'
            content = re.sub(inline_nav_pattern2, '', content, flags=re.MULTILINE)
            
            # 3. 确保有nav-container div（如果没有的话）
            if '<div class="nav-container"></div>' not in content and '<body>' in content:
                content = content.replace('<body>', '<body>\n    <div class="nav-container"></div>')
            
            # 4. 确保引用了load-nav.js（如果没有的话）
            if 'load-nav.js' not in content and '</head>' in content:
                js_ref = '    <script src="../../js/load-nav.js"></script>\n'
                # 根据文件路径调整相对路径
                if file_path.count('/') == 0 or file_path.count('\\') == 0:  # 根目录文件
                    js_ref = '    <script src="js/load-nav.js"></script>\n'
                content = content.replace('</head>', js_ref + '</head>')
            
            # 5. 清理多余的空行
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            # 6. 移除重复的"返回首页"按钮脚本
            home_button_pattern = r'<script>[\s\S]*?返回首页[\s\S]*?</script>'
            content = re.sub(home_button_pattern, '', content, flags=re.MULTILINE)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"修复: {file_path}")
        
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    print(f"\n总共修复了 {fixed_count} 个文件的重复导航问题")

if __name__ == "__main__":
    fix_duplicate_navigation()