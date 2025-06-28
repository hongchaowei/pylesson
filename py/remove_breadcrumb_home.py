#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除面包屑导航中的首页链接，只保留右上角的返回首页按钮
"""

import os
import re
from pathlib import Path

def remove_breadcrumb_home_link(file_path):
    """移除JavaScript中面包屑导航的首页链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找并修改面包屑配置，移除首页链接
        # 匹配 breadcrumbs: [ { text: '首页', href: 'index.html' }, ... ]
        breadcrumb_pattern = r"breadcrumbs:\s*\[\s*\{\s*text:\s*['\"]首页['\"],\s*href:\s*['\"][^'\"]*['\"]\s*\},?\s*"
        
        # 替换为空的面包屑数组开始
        content = re.sub(breadcrumb_pattern, 'breadcrumbs: [', content)
        
        # 如果替换后出现空的面包屑数组，清理格式
        content = re.sub(r'breadcrumbs:\s*\[\s*\]', 'breadcrumbs: []', content)
        
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
    
    # 特殊文件列表
    special_files = [
        'case_studies.html',
        'knowledge_graph.html', 
        'blockchain_finance.html',
        'deep_learning_finance.html',
        'syllabus.html',
        'test_navigation.html'
    ]
    
    print("移除面包屑导航中的首页链接...\n")
    
    for file_name in special_files:
        file_path = base_dir / file_name
        if file_path.exists():
            if remove_breadcrumb_home_link(file_path):
                print(f"修复: {file_path}")
                fixed_count += 1
            else:
                print(f"无需修复: {file_path}")
        else:
            print(f"文件不存在: {file_name}")
    
    print(f"\n总共修复了 {fixed_count} 个文件的面包屑首页链接")

if __name__ == '__main__':
    main()