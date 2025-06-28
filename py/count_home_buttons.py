#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计和显示所有HTML文件中的返回首页按钮
"""

import os
import re
from pathlib import Path

def count_home_buttons_in_file(file_path):
    """统计单个文件中的返回首页按钮数量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找所有包含"返回首页"的行
        home_button_patterns = [
            r'<a[^>]*>.*?返回首页.*?</a>',
            r'<button[^>]*>.*?返回首页.*?</button>',
        ]
        
        all_matches = []
        for pattern in home_button_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            all_matches.extend(matches)
        
        return all_matches
        
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return []

def main():
    """主函数"""
    base_dir = Path('.')
    
    # 特殊文件列表
    special_files = [
        'case_studies.html',
        'knowledge_graph.html', 
        'blockchain_finance.html',
        'deep_learning_finance.html',
        'syllabus.html',
        'test_navigation.html',
        'index.html'
    ]
    
    print("检查特殊文件中的返回首页按钮数量...\n")
    
    for file_name in special_files:
        file_path = base_dir / file_name
        if file_path.exists():
            buttons = count_home_buttons_in_file(file_path)
            print(f"文件: {file_name}")
            print(f"返回首页按钮数量: {len(buttons)}")
            for i, button in enumerate(buttons, 1):
                print(f"  按钮 {i}: {button[:100]}..." if len(button) > 100 else f"  按钮 {i}: {button}")
            print()
        else:
            print(f"文件不存在: {file_name}\n")

if __name__ == '__main__':
    main()