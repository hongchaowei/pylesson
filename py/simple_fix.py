#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单直接的HTML修复脚本
"""

import os
import re
from pathlib import Path

def fix_html_file(file_path):
    """
    修复单个HTML文件
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 确保有DOCTYPE
        if not content.strip().startswith('<!DOCTYPE html>'):
            content = '<!DOCTYPE html>\n' + content
        
        # 2. 移除重复的DOCTYPE
        while content.count('<!DOCTYPE html>') > 1:
            # 找到第二个DOCTYPE的位置并移除
            first_pos = content.find('<!DOCTYPE html>')
            second_pos = content.find('<!DOCTYPE html>', first_pos + 1)
            if second_pos != -1:
                # 移除第二个DOCTYPE
                content = content[:second_pos] + content[second_pos + 15:]
        
        # 3. 移除重复的html标签
        html_tags = re.findall(r'<html[^>]*>', content, re.IGNORECASE)
        if len(html_tags) > 1:
            # 保留第一个，移除其他
            for i in range(1, len(html_tags)):
                content = content.replace(html_tags[i], '', 1)
        
        # 4. 移除重复的head标签
        while content.count('<head>') > 1:
            # 找到第二个head标签的位置
            first_head = content.find('<head>')
            second_head = content.find('<head>', first_head + 1)
            if second_head != -1:
                # 找到对应的</head>
                head_end = content.find('</head>', second_head)
                if head_end != -1:
                    # 移除整个第二个head块
                    content = content[:second_head] + content[head_end + 7:]
                else:
                    # 如果没有找到结束标签，只移除开始标签
                    content = content[:second_head] + content[second_head + 6:]
        
        # 5. 移除重复的body标签
        body_tags = re.findall(r'<body[^>]*>', content, re.IGNORECASE)
        if len(body_tags) > 1:
            # 保留第一个，移除其他
            for i in range(1, len(body_tags)):
                content = content.replace(body_tags[i], '', 1)
        
        # 6. 移除重复的</html>标签
        while content.count('</html>') > 1:
            last_pos = content.rfind('</html>')
            second_last_pos = content.rfind('</html>', 0, last_pos)
            if second_last_pos != -1:
                content = content[:second_last_pos] + content[second_last_pos + 7:]
        
        # 7. 移除重复的</body>标签
        while content.count('</body>') > 1:
            last_pos = content.rfind('</body>')
            second_last_pos = content.rfind('</body>', 0, last_pos)
            if second_last_pos != -1:
                content = content[:second_last_pos] + content[second_last_pos + 7:]
        
        # 8. 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 如果内容有变化，保存文件
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
    
    print(f"简单修复 {len(html_files)} 个HTML文件...\n")
    
    fixed_count = 0
    
    for file_path in html_files:
        if fix_html_file(file_path):
            relative_path = str(file_path.relative_to(project_root))
            print(f"✅ 已修复: {relative_path}")
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
            
            if 'home-button' not in content and file_path.name != 'index.html':
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
        for issue in issues[:10]:  # 显示前10个
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... 还有 {len(issues) - 10} 个问题")
    
    if len(issues) == 0:
        print("\n🎉 所有HTML文件UI风格已完全统一！")
        print("✅ 所有文件都具备：")
        print("   - 标准的HTML5 DOCTYPE声明")
        print("   - 正确的html、head、body标签结构")
        print("   - 统一的CSS样式引用")
        print("   - 返回首页按钮（非首页文件）")
        print("   - 标准的header结构（非首页文件）")
        print("   - 清洁的HTML文档结构")
        print("   - 无重复标签和引用")
    else:
        print(f"\n⚠️  还有 {len(issues)} 个问题需要处理")

if __name__ == "__main__":
    print("=" * 60)
    print("简单直接的HTML修复")
    print("=" * 60)
    
    main()