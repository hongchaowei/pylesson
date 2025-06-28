#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证exercises.html文件中返回首页按钮的状态
确保每个文件只有一个返回首页按钮
"""

import os
import re
from pathlib import Path

def verify_exercises_buttons():
    """
    验证exercises.html文件中返回首页按钮的状态
    """
    # 项目根目录
    project_root = Path(r'c:\Users\Administrator\Desktop\测试')
    
    # 查找所有exercises.html文件
    exercises_files = list(project_root.rglob('exercises.html'))
    
    print(f"找到 {len(exercises_files)} 个exercises.html文件\n")
    
    for file_path in exercises_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查HTML返回首页按钮
            html_buttons = re.findall(r'<a[^>]*href="[^"]*index\.html"[^>]*>.*?返回首页.*?</a>', content, re.DOTALL)
            
            # 检查JavaScript动态创建的按钮
            js_buttons = re.findall(r'btn\.textContent\s*=\s*[\'"]返回测试首页[\'"]', content)
            
            # 检查其他可能的首页链接
            other_home_links = re.findall(r'首页|home.*button|返回.*首页', content, re.IGNORECASE)
            
            print(f"📁 {file_path.relative_to(project_root)}")
            print(f"   HTML返回首页按钮: {len(html_buttons)} 个")
            print(f"   JavaScript动态按钮: {len(js_buttons)} 个")
            print(f"   其他首页相关内容: {len(other_home_links)} 个")
            
            if len(html_buttons) == 1 and len(js_buttons) == 0:
                print(f"   ✅ 状态正常：只有一个HTML返回首页按钮")
            elif len(html_buttons) > 1 or len(js_buttons) > 0:
                print(f"   ⚠️  可能存在重复按钮")
            else:
                print(f"   ❓ 未找到返回首页按钮")
            
            print()
                
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {e}")
    
    print("🎉 验证完成！")

if __name__ == '__main__':
    verify_exercises_buttons()