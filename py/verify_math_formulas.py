#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证HTML文件中的数学公式显示情况
"""

import os
import re
from pathlib import Path

def has_math_formulas(content):
    """检查文件是否包含数学公式"""
    latex_patterns = [
        r'\\\[.*?\\\]',  # 块级公式 \[...\]
        r'\\\(.*?\\\)',  # 行内公式 \(...\)
    ]
    
    formulas = []
    for pattern in latex_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        formulas.extend(matches)
    
    return formulas

def has_mathjax(content):
    """检查文件是否已经引入了MathJax"""
    mathjax_patterns = [
        r'mathjax',
        r'MathJax',
        r'tex-mml-chtml\.js'
    ]
    
    for pattern in mathjax_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False

def analyze_html_file(file_path):
    """分析单个HTML文件的数学公式情况"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        formulas = has_math_formulas(content)
        has_mathjax_support = has_mathjax(content)
        
        return {
            'file': str(file_path),
            'has_formulas': len(formulas) > 0,
            'formula_count': len(formulas),
            'formulas': formulas[:5],  # 只显示前5个公式作为示例
            'has_mathjax': has_mathjax_support,
            'status': 'OK' if (len(formulas) == 0 or has_mathjax_support) else 'MISSING_MATHJAX'
        }
        
    except Exception as e:
        return {
            'file': str(file_path),
            'error': str(e),
            'status': 'ERROR'
        }

def find_html_files(base_dir):
    """查找所有HTML文件"""
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        # 跳过py目录
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    
    return html_files

def main():
    """主函数"""
    base_dir = Path('c:/Users/Administrator/Desktop/测试')
    
    print("正在分析所有HTML文件的数学公式显示情况...")
    print("=" * 60)
    
    html_files = find_html_files(base_dir)
    results = []
    
    for file_path in html_files:
        result = analyze_html_file(file_path)
        results.append(result)
    
    # 统计信息
    total_files = len(results)
    files_with_formulas = sum(1 for r in results if r.get('has_formulas', False))
    files_with_mathjax = sum(1 for r in results if r.get('has_mathjax', False))
    missing_mathjax = sum(1 for r in results if r.get('status') == 'MISSING_MATHJAX')
    error_files = sum(1 for r in results if r.get('status') == 'ERROR')
    
    print(f"📊 统计信息:")
    print(f"   总HTML文件数: {total_files}")
    print(f"   包含数学公式的文件: {files_with_formulas}")
    print(f"   已引入MathJax的文件: {files_with_mathjax}")
    print(f"   缺少MathJax支持的文件: {missing_mathjax}")
    print(f"   处理出错的文件: {error_files}")
    print()
    
    # 显示包含数学公式的文件详情
    print("📝 包含数学公式的文件详情:")
    print("-" * 60)
    
    for result in results:
        if result.get('has_formulas', False):
            status_icon = "✅" if result['status'] == 'OK' else "❌"
            relative_path = result['file'].replace(str(base_dir), '').lstrip('\\/')
            
            print(f"{status_icon} {relative_path}")
            print(f"   公式数量: {result['formula_count']}")
            print(f"   MathJax支持: {'是' if result['has_mathjax'] else '否'}")
            
            if result['formulas']:
                print(f"   示例公式:")
                for i, formula in enumerate(result['formulas'][:3], 1):
                    # 清理公式显示
                    clean_formula = formula.replace('\\[', '').replace('\\]', '').replace('\\(', '').replace('\\)', '').strip()
                    if len(clean_formula) > 50:
                        clean_formula = clean_formula[:50] + '...'
                    print(f"     {i}. {clean_formula}")
            print()
    
    # 显示需要修复的文件
    if missing_mathjax > 0:
        print("⚠️  需要添加MathJax支持的文件:")
        print("-" * 60)
        for result in results:
            if result.get('status') == 'MISSING_MATHJAX':
                relative_path = result['file'].replace(str(base_dir), '').lstrip('\\/')
                print(f"   {relative_path}")
        print()
    
    # 显示错误文件
    if error_files > 0:
        print("❌ 处理出错的文件:")
        print("-" * 60)
        for result in results:
            if result.get('status') == 'ERROR':
                relative_path = result['file'].replace(str(base_dir), '').lstrip('\\/')
                print(f"   {relative_path}: {result.get('error', '未知错误')}")
        print()
    
    # 总结
    if missing_mathjax == 0 and error_files == 0:
        print("🎉 所有包含数学公式的HTML文件都已正确配置MathJax支持！")
    else:
        print(f"📋 总结: 发现 {missing_mathjax} 个文件需要添加MathJax支持，{error_files} 个文件处理出错。")

if __name__ == '__main__':
    main()