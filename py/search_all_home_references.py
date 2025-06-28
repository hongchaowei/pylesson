#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索所有包含"首页"、"home"、"返回"等关键词的内容
"""

import os
import re
from pathlib import Path

def search_home_references_in_file(file_path):
    """搜索文件中所有与首页相关的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 搜索关键词
        keywords = ['首页', 'home', '返回', 'Home', 'HOME', 'index.html']
        
        matches = []
        for line_num, line in enumerate(lines, 1):
            for keyword in keywords:
                if keyword in line:
                    matches.append((line_num, line.strip()))
                    break  # 避免同一行重复匹配
        
        return matches
        
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return []

def main():
    """主函数"""
    base_dir = Path('.')
    
    # 检查case_studies.html文件
    file_path = base_dir / 'case_studies.html'
    
    if file_path.exists():
        print(f"搜索文件 {file_path} 中所有与首页相关的内容...\n")
        
        matches = search_home_references_in_file(file_path)
        
        print(f"找到 {len(matches)} 处相关内容:\n")
        
        for line_num, content in matches:
            print(f"第 {line_num} 行: {content}")
    else:
        print(f"文件不存在: {file_path}")

if __name__ == '__main__':
    main()