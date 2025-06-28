#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一所有HTML文件的导航条
删除原有的不同导航条和返回首页按钮，替换为统一的导航条
"""

import os
import re
from pathlib import Path

def get_relative_path_to_root(file_path, root_dir):
    """计算从文件到根目录的相对路径"""
    file_path = Path(file_path)
    root_dir = Path(root_dir)
    
    # 计算相对路径
    try:
        rel_path = os.path.relpath(root_dir, file_path.parent)
        if rel_path == '.':
            return './'
        else:
            return rel_path.replace('\\', '/') + '/'
    except ValueError:
        return './'

def create_navigation_html(relative_path_to_root):
    """创建统一的导航条HTML"""
    nav_html = f'''<nav>
        <button class="mobile-menu-toggle" id="menuToggle">☰</button>
        <ul class="nav-menu">
            <li><a href="{relative_path_to_root}index.html" class="active">首页</a></li>
            <li><a href="{relative_path_to_root}syllabus.html">课程大纲</a></li>
            <li><a href="{relative_path_to_root}knowledge_graph.html">知识图谱</a></li>
            <li><a href="{relative_path_to_root}case_studies.html">行业案例</a></li>
            <li class="dropdown">
                <a href="#">Python基础</a>
                <div class="dropdown-content">
                    <a href="{relative_path_to_root}index.html">模块1: Python入门</a>
                    <a href="{relative_path_to_root}index.html">模块2: 数据结构与控制流</a>
                    <a href="{relative_path_to_root}index.html">模块3: 函数与模块</a>
                    <a href="{relative_path_to_root}index.html">模块4: 面向对象编程</a>
                </div>
            </li>
            <li class="dropdown">
                <a href="#">数据分析</a>
                <div class="dropdown-content">
                    <a href="{relative_path_to_root}index.html">模块5: NumPy基础</a>
                    <a href="{relative_path_to_root}index.html">模块6: Pandas数据处理</a>
                    <a href="{relative_path_to_root}index.html">模块7: 数据可视化</a>
                    <a href="{relative_path_to_root}index.html">模块8: 统计分析</a>
                </div>
            </li>
            <li class="dropdown">
                <a href="#">金融应用</a>
                <div class="dropdown-content">
                    <a href="{relative_path_to_root}index.html">模块9: 金融数据获取</a>
                    <a href="{relative_path_to_root}index.html">模块10: 投资组合分析</a>
                    <a href="{relative_path_to_root}index.html">模块11: 风险管理</a>
                    <a href="{relative_path_to_root}index.html">模块12: 量化交易策略</a>
                </div>
            </li>
            <li class="dropdown">
                <a href="#">高级主题</a>
                <div class="dropdown-content">
                    <a href="{relative_path_to_root}index.html">模块13: 金融衍生品分析</a>
                    <a href="{relative_path_to_root}index.html">模块14: 算法交易与回测系统</a>
                    <a href="{relative_path_to_root}index.html">模块15: 机器学习在金融中的应用</a>
                    <a href="{relative_path_to_root}deep_learning_finance.html">深度学习金融应用</a>
                    <a href="{relative_path_to_root}blockchain_finance.html">区块链金融应用</a>
                    <a href="{relative_path_to_root}index.html">模块16: 综合项目与实践</a>
                </div>
            </li>
        </ul>
    </nav>'''
    return nav_html

def remove_existing_navigation_and_home_buttons(content):
    """删除现有的导航条和返回首页按钮"""
    # 删除返回首页按钮
    content = re.sub(r'<div class="home-button-container">.*?</div>', '', content, flags=re.DOTALL)
    
    # 删除各种形式的导航条
    # 删除完整的nav标签
    content = re.sub(r'<nav>.*?</nav>', '', content, flags=re.DOTALL)
    
    # 删除header中的导航
    content = re.sub(r'<header>.*?</header>', '', content, flags=re.DOTALL)
    
    # 删除独立的导航ul
    content = re.sub(r'<ul class="nav-menu">.*?</ul>', '', content, flags=re.DOTALL)
    
    # 删除面包屑导航
    content = re.sub(r'<div class="breadcrumb">.*?</div>', '', content, flags=re.DOTALL)
    
    return content

def process_html_file(file_path, root_dir):
    """处理单个HTML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 删除现有的导航和返回首页按钮
        content = remove_existing_navigation_and_home_buttons(content)
        
        # 计算相对路径
        relative_path = get_relative_path_to_root(file_path, root_dir)
        
        # 创建新的导航条
        new_nav = create_navigation_html(relative_path)
        
        # 在<body>标签后插入新的导航条
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n{new_nav}\n')
        else:
            # 如果没有<body>标签，在</head>后插入
            content = content.replace('</head>', f'</head>\n<body>\n{new_nav}\n')
        
        # 确保有</body>和</html>标签
        if '</body>' not in content:
            content += '\n</body>'
        if '</html>' not in content:
            content += '\n</html>'
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    root_dir = os.getcwd()
    print(f"开始处理HTML文件，根目录: {root_dir}")
    
    # 查找所有HTML文件
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # 跳过py目录
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    success_count = 0
    error_count = 0
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        success, error = process_html_file(file_path, root_dir)
        
        if success:
            print(f"✓ 已处理: {rel_path}")
            success_count += 1
        else:
            print(f"✗ 处理失败: {rel_path} - {error}")
            error_count += 1
    
    print(f"\n处理完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {error_count} 个文件")
    
    if error_count == 0:
        print("\n所有HTML文件已成功统一导航条!")
    else:
        print(f"\n有 {error_count} 个文件处理失败，请检查错误信息。")

if __name__ == "__main__":
    main()