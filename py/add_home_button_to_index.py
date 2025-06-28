#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为index.html文件添加返回首页按钮
"""

import os
import re
from pathlib import Path

def add_home_button_to_index(file_path):
    """为index.html文件添加返回首页按钮"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有返回首页按钮
        if '返回首页' in content:
            return False
        
        # 计算相对路径
        relative_path = os.path.relpath('.', os.path.dirname(file_path))
        if relative_path == '.':
            home_path = 'index.html'
        else:
            home_path = relative_path.replace('\\', '/') + '/index.html'
        
        # 在<body>标签后添加返回首页按钮
        if '<body>' in content:
            home_button_html = f'''<body>
<div class="home-button-container">
<a href="{home_path}" class="home-button">🏠 返回首页</a>
</div>'''
            
            content = content.replace('<body>', home_button_html)
            
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
    
    # 查找所有index.html文件
    index_files = list(base_dir.rglob('**/index.html'))
    
    print(f"找到 {len(index_files)} 个index.html文件")
    
    for index_file in index_files:
        if add_home_button_to_index(index_file):
            print(f"添加返回首页按钮: {index_file}")
            fixed_count += 1
    
    print(f"\n总共为 {fixed_count} 个index.html文件添加了返回首页按钮")

if __name__ == '__main__':
    main()