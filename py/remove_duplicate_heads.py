#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除HTML文件中重复的head标签
"""

import os
import re
from pathlib import Path

def fix_duplicate_heads(file_path):
    """
    修复单个文件中重复的head标签
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 检查是否有重复的head标签
        head_count = content.count('<head>')
        if head_count <= 1:
            return False  # 没有重复，无需修改
        
        # 找到所有head标签的位置
        head_starts = []
        head_ends = []
        
        for match in re.finditer(r'<head>', content):
            head_starts.append(match.start())
        
        for match in re.finditer(r'</head>', content):
            head_ends.append(match.end())
        
        if len(head_starts) != len(head_ends):
            print(f"警告: {file_path} 中head标签不匹配")
            return False
        
        # 提取第一个head的内容
        if len(head_starts) > 0 and len(head_ends) > 0:
            first_head_content = content[head_starts[0]:head_ends[0]]
            
            # 从其他head标签中提取额外内容
            additional_content = []
            for i in range(1, len(head_starts)):
                head_content = content[head_starts[i]:head_ends[i]]
                # 提取head标签内的内容（不包括<head>和</head>）
                inner_content = head_content[6:-7].strip()  # 去掉<head>和</head>
                if inner_content:
                    additional_content.append(inner_content)
            
            # 合并内容到第一个head中
            if additional_content:
                # 在第一个head的</head>前插入额外内容
                insert_pos = first_head_content.rfind('</head>')
                if insert_pos != -1:
                    merged_content = (first_head_content[:insert_pos] + 
                                    '\n    ' + '\n    '.join(additional_content) + 
                                    '\n' + first_head_content[insert_pos:])
                else:
                    merged_content = first_head_content
            else:
                merged_content = first_head_content
            
            # 移除所有head标签
            new_content = content
            for i in range(len(head_starts) - 1, -1, -1):  # 从后往前删除
                new_content = new_content[:head_starts[i]] + new_content[head_ends[i]:]
            
            # 在第一个head的原位置插入合并后的内容
            new_content = new_content[:head_starts[0]] + merged_content + new_content[head_starts[0]:]
            
            # 保存文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
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
    
    print(f"修复 {len(html_files)} 个HTML文件中的重复head标签...\n")
    
    fixed_count = 0
    
    for file_path in html_files:
        if fix_duplicate_heads(file_path):
            relative_path = str(file_path.relative_to(project_root))
            print(f"✅ 已修复重复head: {relative_path}")
            fixed_count += 1
    
    print(f"\n🎉 完成！共修复了 {fixed_count} 个文件")
    
    # 最终验证
    print("\n" + "=" * 50)
    print("最终验证结果")
    print("=" * 50)
    
    verify_all_files()

def verify_all_files():
    """
    验证所有文件
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"验证 {len(html_files)} 个HTML文件...\n")
    
    perfect_files = 0
    issues = []
    
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
                file_issues.append(f'重复DOCTYPE({content.count("<!DOCTYPE html>")})')
            
            if content.count('<html') > 1:
                file_issues.append(f'重复html标签({content.count("<html")})')
            
            if content.count('<head>') > 1:
                file_issues.append(f'重复head标签({content.count("<head>")})')
            
            if content.count('<body>') > 1:
                file_issues.append(f'重复body标签({content.count("<body>")})')
            
            if content.count('<head>') == 0:
                file_issues.append('缺少head标签')
            
            if content.count('<body>') == 0:
                file_issues.append('缺少body标签')
            
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
    print(f"✅ 完美的文件: {perfect_files} 个")
    print(f"❌ 有问题的文件: {len(issues)} 个")
    
    if issues:
        print(f"\n问题详情:")
        for issue in issues[:5]:  # 显示前5个
            print(f"   - {issue}")
        if len(issues) > 5:
            print(f"   ... 还有 {len(issues) - 5} 个问题")
    
    if len(issues) == 0:
        print("\n🎉 所有HTML文件UI风格已完全统一！")
        print("✅ 所有文件都具备：")
        print("   - 标准的HTML5 DOCTYPE声明")
        print("   - 正确的html、head、body标签结构")
        print("   - 统一的CSS样式引用")
        print("   - 返回首页按钮")
        print("   - 标准的header结构（非首页）")
        print("   - 清洁的HTML文档结构")
        print("   - 无重复标签和引用")
    else:
        print(f"\n⚠️  还有 {len(issues)} 个问题需要处理")

if __name__ == "__main__":
    print("=" * 60)
    print("移除重复head标签")
    print("=" * 60)
    
    main()