#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面修复HTML文件问题的脚本
主要修复：
1. 添加缺失的DOCTYPE声明
2. 修正CSS路径错误
3. 确保HTML结构完整性
"""

import os
import re
from pathlib import Path

def calculate_relative_path(file_path, target_file):
    """计算从当前文件到目标文件的相对路径"""
    file_dir = os.path.dirname(file_path)
    rel_path = os.path.relpath(target_file, file_dir)
    return rel_path.replace('\\', '/')

def fix_html_file(file_path, root_dir):
    """修复单个HTML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        issues_found = []
        
        # 1. 检查并添加DOCTYPE声明
        if not content.strip().startswith('<!DOCTYPE html>'):
            if content.strip().startswith('<html'):
                content = '<!DOCTYPE html>\n' + content
                issues_found.append('添加DOCTYPE声明')
            else:
                # 如果文件开头有其他内容，在html标签前添加DOCTYPE
                content = re.sub(r'(<html[^>]*>)', r'<!DOCTYPE html>\n\1', content)
                issues_found.append('添加DOCTYPE声明')
        
        # 2. 修正CSS路径
        css_path = calculate_relative_path(file_path, os.path.join(root_dir, 'css', 'style.css'))
        
        # 查找并替换CSS链接
        css_pattern = r'<link[^>]*href=["\']([^"\']*)css/style\.css["\'][^>]*>'
        css_matches = re.findall(css_pattern, content)
        
        if css_matches:
            # 替换错误的CSS路径
            new_css_link = f'<link rel="stylesheet" href="{css_path}">'
            content = re.sub(css_pattern, new_css_link, content)
            issues_found.append(f'修正CSS路径: {css_path}')
        
        # 3. 修正返回首页按钮的路径
        index_path = calculate_relative_path(file_path, os.path.join(root_dir, 'index.html'))
        
        # 查找并替换返回首页链接
        home_pattern = r'href=["\']([^"\']*)index\.html["\']'
        home_matches = re.findall(home_pattern, content)
        
        if home_matches:
            for match in home_matches:
                if 'index.html' in match and match != index_path:
                    old_href = f'href="{match}index.html"'
                    new_href = f'href="{index_path}"'
                    content = content.replace(old_href, new_href)
                    issues_found.append(f'修正首页链接: {index_path}')
        
        # 4. 确保基本HTML结构完整
        if '<html' in content and '</html>' not in content:
            content += '\n</html>'
            issues_found.append('添加缺失的</html>标签')
        
        if '<body' in content and '</body>' not in content:
            content = content.replace('</html>', '</body>\n</html>')
            issues_found.append('添加缺失的</body>标签')
        
        # 5. 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 如果有修改，写入文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, issues_found
        else:
            return False, []
            
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False, [f"错误: {e}"]

def scan_and_fix_all_html_files(root_dir):
    """扫描并修复所有HTML文件"""
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
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    fixed_count = 0
    total_issues = 0
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        was_fixed, issues = fix_html_file(file_path, root_dir)
        
        if was_fixed:
            fixed_count += 1
            total_issues += len(issues)
            print(f"✓ 修复: {rel_path}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            if issues:  # 有错误
                print(f"✗ 错误: {rel_path}")
                for issue in issues:
                    print(f"  - {issue}")
            else:  # 无需修复
                print(f"○ 无需修复: {rel_path}")
    
    print(f"\n修复完成:")
    print(f"- 总文件数: {len(html_files)}")
    print(f"- 修复文件数: {fixed_count}")
    print(f"- 修复问题数: {total_issues}")
    
    return fixed_count, total_issues

def verify_all_files(root_dir):
    """验证所有HTML文件的完整性"""
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                html_files.append(file_path)
    
    print(f"\n验证 {len(html_files)} 个HTML文件...")
    
    perfect_count = 0
    issues_count = 0
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # 检查DOCTYPE
            if not content.strip().startswith('<!DOCTYPE html>'):
                issues.append('缺少DOCTYPE声明')
            
            # 检查基本标签
            if '<html' not in content:
                issues.append('缺少html标签')
            if '<head>' not in content:
                issues.append('缺少head标签')
            if '<body' not in content:
                issues.append('缺少body标签')
            
            # 检查CSS链接
            if 'style.css' in content:
                css_path = calculate_relative_path(file_path, os.path.join(root_dir, 'css', 'style.css'))
                if css_path not in content:
                    issues.append(f'CSS路径可能错误，应为: {css_path}')
            
            if not issues:
                perfect_count += 1
                print(f"✓ 完美: {rel_path}")
            else:
                issues_count += 1
                print(f"✗ 问题: {rel_path}")
                for issue in issues:
                    print(f"  - {issue}")
                    
        except Exception as e:
            issues_count += 1
            print(f"✗ 错误: {rel_path} - {e}")
    
    print(f"\n验证结果:")
    print(f"- 完美文件: {perfect_count}")
    print(f"- 问题文件: {issues_count}")
    print(f"- 总文件数: {len(html_files)}")
    
    if issues_count == 0:
        print("\n🎉 所有HTML文件都完美！")
    
    return perfect_count, issues_count

if __name__ == "__main__":
    # 获取当前脚本所在目录的上级目录作为根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    print(f"开始全面修复HTML文件...")
    print(f"根目录: {root_dir}")
    print("=" * 50)
    
    # 执行修复
    fixed_count, total_issues = scan_and_fix_all_html_files(root_dir)
    
    print("\n" + "=" * 50)
    
    # 验证结果
    verify_all_files(root_dir)