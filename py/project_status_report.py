#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目状态报告生成器
生成详细的HTML文件状态和项目结构报告
"""

import os
import re
from datetime import datetime

def analyze_project_structure(root_dir):
    """分析项目结构"""
    structure = {
        '根目录文件': [],
        'Python基础模块': {},
        '数据分析模块': {},
        '金融应用模块': {},
        '高级主题模块': {},
        '其他目录': []
    }
    
    # 统计各类文件
    file_stats = {
        'html': 0,
        'css': 0,
        'js': 0,
        'py': 0,
        'md': 0,
        'other': 0
    }
    
    for root, dirs, files in os.walk(root_dir):
        rel_root = os.path.relpath(root, root_dir)
        
        # 跳过py目录的详细分析
        if 'py' in rel_root:
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext == '.html':
                file_stats['html'] += 1
            elif ext == '.css':
                file_stats['css'] += 1
            elif ext == '.js':
                file_stats['js'] += 1
            elif ext == '.py':
                file_stats['py'] += 1
            elif ext == '.md':
                file_stats['md'] += 1
            else:
                file_stats['other'] += 1
            
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir)
            
            if file.endswith('.html'):
                if rel_root == '.':
                    structure['根目录文件'].append(file)
                elif 'part1_python_basics' in rel_root:
                    module_match = re.search(r'module(\d+)', rel_root)
                    if module_match:
                        module_num = module_match.group(1)
                        if module_num not in structure['Python基础模块']:
                            structure['Python基础模块'][module_num] = []
                        structure['Python基础模块'][module_num].append(file)
                elif 'part2_data_analysis' in rel_root:
                    module_match = re.search(r'module(\d+)', rel_root)
                    if module_match:
                        module_num = module_match.group(1)
                        if module_num not in structure['数据分析模块']:
                            structure['数据分析模块'][module_num] = []
                        structure['数据分析模块'][module_num].append(file)
                elif 'part3_finance_applications' in rel_root:
                    module_match = re.search(r'module(\d+)', rel_root)
                    if module_match:
                        module_num = module_match.group(1)
                        if module_num not in structure['金融应用模块']:
                            structure['金融应用模块'][module_num] = []
                        structure['金融应用模块'][module_num].append(file)
                elif 'part4_advanced_topics' in rel_root:
                    module_match = re.search(r'module(\d+)', rel_root)
                    if module_match:
                        module_num = module_match.group(1)
                        if module_num not in structure['高级主题模块']:
                            structure['高级主题模块'][module_num] = []
                        structure['高级主题模块'][module_num].append(file)
    
    return structure, file_stats

def check_html_quality(root_dir):
    """检查HTML文件质量"""
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                html_files.append(file_path)
    
    quality_stats = {
        'perfect': 0,
        'warnings': 0,
        'errors': 0,
        'total': len(html_files)
    }
    
    issues_summary = {
        '缺少DOCTYPE': 0,
        '缺少基本标签': 0,
        'CSS路径错误': 0,
        '首页链接错误': 0,
        '默认标题': 0,
        '其他问题': 0
    }
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_issues = []
            file_warnings = []
            
            # 检查各种问题
            if not content.strip().startswith('<!DOCTYPE html>'):
                file_issues.append('缺少DOCTYPE')
                issues_summary['缺少DOCTYPE'] += 1
            
            if '<html' not in content or '<head>' not in content or '<body' not in content:
                file_issues.append('缺少基本标签')
                issues_summary['缺少基本标签'] += 1
            
            # 检查标题
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match and title_match.group(1).strip() == '页面标题':
                file_warnings.append('默认标题')
                issues_summary['默认标题'] += 1
            
            # 分类文件质量
            if file_issues:
                quality_stats['errors'] += 1
            elif file_warnings:
                quality_stats['warnings'] += 1
            else:
                quality_stats['perfect'] += 1
                
        except Exception as e:
            quality_stats['errors'] += 1
            issues_summary['其他问题'] += 1
    
    return quality_stats, issues_summary

def generate_report(root_dir):
    """生成完整的项目状态报告"""
    print("=" * 80)
    print("                    项目状态报告")
    print("=" * 80)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"项目路径: {root_dir}")
    print()
    
    # 分析项目结构
    structure, file_stats = analyze_project_structure(root_dir)
    
    print("📁 项目文件统计")
    print("-" * 40)
    print(f"HTML文件: {file_stats['html']} 个")
    print(f"CSS文件:  {file_stats['css']} 个")
    print(f"JS文件:   {file_stats['js']} 个")
    print(f"Python脚本: {file_stats['py']} 个")
    print(f"Markdown文件: {file_stats['md']} 个")
    print(f"其他文件: {file_stats['other']} 个")
    print(f"总计: {sum(file_stats.values())} 个文件")
    print()
    
    print("📚 课程结构概览")
    print("-" * 40)
    
    # 根目录文件
    if structure['根目录文件']:
        print(f"根目录: {len(structure['根目录文件'])} 个HTML文件")
        for file in structure['根目录文件']:
            print(f"  - {file}")
        print()
    
    # 各部分模块
    parts = [
        ('Python基础', structure['Python基础模块']),
        ('数据分析', structure['数据分析模块']),
        ('金融应用', structure['金融应用模块']),
        ('高级主题', structure['高级主题模块'])
    ]
    
    for part_name, modules in parts:
        if modules:
            print(f"{part_name}: {len(modules)} 个模块")
            for module_num in sorted(modules.keys(), key=int):
                files = modules[module_num]
                print(f"  模块{module_num}: {len(files)} 个文件 ({', '.join(files)})")
            print()
    
    # HTML质量检查
    quality_stats, issues_summary = check_html_quality(root_dir)
    
    print("✅ HTML文件质量报告")
    print("-" * 40)
    print(f"完美文件: {quality_stats['perfect']} 个 ({quality_stats['perfect']/quality_stats['total']*100:.1f}%)")
    print(f"警告文件: {quality_stats['warnings']} 个 ({quality_stats['warnings']/quality_stats['total']*100:.1f}%)")
    print(f"错误文件: {quality_stats['errors']} 个 ({quality_stats['errors']/quality_stats['total']*100:.1f}%)")
    print(f"总文件数: {quality_stats['total']} 个")
    print()
    
    if any(count > 0 for count in issues_summary.values()):
        print("⚠️  问题分布统计")
        print("-" * 40)
        for issue, count in issues_summary.items():
            if count > 0:
                print(f"{issue}: {count} 个文件")
        print()
    
    # 项目健康度评估
    print("🏥 项目健康度评估")
    print("-" * 40)
    
    health_score = (quality_stats['perfect'] + quality_stats['warnings'] * 0.8) / quality_stats['total'] * 100
    
    if health_score >= 95:
        health_status = "优秀 🌟"
        health_color = "绿色"
    elif health_score >= 85:
        health_status = "良好 ✅"
        health_color = "蓝色"
    elif health_score >= 70:
        health_status = "一般 ⚠️"
        health_color = "黄色"
    else:
        health_status = "需要改进 ❌"
        health_color = "红色"
    
    print(f"健康度评分: {health_score:.1f}/100")
    print(f"健康状态: {health_status}")
    print()
    
    # 建议和总结
    print("💡 建议和总结")
    print("-" * 40)
    
    if quality_stats['errors'] == 0:
        print("✅ 所有HTML文件结构完整，无严重错误")
    else:
        print(f"❌ 发现 {quality_stats['errors']} 个文件存在结构错误，需要修复")
    
    if issues_summary['默认标题'] > 0:
        print(f"📝 建议为 {issues_summary['默认标题']} 个文件自定义页面标题")
    
    if quality_stats['perfect'] == quality_stats['total']:
        print("🎉 恭喜！所有HTML文件都达到完美标准！")
    elif quality_stats['errors'] == 0:
        print("👍 项目整体质量良好，可以正常使用")
    
    print()
    print("📋 维护建议:")
    print("1. 定期运行验证脚本检查文件完整性")
    print("2. 为使用默认标题的页面添加具体的标题")
    print("3. 保持CSS和JS文件的统一引用")
    print("4. 确保所有链接路径的正确性")
    
    print("\n" + "=" * 80)
    print("                    报告结束")
    print("=" * 80)

if __name__ == "__main__":
    # 获取当前脚本所在目录的上级目录作为根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    generate_report(root_dir)