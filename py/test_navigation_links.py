#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导航链接脚本
验证所有页面的导航链接是否正确
"""

import os
import re
from urllib.parse import urljoin, urlparse

def test_navigation_links():
    """
    测试导航链接的正确性
    """
    print("开始测试导航链接...")
    
    # 读取nav.html获取所有链接
    nav_file = 'nav.html'
    if not os.path.exists(nav_file):
        print(f"错误：找不到 {nav_file} 文件")
        return False
    
    with open(nav_file, 'r', encoding='utf-8') as f:
        nav_content = f.read()
    
    # 提取nav.html中的所有链接
    nav_links = re.findall(r'href="([^"#]+)"', nav_content)
    print(f"nav.html中找到 {len(nav_links)} 个链接")
    
    # 测试不同深度的页面
    test_pages = [
        ('./index.html', 0),
        ('./part1_python_basics/index.html', 1),
        ('./part1_python_basics/module1/lesson1.html', 2),
        ('./part4_advanced_topics/module16/lesson1.html', 2)
    ]
    
    all_passed = True
    
    for page_path, depth in test_pages:
        if not os.path.exists(page_path):
            print(f"跳过不存在的文件: {page_path}")
            continue
        
        print(f"\n测试页面: {page_path} (深度: {depth})")
        
        # 模拟JavaScript处理后的链接
        root_path = '../' * depth
        processed_links = []
        
        for link in nav_links:
            if link == 'index.html':
                processed_link = root_path + 'index.html'
            elif link.startswith('./'):
                if link.startswith('./part'):
                    # 模块路径链接
                    processed_link = root_path + link[2:]
                else:
                    # 根目录文件链接
                    processed_link = root_path + link[2:]
            else:
                processed_link = link
            
            processed_links.append(processed_link)
        
        # 验证处理后的链接是否存在
        page_dir = os.path.dirname(page_path)
        valid_count = 0
        invalid_count = 0
        
        for i, processed_link in enumerate(processed_links):
            if processed_link.startswith('#') or processed_link.startswith('http'):
                continue  # 跳过锚点和外部链接
            
            # 计算绝对路径
            if page_dir:
                target_path = os.path.normpath(os.path.join(page_dir, processed_link))
            else:
                target_path = os.path.normpath(processed_link)
            
            # 检查文件是否存在
            if os.path.exists(target_path):
                print(f"  ✓ {nav_links[i]} -> {processed_link}")
                valid_count += 1
            else:
                print(f"  ✗ {nav_links[i]} -> {processed_link} (目标不存在: {target_path})")
                invalid_count += 1
                all_passed = False
        
        print(f"  结果: {valid_count} 个有效链接, {invalid_count} 个无效链接")
    
    return all_passed

def test_javascript_logic():
    """
    测试JavaScript逻辑是否正确
    """
    print("\n测试JavaScript逻辑...")
    
    # 测试样例
    test_cases = [
        {
            'file': './index.html',
            'depth': 0,
            'nav_links': ['index.html', './syllabus.html', './part1_python_basics/module1/index.html'],
            'expected': ['index.html', 'syllabus.html', 'part1_python_basics/module1/index.html']
        },
        {
            'file': './part1_python_basics/module1/lesson1.html',
            'depth': 2,
            'nav_links': ['index.html', './syllabus.html', './part1_python_basics/module1/index.html'],
            'expected': ['../../index.html', '../../syllabus.html', '../../part1_python_basics/module1/index.html']
        }
    ]
    
    for case in test_cases:
        print(f"\n测试文件: {case['file']}")
        root_path = '../' * case['depth']
        
        for i, nav_link in enumerate(case['nav_links']):
            if nav_link == 'index.html':
                result = root_path + 'index.html'
            elif nav_link.startswith('./'):
                if nav_link.startswith('./part'):
                    result = root_path + nav_link[2:]
                else:
                    result = root_path + nav_link[2:]
            else:
                result = nav_link
            
            expected = case['expected'][i]
            if result == expected:
                print(f"  ✓ {nav_link} -> {result}")
            else:
                print(f"  ✗ {nav_link} -> {result} (期望: {expected})")

if __name__ == "__main__":
    print("=== 导航链接测试工具 ===")
    
    # 测试导航链接
    if test_navigation_links():
        print("\n🎉 所有导航链接测试通过！")
    else:
        print("\n❌ 部分导航链接测试失败！")
    
    # 测试JavaScript逻辑
    test_javascript_logic()
    
    print("\n测试完成！")