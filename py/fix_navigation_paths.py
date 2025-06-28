#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复导航条路径问题
确保不同深度的HTML文件都能正确加载导航条和链接
"""

import os
import re
from pathlib import Path

def get_relative_path_to_root(file_path, root_dir):
    """计算从文件到根目录的相对路径"""
    file_path = Path(file_path)
    root_dir = Path(root_dir)
    
    try:
        rel_path = os.path.relpath(root_dir, file_path.parent)
        if rel_path == '.':
            return './'
        else:
            return rel_path.replace('\\', '/') + '/'
    except ValueError:
        return './'

def create_correct_navigation_script(relative_path_to_root):
    """创建正确的导航加载脚本"""
    script = f'''
<div id="navigation-container"></div>
<script>
// 动态加载导航条
function loadNavigation() {{
    fetch('{relative_path_to_root}nav.html')
        .then(response => response.text())
        .then(html => {{
            // 更新导航中的链接路径
            let updatedHtml = html;
            // 替换所有相对路径引用
            updatedHtml = updatedHtml.replace(/href="\.\/([^"]*)"/g, 'href="{relative_path_to_root}$1"');
            updatedHtml = updatedHtml.replace(/href="index\.html"/g, 'href="{relative_path_to_root}index.html"');
            
            document.getElementById('navigation-container').innerHTML = updatedHtml;
            
            // 添加移动端菜单切换功能
            const menuToggle = document.getElementById('menuToggle');
            const navMenu = document.querySelector('.nav-menu');
            if (menuToggle && navMenu) {{
                menuToggle.addEventListener('click', function() {{
                    navMenu.classList.toggle('active');
                }});
            }}
        }})
        .catch(error => console.error('导航加载失败:', error));
}}

// 页面加载完成后加载导航
document.addEventListener('DOMContentLoaded', loadNavigation);
</script>
'''
    return script

def fix_navigation_in_file(file_path, root_dir):
    """修复单个文件的导航脚本"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 计算正确的相对路径
        relative_path = get_relative_path_to_root(file_path, root_dir)
        
        # 删除现有的导航容器和脚本
        # 匹配从<div id="navigation-container"></div>到</script>的整个块
        pattern = r'<div id="navigation-container"></div>\s*<script>[\s\S]*?</script>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 创建新的导航脚本
        new_nav_script = create_correct_navigation_script(relative_path)
        
        # 在<body>标签后插入新的导航脚本
        if '<body>' in content:
            content = content.replace('<body>', f'<body>{new_nav_script}')
        else:
            # 如果没有<body>标签，在</head>后插入
            if '</head>' in content:
                content = content.replace('</head>', f'</head>\n<body>{new_nav_script}')
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, relative_path
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    root_dir = os.getcwd()
    print(f"开始修复导航条路径问题，根目录: {root_dir}")
    
    # 查找所有HTML文件（除了nav.html）
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # 跳过py目录
        if 'py' in dirs:
            dirs.remove('py')
        
        for file in files:
            if file.endswith('.html') and file != 'nav.html':
                html_files.append(os.path.join(root, file))
    
    print(f"找到 {len(html_files)} 个HTML文件需要处理")
    
    success_count = 0
    error_count = 0
    path_info = {}
    
    for file_path in html_files:
        rel_file_path = os.path.relpath(file_path, root_dir)
        success, result = fix_navigation_in_file(file_path, root_dir)
        
        if success:
            relative_path = result
            print(f"✓ 已修复: {rel_file_path} (路径: {relative_path})")
            success_count += 1
            
            # 记录路径信息用于验证
            if relative_path not in path_info:
                path_info[relative_path] = []
            path_info[relative_path].append(rel_file_path)
        else:
            print(f"✗ 修复失败: {rel_file_path} - {result}")
            error_count += 1
    
    print(f"\n修复完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {error_count} 个文件")
    
    # 显示路径分布
    print("\n路径分布统计:")
    for path, files in sorted(path_info.items()):
        print(f"  {path}: {len(files)} 个文件")
        if len(files) <= 5:  # 只显示少量文件的详细信息
            for file in files[:3]:
                print(f"    - {file}")
            if len(files) > 3:
                print(f"    - ... 还有 {len(files) - 3} 个文件")
    
    if error_count == 0:
        print("\n所有HTML文件的导航路径已成功修复!")
        print("- 每个文件现在都使用正确的相对路径加载nav.html")
        print("- 导航链接会根据文件位置自动调整")
        print("- 所有深度的文件都能正确显示导航条")
    else:
        print(f"\n有 {error_count} 个文件修复失败，请检查错误信息。")

if __name__ == "__main__":
    main()