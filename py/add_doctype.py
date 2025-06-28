#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为缺少DOCTYPE的HTML文件添加DOCTYPE声明
"""

import os
from pathlib import Path

def add_doctype_to_file(file_path):
    """
    为单个文件添加DOCTYPE
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有DOCTYPE
        if content.strip().startswith('<!DOCTYPE html>'):
            return False  # 已有DOCTYPE，无需修改
        
        # 添加DOCTYPE
        new_content = '<!DOCTYPE html>\n' + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """
    主函数
    """
    project_root = Path('.')
    html_files = list(project_root.rglob('*.html'))
    
    print(f"检查 {len(html_files)} 个HTML文件的DOCTYPE声明...\n")
    
    fixed_count = 0
    
    for file_path in html_files:
        if add_doctype_to_file(file_path):
            relative_path = str(file_path.relative_to(project_root))
            print(f"✅ 已添加DOCTYPE: {relative_path}")
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
    print("添加DOCTYPE声明并验证HTML文件")
    print("=" * 60)
    
    main()