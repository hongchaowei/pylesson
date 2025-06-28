#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除HTML文件中的重复内容
"""

import os
import re
from pathlib import Path

def remove_duplicates_from_file(file_path):
    """
    移除单个文件中的重复内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 移除重复的script标签
        script_pattern = r'<script[^>]*src="[^"]+"[^>]*></script>'
        scripts = re.findall(script_pattern, content)
        unique_scripts = list(dict.fromkeys(scripts))  # 保持顺序去重
        
        # 替换所有script标签
        content = re.sub(script_pattern, '', content)
        
        # 移除重复的内联script
        inline_script_pattern = r'<script[^>]*>\s*hljs\.highlightAll\(\);?\s*</script>'
        inline_scripts = re.findall(inline_script_pattern, content)
        if inline_scripts:
            content = re.sub(inline_script_pattern, '', content)
            unique_scripts.append(inline_scripts[0])  # 只保留一个
        
        # 移除重复的link标签
        link_pattern = r'<link[^>]*href="[^"]+"[^>]*>'
        links = re.findall(link_pattern, content)
        unique_links = list(dict.fromkeys(links))  # 保持顺序去重
        
        # 替换所有link标签
        content = re.sub(link_pattern, '', content)
        
        # 在head结束前重新插入唯一的links和scripts
        head_end = content.find('</head>')
        if head_end != -1:
            insert_content = ''
            if unique_links:
                insert_content += '\n    ' + '\n    '.join(unique_links)
            if unique_scripts:
                insert_content += '\n    ' + '\n    '.join(unique_scripts)
            
            content = content[:head_end] + insert_content + '\n' + content[head_end:]
        
        # 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # 只有内容真的改变了才写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """
    主函数
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"移除 {len(html_files)} 个HTML文件中的重复内容...\n")
    
    changed_count = 0
    
    for file_path in html_files:
        if remove_duplicates_from_file(file_path):
            relative_path = str(file_path.relative_to(project_root))
            print(f"✅ 已清理重复内容: {relative_path}")
            changed_count += 1
    
    print(f"\n🎉 完成！共修改了 {changed_count} 个文件")
    
    # 验证结果
    print("\n" + "=" * 50)
    print("验证清理结果")
    print("=" * 50)
    
    verify_cleanup()

def verify_cleanup():
    """
    验证清理结果
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"验证 {len(html_files)} 个HTML文件...\n")
    
    issues = []
    perfect_files = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(project_root))
            file_issues = []
            
            # 检查基本结构
            if not content.strip().startswith('<!DOCTYPE html>'):
                file_issues.append('缺少DOCTYPE')
            
            if content.count('<!DOCTYPE html>') > 1:
                file_issues.append('重复DOCTYPE')
            
            html_count = len(re.findall(r'<html[^>]*>', content))
            if html_count != 1:
                file_issues.append(f'html标签数量异常({html_count})')
            
            head_count = len(re.findall(r'<head[^>]*>', content))
            if head_count != 1:
                file_issues.append(f'head标签数量异常({head_count})')
            
            body_count = len(re.findall(r'<body[^>]*>', content))
            if body_count != 1:
                file_issues.append(f'body标签数量异常({body_count})')
            
            # 检查重复的script
            scripts = re.findall(r'<script[^>]*src="[^"]+"[^>]*></script>', content)
            if len(scripts) != len(set(scripts)):
                file_issues.append('重复script标签')
            
            # 检查重复的link
            links = re.findall(r'<link[^>]*href="[^"]+"[^>]*>', content)
            if len(links) != len(set(links)):
                file_issues.append('重复link标签')
            
            if 'style.css' not in content:
                file_issues.append('缺少CSS')
            
            if 'home-button' not in content:
                file_issues.append('缺少返回按钮')
            
            if '<header>' not in content and file_path.name != 'index.html':
                file_issues.append('缺少header')
            
            if file_issues:
                issues.append(f"{relative_path}: {', '.join(file_issues)}")
            else:
                perfect_files += 1
                
        except Exception as e:
            issues.append(f"{relative_path}: 读取错误 - {e}")
    
    # 显示结果
    if issues:
        print(f"❌ 发现 {len(issues)} 个文件有问题:")
        for issue in issues[:3]:  # 只显示前3个
            print(f"   - {issue}")
        if len(issues) > 3:
            print(f"   ... 还有 {len(issues) - 3} 个问题")
    
    print(f"\n✅ 完美的文件: {perfect_files} 个")
    print(f"❌ 有问题的文件: {len(issues)} 个")
    
    if len(issues) == 0:
        print("\n🎉 所有HTML文件UI风格已完全统一！")
        print("✅ 所有文件都具备：")
        print("   - 标准的HTML5 DOCTYPE声明")
        print("   - 正确的html、head、body标签结构")
        print("   - 统一的CSS样式引用")
        print("   - 无重复的script和link标签")
        print("   - 返回首页按钮")
        print("   - 标准的header结构（非首页）")
        print("   - 清洁的HTML文档结构")

if __name__ == "__main__":
    print("=" * 60)
    print("移除HTML文件重复内容")
    print("=" * 60)
    
    main()