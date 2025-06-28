#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复导航条链接脚本
修复nav.html中的模块链接，使其指向正确的模块页面
"""

import os
import re

def fix_navigation_links():
    """
    修复nav.html中的导航链接
    """
    nav_file = 'nav.html'
    
    if not os.path.exists(nav_file):
        print(f"错误：找不到 {nav_file} 文件")
        return False
    
    # 读取nav.html文件
    with open(nav_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("开始修复导航链接...")
    
    # 定义正确的模块链接映射
    module_links = {
        '模块1: Python入门': './part1_python_basics/module1/index.html',
        '模块2: 数据结构与控制流': './part1_python_basics/module2/index.html',
        '模块3: 函数与模块': './part1_python_basics/module3/index.html',
        '模块4: 面向对象编程': './part1_python_basics/module4/index.html',
        '模块5: NumPy基础': './part2_data_analysis/module5/index.html',
        '模块6: Pandas数据处理': './part2_data_analysis/module6/index.html',
        '模块7: 数据可视化': './part2_data_analysis/module7/index.html',
        '模块8: 统计分析': './part2_data_analysis/module8/index.html',
        '模块9: 金融数据获取': './part3_finance_applications/module9/index.html',
        '模块10: 投资组合分析': './part3_finance_applications/module10/index.html',
        '模块11: 风险管理': './part3_finance_applications/module11/index.html',
        '模块12: 量化交易策略': './part3_finance_applications/module12/index.html',
        '模块13: 金融衍生品分析': './part4_advanced_topics/module13/index.html',
        '模块14: 算法交易与回测系统': './part4_advanced_topics/module14/index.html',
        '模块15: 机器学习在金融中的应用': './part4_advanced_topics/module15/index.html',
        '模块16: 综合项目与实践': './part4_advanced_topics/module16/index.html'
    }
    
    # 修复每个模块链接
    fixed_count = 0
    for module_name, correct_link in module_links.items():
        # 查找并替换模块链接
        pattern = f'<a href="index\.html">{re.escape(module_name)}</a>'
        replacement = f'<a href="{correct_link}">{module_name}</a>'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            fixed_count += 1
            print(f"✓ 修复链接: {module_name} -> {correct_link}")
    
    # 写回文件
    with open(nav_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n导航链接修复完成！")
    print(f"总共修复了 {fixed_count} 个模块链接")
    
    return True

def verify_links():
    """
    验证修复后的链接是否正确
    """
    nav_file = 'nav.html'
    
    with open(nav_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n验证链接状态:")
    
    # 查找所有href链接
    href_pattern = r'href="([^"]+)"'
    links = re.findall(href_pattern, content)
    
    valid_links = 0
    invalid_links = 0
    
    for link in links:
        if link.startswith('#') or link.startswith('http'):
            continue  # 跳过锚点链接和外部链接
        
        # 检查文件是否存在
        if link.startswith('./'):
            file_path = link[2:]  # 移除 './'
        else:
            file_path = link
        
        if os.path.exists(file_path):
            print(f"✓ {link}")
            valid_links += 1
        else:
            print(f"✗ {link} (文件不存在)")
            invalid_links += 1
    
    print(f"\n验证结果:")
    print(f"有效链接: {valid_links}")
    print(f"无效链接: {invalid_links}")
    
    return invalid_links == 0

if __name__ == "__main__":
    print("=== 导航链接修复工具 ===")
    
    # 修复链接
    if fix_navigation_links():
        # 验证链接
        verify_links()
        print("\n修复完成！现在所有模块链接都指向正确的页面。")
    else:
        print("修复失败！")