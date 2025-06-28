#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导航条功能
验证不同深度的HTML文件是否能正确加载和显示导航条
"""

import os
import re
from pathlib import Path

def analyze_navigation_setup(file_path, root_dir):
    """分析文件的导航设置"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取导航相关信息
        info = {
            'has_nav_container': 'id="navigation-container"' in content,
            'has_load_script': 'loadNavigation' in content,
            'nav_fetch_path': None,
            'link_replacement_pattern': None,
            'relative_depth': None
        }
        
        # 提取fetch路径
        fetch_match = re.search(r"fetch\('([^']+)'\)", content)
        if fetch_match:
            info['nav_fetch_path'] = fetch_match.group(1)
        
        # 提取链接替换模式
        replace_match = re.search(r'href="([^"]*\$1[^"]*)"|href="([^"]*index\.html[^"]*)', content)
        if replace_match:
            info['link_replacement_pattern'] = replace_match.group(1) or replace_match.group(2)
        
        # 计算相对深度
        rel_path = os.path.relpath(file_path, root_dir)
        depth = len(Path(rel_path).parts) - 1
        info['relative_depth'] = depth
        
        return info
    except Exception as e:
        return {'error': str(e)}

def verify_path_correctness(nav_fetch_path, expected_depth):
    """验证路径是否正确"""
    if expected_depth == 0:
        return nav_fetch_path == './nav.html'
    elif expected_depth == 1:
        return nav_fetch_path == '../nav.html'
    elif expected_depth == 2:
        return nav_fetch_path == '../../nav.html'
    elif expected_depth == 3:
        return nav_fetch_path == '../../../nav.html'
    else:
        expected_path = '../' * expected_depth + 'nav.html'
        return nav_fetch_path == expected_path

def main():
    """主函数"""
    root_dir = os.getcwd()
    print(f"开始测试导航条功能，根目录: {root_dir}")
    
    # 查找所有HTML文件（除了nav.html）
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # 跳过py目录
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html') and file != 'nav.html':
                html_files.append(os.path.join(root, file))
    
    print(f"找到 {len(html_files)} 个HTML文件需要测试")
    
    # 按深度分组统计
    depth_stats = {}
    correct_count = 0
    incorrect_count = 0
    error_count = 0
    
    for file_path in html_files:
        rel_file_path = os.path.relpath(file_path, root_dir)
        info = analyze_navigation_setup(file_path, root_dir)
        
        if 'error' in info:
            print(f"✗ 分析失败: {rel_file_path} - {info['error']}")
            error_count += 1
            continue
        
        depth = info['relative_depth']
        if depth not in depth_stats:
            depth_stats[depth] = {'total': 0, 'correct': 0, 'files': []}
        
        depth_stats[depth]['total'] += 1
        depth_stats[depth]['files'].append(rel_file_path)
        
        # 验证路径正确性
        if info['nav_fetch_path']:
            is_correct = verify_path_correctness(info['nav_fetch_path'], depth)
            if is_correct:
                depth_stats[depth]['correct'] += 1
                correct_count += 1
                status = "✓"
            else:
                incorrect_count += 1
                status = "✗"
            
            print(f"{status} {rel_file_path} (深度:{depth}, 路径:{info['nav_fetch_path']})")
        else:
            print(f"? {rel_file_path} (深度:{depth}, 未找到fetch路径)")
            incorrect_count += 1
    
    print(f"\n测试结果统计:")
    print(f"正确配置: {correct_count} 个文件")
    print(f"错误配置: {incorrect_count} 个文件")
    print(f"分析失败: {error_count} 个文件")
    
    print(f"\n按深度分布:")
    for depth in sorted(depth_stats.keys()):
        stats = depth_stats[depth]
        accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        expected_path = './nav.html' if depth == 0 else '../' * depth + 'nav.html'
        print(f"  深度 {depth} ({expected_path}): {stats['correct']}/{stats['total']} 正确 ({accuracy:.1f}%)")
        
        # 显示一些示例文件
        if len(stats['files']) <= 3:
            for file in stats['files']:
                print(f"    - {file}")
        else:
            for file in stats['files'][:2]:
                print(f"    - {file}")
            print(f"    - ... 还有 {len(stats['files']) - 2} 个文件")
    
    # 检查nav.html是否存在
    nav_file = os.path.join(root_dir, 'nav.html')
    if os.path.exists(nav_file):
        print(f"\n✓ nav.html 文件存在")
        with open(nav_file, 'r', encoding='utf-8') as f:
            nav_content = f.read()
        print(f"  - 文件大小: {len(nav_content)} 字符")
        print(f"  - 包含导航菜单: {'nav-menu' in nav_content}")
        print(f"  - 包含移动端按钮: {'mobile-menu-toggle' in nav_content}")
    else:
        print(f"\n✗ nav.html 文件不存在!")
    
    if correct_count == len(html_files) - error_count:
        print(f"\n🎉 所有HTML文件的导航配置都正确!")
        print(f"   - 每个文件都使用了正确的相对路径")
        print(f"   - 导航条应该能在所有页面正常显示")
    else:
        print(f"\n⚠️  有 {incorrect_count} 个文件的导航配置需要修复")

if __name__ == "__main__":
    main()