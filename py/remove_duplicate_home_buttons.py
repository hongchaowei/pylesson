#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除重复的返回首页按钮
只保留最新的home-button样式，移除旧的btn样式的返回首页按钮
"""

import os
import re
from pathlib import Path

def remove_old_home_buttons(file_path):
    """移除旧的返回首页按钮，保留新的home-button样式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 移除旧的返回首页按钮（btn样式的）
        # 匹配各种可能的旧按钮格式
        old_button_patterns = [
            r'<a href="[^"]*" class="btn btn-secondary">返回首页</a>',
            r'<a href="[^"]*" class="btn btn-outline">← 返回首页</a>',
            r'<a href="[^"]*" class="btn btn-outline">返回首页</a>',
        ]
        
        for pattern in old_button_patterns:
            content = re.sub(pattern, '', content)
        
        # 移除可能残留的nav-container和load-nav.js引用（如果存在）
        content = re.sub(r'\s*<div class="nav-container"></div>\s*', '', content)
        content = re.sub(r'\s*<script src="[^"]*load-nav\.js"[^>]*></script>\s*', '', content)
        
        # 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    base_dir = Path('.')
    fixed_count = 0
    
    # 查找所有HTML文件
    html_files = list(base_dir.rglob('*.html'))
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    for html_file in html_files:
        if remove_old_home_buttons(html_file):
            print(f"修复: {html_file}")
            fixed_count += 1
    
    print(f"\n总共修复了 {fixed_count} 个文件的重复返回首页按钮")

if __name__ == '__main__':
    main()