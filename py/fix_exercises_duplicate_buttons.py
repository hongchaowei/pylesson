#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复exercises.html文件中重复的返回首页按钮问题
移除JavaScript动态创建的按钮，保留HTML中的home-button样式按钮
"""

import os
import re
from pathlib import Path

def fix_exercises_duplicate_buttons():
    """
    修复exercises.html文件中重复的返回首页按钮
    """
    # 项目根目录
    project_root = Path(r'c:\Users\Administrator\Desktop\测试')
    
    # 查找所有exercises.html文件
    exercises_files = list(project_root.rglob('exercises.html'))
    
    fixed_count = 0
    
    for file_path in exercises_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否存在JavaScript动态创建按钮的代码
            js_button_pattern = r'<script>\s*document\.addEventListener\([^}]+btn\.textContent\s*=\s*[\'"]返回测试首页[\'"][^}]+}\);\s*</script>'
            
            if re.search(js_button_pattern, content, re.DOTALL):
                # 移除JavaScript动态创建的按钮代码
                new_content = re.sub(js_button_pattern, '', content, flags=re.DOTALL)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ 修复了文件: {file_path}")
                fixed_count += 1
            else:
                print(f"ℹ️  文件无需修复: {file_path}")
                
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {e}")
    
    print(f"\n🎉 修复完成！总共修复了 {fixed_count} 个文件的重复按钮问题。")

if __name__ == '__main__':
    fix_exercises_duplicate_buttons()