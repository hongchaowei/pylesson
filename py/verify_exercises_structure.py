#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证exercises.html文件结构是否与lesson.html保持一致
检查HTML结构、CSS引用、JavaScript引用等关键元素
"""

import os
from pathlib import Path

def verify_exercises_structure():
    """
    验证所有exercises.html文件的结构是否标准化
    """
    # 项目根目录
    project_root = Path(r'c:\Users\Administrator\Desktop\测试')
    
    # 查找所有exercises.html文件
    exercises_files = list(project_root.rglob('exercises.html'))
    
    print(f"找到 {len(exercises_files)} 个exercises.html文件\n")
    
    all_good = True
    
    for file_path in exercises_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = file_path.relative_to(project_root)
            issues = []
            
            # 检查关键结构元素
            checks = {
                'CSS引用': 'style.css' in content,
                'JavaScript引用': 'components.js' in content,
                'Body标签': '<body>' in content,
                'Header结构': '<header>' in content and '<div class="container">' in content,
                'Home按钮': 'home-button-container' in content,
                'Main容器': '<main class="container">' in content,
                'Lesson内容区': 'lesson-content' in content,
                '代码高亮': 'highlight.js' in content,
                '高亮初始化': 'hljs.highlightAll()' in content if 'highlight.js' in content else True,
                '结束标签': '</body>' in content and '</html>' in content
            }
            
            # 收集问题
            for check_name, passed in checks.items():
                if not passed:
                    issues.append(check_name)
            
            # 输出结果
            if issues:
                print(f"❌ {relative_path}")
                for issue in issues:
                    print(f"   ⚠️  缺少: {issue}")
                all_good = False
            else:
                print(f"✅ {relative_path} - 结构完整")
                
        except Exception as e:
            print(f"❌ 读取文件 {file_path} 时出错: {e}")
            all_good = False
    
    print(f"\n📊 验证结果:")
    if all_good:
        print(f"🎉 所有exercises.html文件结构都已标准化，与lesson.html保持一致！")
    else:
        print(f"⚠️  部分文件仍需修复。")

if __name__ == '__main__':
    verify_exercises_structure()