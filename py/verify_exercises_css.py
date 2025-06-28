#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证exercises.html文件的CSS样式引用状态
检查所有exercises.html文件是否正确引用了style.css
"""

import os
from pathlib import Path

def verify_exercises_css():
    """
    验证所有exercises.html文件的CSS引用状态
    """
    # 项目根目录
    project_root = Path(r'c:\Users\Administrator\Desktop\测试')
    
    # 查找所有exercises.html文件
    exercises_files = list(project_root.rglob('exercises.html'))
    
    print(f"找到 {len(exercises_files)} 个exercises.html文件\n")
    
    has_css_count = 0
    missing_css_count = 0
    
    for file_path in exercises_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查CSS引用
            has_style_css = 'style.css' in content
            has_head_tag = '<head>' in content
            has_closing_head = '</head>' in content
            
            relative_path = file_path.relative_to(project_root)
            
            if has_style_css:
                print(f"✅ {relative_path} - 已有CSS引用")
                has_css_count += 1
            else:
                print(f"❌ {relative_path} - 缺少CSS引用")
                missing_css_count += 1
            
            # 检查HTML结构
            if not has_head_tag:
                print(f"   ⚠️  缺少<head>标签")
            elif not has_closing_head:
                print(f"   ⚠️  缺少</head>标签")
                
        except Exception as e:
            print(f"❌ 读取文件 {file_path} 时出错: {e}")
    
    print(f"\n📊 统计结果:")
    print(f"   ✅ 已有CSS引用: {has_css_count} 个文件")
    print(f"   ❌ 缺少CSS引用: {missing_css_count} 个文件")
    
    if missing_css_count == 0:
        print(f"\n🎉 所有exercises.html文件都已正确引用CSS样式！")
    else:
        print(f"\n⚠️  还有 {missing_css_count} 个文件需要添加CSS引用。")

if __name__ == '__main__':
    verify_exercises_css()