#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复特殊文件中的重复返回首页按钮
针对case_studies.html, knowledge_graph.html, blockchain_finance.html等文件
"""

import os
import re
from pathlib import Path

def fix_special_file_home_buttons(file_path):
    """修复特殊文件中的重复返回首页按钮"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 检查是否已经有home-button样式的返回首页按钮
        if 'class="home-button"' in content and '🏠 返回首页' in content:
            print(f"文件 {file_path} 已有新样式的返回首页按钮")
            return False
        
        # 如果没有新样式按钮，添加一个
        if 'class="home-button"' not in content:
            # 在<body>标签后添加返回首页按钮
            if '<body>' in content:
                home_button_html = '''<body>
    <div class="home-button-container">
        <a href="index.html" class="home-button">🏠 返回首页</a>
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
    
    # 特殊文件列表
    special_files = [
        'case_studies.html',
        'knowledge_graph.html', 
        'blockchain_finance.html',
        'deep_learning_finance.html',
        'syllabus.html',
        'test_navigation.html'
    ]
    
    print(f"检查特殊文件的返回首页按钮...")
    
    for file_name in special_files:
        file_path = base_dir / file_name
        if file_path.exists():
            if fix_special_file_home_buttons(file_path):
                print(f"修复: {file_path}")
                fixed_count += 1
        else:
            print(f"文件不存在: {file_path}")
    
    print(f"\n总共修复了 {fixed_count} 个特殊文件的返回首页按钮")

if __name__ == '__main__':
    main()