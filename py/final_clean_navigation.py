#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终彻底清理导航条脚本
使用更强力的正则表达式来删除所有导航相关内容
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

def ultra_clean_navigation(content):
    """使用最强力的方法清理所有导航相关内容"""
    # 删除返回首页按钮 - 多种模式
    patterns_to_remove = [
        r'<div[^>]*home-button-container[^>]*>.*?</div>',
        r'<div[^>]*class="home-button-container"[^>]*>.*?</div>',
        r'<a[^>]*home-button[^>]*>.*?</a>',
        r'<div[^>]*>\s*<a[^>]*home-button[^>]*>.*?</a>\s*</div>',
    ]
    
    # 删除导航相关元素
    nav_patterns = [
        r'<nav[^>]*>.*?</nav>',
        r'<header[^>]*>.*?</header>',
        r'<ul[^>]*nav-menu[^>]*>.*?</ul>',
        r'<button[^>]*mobile-menu-toggle[^>]*>.*?</button>',
        r'<li[^>]*dropdown[^>]*>.*?</li>',
        r'<div[^>]*breadcrumb[^>]*>.*?</div>',
        r'<div[^>]*navigation-container[^>]*>.*?</div>',
        r'<div id="navigation-container"[^>]*></div>',
    ]
    
    # 删除导航相关脚本
    script_patterns = [
        r'<script[^>]*>[^<]*loadNavigation[^<]*</script>',
        r'<script>[^<]*navigation-container[^<]*</script>',
        r'<script>\s*//[^<]*动态加载导航条[^<]*</script>',
    ]
    
    all_patterns = patterns_to_remove + nav_patterns + script_patterns
    
    for pattern in all_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # 特殊处理：删除包含"返回首页"文本的任何元素
    content = re.sub(r'<[^>]*>[^<]*返回首页[^<]*</[^>]*>', '', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]*>[^<]*🏠[^<]*</[^>]*>', '', content, flags=re.DOTALL)
    
    # 删除包含menuToggle的任何内容
    content = re.sub(r'<[^>]*menuToggle[^>]*>[^<]*</[^>]*>', '', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]*id="menuToggle"[^>]*>[^<]*</[^>]*>', '', content, flags=re.DOTALL)
    
    # 删除包含nav-menu的任何内容
    content = re.sub(r'<ul[^>]*nav-menu[^>]*>.*?</ul>', '', content, flags=re.DOTALL)
    
    # 清理多余的空行
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    content = re.sub(r'^\s*\n', '', content, flags=re.MULTILINE)
    
    return content

def create_navigation_loader_script(relative_path_to_root):
    """创建动态加载导航条的JavaScript代码"""
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
            if ('{relative_path_to_root}' !== './') {{
                updatedHtml = html.replace(/href="\./g, 'href="{relative_path_to_root}');
                updatedHtml = updatedHtml.replace(/href="index\.html"/g, 'href="{relative_path_to_root}index.html"');
            }}
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

def process_html_file(file_path, root_dir):
    """处理单个HTML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 超强力清理所有导航相关内容
        content = ultra_clean_navigation(content)
        
        # 计算相对路径
        relative_path = get_relative_path_to_root(file_path, root_dir)
        
        # 创建导航加载脚本
        nav_loader = create_navigation_loader_script(relative_path)
        
        # 在<body>标签后插入导航加载器
        if '<body>' in content:
            content = content.replace('<body>', f'<body>{nav_loader}')
        else:
            # 如果没有<body>标签，在</head>后插入
            if '</head>' in content:
                content = content.replace('</head>', f'</head>\n<body>{nav_loader}')
            else:
                # 如果连head都没有，直接在html标签后添加
                content = content.replace('<html', f'<html')
                content = content.replace('>', f'>\n<head></head>\n<body>{nav_loader}', 1)
        
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
    print(f"开始最终彻底清理并实现统一导航条系统，根目录: {root_dir}")
    
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
        print("\n所有HTML文件已成功最终清理并实现统一导航条系统!")
        print("- 所有原有导航条和返回首页按钮已彻底删除")
        print("- 导航条现在通过JavaScript动态加载统一的nav.html文件")
        print("- 所有页面将显示相同的导航条")
    else:
        print(f"\n有 {error_count} 个文件处理失败，请检查错误信息。")

if __name__ == "__main__":
    main()