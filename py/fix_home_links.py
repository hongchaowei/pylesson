#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复首页链接路径错误的脚本
"""

import os
import re

def calculate_relative_path(file_path, target_file):
    """计算从当前文件到目标文件的相对路径"""
    file_dir = os.path.dirname(file_path)
    rel_path = os.path.relpath(target_file, file_dir)
    return rel_path.replace('\\', '/')

def fix_home_links_in_file(file_path, root_dir):
    """修复单个文件中的首页链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 计算正确的首页路径
        correct_index_path = calculate_relative_path(file_path, os.path.join(root_dir, 'index.html'))
        
        # 查找所有指向index.html的链接
        # 匹配模式：href="任意路径/index.html"
        pattern = r'href=["\']([^"\']*)index\.html["\']'
        matches = re.findall(pattern, content)
        
        fixed_links = []
        
        for match in matches:
            current_href = f'href="{match}index.html"'
            correct_href = f'href="{correct_index_path}"'
            
            # 如果当前路径不正确，则替换
            if match + 'index.html' != correct_index_path:
                content = content.replace(current_href, correct_href)
                fixed_links.append(f'{match}index.html -> {correct_index_path}')
        
        # 如果有修改，写入文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, fixed_links
        else:
            return False, []
            
    except Exception as e:
        return False, [f"错误: {e}"]

def fix_all_home_links(root_dir):
    """修复所有HTML文件中的首页链接"""
    html_files = []
    
    # 递归查找所有HTML文件
    for root, dirs, files in os.walk(root_dir):
        # 跳过py目录
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                html_files.append(file_path)
    
    print(f"检查 {len(html_files)} 个HTML文件的首页链接...")
    print("=" * 60)
    
    fixed_count = 0
    total_fixes = 0
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        was_fixed, fixes = fix_home_links_in_file(file_path, root_dir)
        
        if was_fixed:
            fixed_count += 1
            total_fixes += len(fixes)
            print(f"✓ 修复: {rel_path}")
            for fix in fixes:
                print(f"  - {fix}")
        else:
            if fixes and "错误" in fixes[0]:
                print(f"✗ 错误: {rel_path}")
                for fix in fixes:
                    print(f"  - {fix}")
            else:
                print(f"○ 无需修复: {rel_path}")
    
    print("\n" + "=" * 60)
    print(f"修复完成:")
    print(f"- 修复文件数: {fixed_count}")
    print(f"- 修复链接数: {total_fixes}")
    print(f"- 总文件数: {len(html_files)}")
    
    return fixed_count, total_fixes

def verify_home_links(root_dir):
    """验证所有首页链接是否正确"""
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                html_files.append(file_path)
    
    print(f"\n验证 {len(html_files)} 个文件的首页链接...")
    print("=" * 60)
    
    correct_count = 0
    error_count = 0
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 计算正确的首页路径
            correct_index_path = calculate_relative_path(file_path, os.path.join(root_dir, 'index.html'))
            
            # 检查是否有首页链接
            if '返回首页' in content or 'home-button' in content:
                # 查找index.html链接
                pattern = r'href=["\']([^"\']*)index\.html["\']'
                matches = re.findall(pattern, content)
                
                has_error = False
                for match in matches:
                    if match + 'index.html' != correct_index_path:
                        if not has_error:
                            print(f"✗ 错误: {rel_path}")
                            error_count += 1
                            has_error = True
                        print(f"  - 错误路径: {match}index.html (应为: {correct_index_path})")
                
                if not has_error:
                    correct_count += 1
                    print(f"✓ 正确: {rel_path}")
            else:
                correct_count += 1
                print(f"○ 无首页链接: {rel_path}")
                
        except Exception as e:
            error_count += 1
            print(f"✗ 读取错误: {rel_path} - {e}")
    
    print("\n" + "=" * 60)
    print(f"验证结果:")
    print(f"- 正确文件: {correct_count}")
    print(f"- 错误文件: {error_count}")
    print(f"- 总文件数: {len(html_files)}")
    
    if error_count == 0:
        print("\n🎉 所有首页链接都正确！")
    
    return correct_count, error_count

if __name__ == "__main__":
    # 获取当前脚本所在目录的上级目录作为根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    print(f"开始修复首页链接...")
    print(f"根目录: {root_dir}")
    
    # 执行修复
    fixed_count, total_fixes = fix_all_home_links(root_dir)
    
    # 验证结果
    verify_home_links(root_dir)