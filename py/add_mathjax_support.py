#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为包含数学公式的HTML文件添加MathJax支持
"""

import os
import re
from pathlib import Path

def has_math_formulas(content):
    """检查文件是否包含数学公式"""
    # 检查LaTeX格式的数学公式
    latex_patterns = [
        r'\\\[.*?\\\]',  # 块级公式 \[...\]
        r'\\\(.*?\\\)',  # 行内公式 \(...\)
    ]
    
    for pattern in latex_patterns:
        if re.search(pattern, content, re.DOTALL):
            return True
    return False

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

def add_mathjax_to_file(file_path):
    """为HTML文件添加MathJax支持"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否需要添加MathJax
        if not has_math_formulas(content):
            print(f"跳过 {file_path} - 没有数学公式")
            return False
            
        if has_mathjax(content):
            print(f"跳过 {file_path} - 已有MathJax支持")
            return False
        
        # 查找</head>标签的位置
        head_end_match = re.search(r'</head>', content, re.IGNORECASE)
        if not head_end_match:
            print(f"警告：{file_path} 中未找到</head>标签")
            return False
        
        # 准备要插入的MathJax脚本
        mathjax_scripts = '''    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'''
        
        # 在</head>之前插入MathJax脚本
        head_end_pos = head_end_match.start()
        new_content = content[:head_end_pos] + mathjax_scripts + '\n' + content[head_end_pos:]
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ 已为 {file_path} 添加MathJax支持")
        return True
        
    except Exception as e:
        print(f"错误：处理 {file_path} 时出现异常 - {e}")
        return False

def main():
    """主函数"""
    # 需要处理的HTML文件列表（从搜索结果中提取）
    html_files = [
        'part3_finance_applications/module11/lesson1.html',
        'deep_learning_finance.html',
        'part3_finance_applications/module9/lesson1.html',
        'part3_finance_applications/module10/lesson1.html',
        'part3_finance_applications/module12/lesson1.html',
        'part2_data_analysis/module8/lesson1.html',
        'part4_advanced_topics/module14/lesson1.html',
        'part4_advanced_topics/module15/lesson1.html',
        'part4_advanced_topics/module13/lesson1.html'
    ]
    
    base_dir = Path('c:/Users/Administrator/Desktop/测试')
    processed_count = 0
    
    print("开始为HTML文件添加MathJax支持...")
    print("=" * 50)
    
    for file_path in html_files:
        full_path = base_dir / file_path
        if full_path.exists():
            if add_mathjax_to_file(full_path):
                processed_count += 1
        else:
            print(f"警告：文件不存在 - {full_path}")
    
    print("=" * 50)
    print(f"处理完成！共为 {processed_count} 个文件添加了MathJax支持")

if __name__ == '__main__':
    main()