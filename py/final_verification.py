#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证脚本 - 全面检查所有HTML文件的完整性和一致性
"""

import os
import re
from pathlib import Path

def calculate_relative_path(file_path, target_file):
    """计算从当前文件到目标文件的相对路径"""
    file_dir = os.path.dirname(file_path)
    rel_path = os.path.relpath(target_file, file_dir)
    return rel_path.replace('\\', '/')

def verify_html_file(file_path, root_dir):
    """验证单个HTML文件的完整性"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        warnings = []
        
        # 1. 检查DOCTYPE声明
        if not content.strip().startswith('<!DOCTYPE html>'):
            issues.append('缺少DOCTYPE声明')
        
        # 2. 检查基本HTML结构
        if '<html' not in content:
            issues.append('缺少<html>标签')
        elif 'lang="zh-CN"' not in content:
            warnings.append('建议添加lang="zh-CN"属性')
        
        if '<head>' not in content:
            issues.append('缺少<head>标签')
        
        if '<body' not in content:
            issues.append('缺少<body>标签')
        
        # 3. 检查meta标签
        if '<meta charset="UTF-8">' not in content:
            issues.append('缺少UTF-8字符集声明')
        
        if 'viewport' not in content:
            warnings.append('建议添加viewport meta标签')
        
        # 4. 检查CSS引用
        expected_css_path = calculate_relative_path(file_path, os.path.join(root_dir, 'css', 'style.css'))
        
        if 'style.css' in content:
            if expected_css_path not in content:
                issues.append(f'CSS路径错误，应为: {expected_css_path}')
        else:
            warnings.append('未找到CSS样式引用')
        
        # 5. 检查返回首页按钮
        expected_index_path = calculate_relative_path(file_path, os.path.join(root_dir, 'index.html'))
        
        if '返回首页' in content or 'home-button' in content:
            if expected_index_path not in content and 'index.html' in content:
                issues.append(f'首页链接路径错误，应为: {expected_index_path}')
        
        # 6. 检查标题
        title_match = re.search(r'<title>(.*?)</title>', content)
        if not title_match:
            warnings.append('缺少页面标题')
        elif title_match.group(1).strip() == '页面标题':
            warnings.append('使用默认标题，建议自定义')
        
        # 7. 检查结构完整性
        if '<html' in content and '</html>' not in content:
            issues.append('缺少</html>结束标签')
        
        if '<head>' in content and '</head>' not in content:
            issues.append('缺少</head>结束标签')
        
        if '<body' in content and '</body>' not in content:
            issues.append('缺少</body>结束标签')
        
        # 8. 检查重复标签
        html_count = content.count('<html')
        head_count = content.count('<head>')
        body_count = content.count('<body')
        
        if html_count > 1:
            issues.append(f'发现{html_count}个<html>标签，应该只有1个')
        if head_count > 1:
            issues.append(f'发现{head_count}个<head>标签，应该只有1个')
        if body_count > 1:
            issues.append(f'发现{body_count}个<body>标签，应该只有1个')
        
        return issues, warnings
        
    except Exception as e:
        return [f"读取文件错误: {e}"], []

def verify_all_html_files(root_dir):
    """验证所有HTML文件"""
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
    
    print(f"验证 {len(html_files)} 个HTML文件...")
    print("=" * 60)
    
    perfect_count = 0
    warning_count = 0
    error_count = 0
    
    total_issues = 0
    total_warnings = 0
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        issues, warnings = verify_html_file(file_path, root_dir)
        
        if not issues and not warnings:
            perfect_count += 1
            print(f"✓ 完美: {rel_path}")
        elif issues:
            error_count += 1
            total_issues += len(issues)
            print(f"✗ 错误: {rel_path}")
            for issue in issues:
                print(f"  - ❌ {issue}")
            for warning in warnings:
                print(f"  - ⚠️  {warning}")
        else:
            warning_count += 1
            total_warnings += len(warnings)
            print(f"⚠️  警告: {rel_path}")
            for warning in warnings:
                print(f"  - ⚠️  {warning}")
    
    print("\n" + "=" * 60)
    print("验证结果汇总:")
    print(f"- 完美文件: {perfect_count}")
    print(f"- 警告文件: {warning_count} (共{total_warnings}个警告)")
    print(f"- 错误文件: {error_count} (共{total_issues}个错误)")
    print(f"- 总文件数: {len(html_files)}")
    
    if error_count == 0 and warning_count == 0:
        print("\n🎉 所有HTML文件都完美无缺！")
    elif error_count == 0:
        print("\n✅ 所有HTML文件结构正确，仅有少量建议性警告")
    else:
        print(f"\n❌ 发现 {error_count} 个文件存在错误，需要修复")
    
    return perfect_count, warning_count, error_count

def generate_summary_report(root_dir):
    """生成项目HTML文件概况报告"""
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                html_files.append(file_path)
    
    # 按目录分类统计
    categories = {
        '根目录': [],
        'Python基础': [],
        '数据分析': [],
        '金融应用': [],
        '高级主题': []
    }
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        
        if '\\' not in rel_path:  # 根目录文件
            categories['根目录'].append(rel_path)
        elif 'part1_python_basics' in rel_path:
            categories['Python基础'].append(rel_path)
        elif 'part2_data_analysis' in rel_path:
            categories['数据分析'].append(rel_path)
        elif 'part3_finance_applications' in rel_path:
            categories['金融应用'].append(rel_path)
        elif 'part4_advanced_topics' in rel_path:
            categories['高级主题'].append(rel_path)
    
    print("\n" + "=" * 60)
    print("项目HTML文件概况:")
    print("=" * 60)
    
    total_files = 0
    for category, files in categories.items():
        if files:
            print(f"\n{category}: {len(files)} 个文件")
            total_files += len(files)
            # 只显示前5个文件，避免输出过长
            for i, file in enumerate(files[:5]):
                print(f"  - {file}")
            if len(files) > 5:
                print(f"  - ... 还有 {len(files) - 5} 个文件")
    
    print(f"\n总计: {total_files} 个HTML文件")

if __name__ == "__main__":
    # 获取当前脚本所在目录的上级目录作为根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    print(f"开始最终验证...")
    print(f"根目录: {root_dir}")
    
    # 生成概况报告
    generate_summary_report(root_dir)
    
    # 执行验证
    perfect_count, warning_count, error_count = verify_all_html_files(root_dir)
    
    print("\n" + "=" * 60)
    print("最终验证完成！")
    
    if error_count == 0:
        print("✅ 所有HTML文件结构完整，可以正常使用")
    else:
        print("❌ 部分文件需要进一步修复")