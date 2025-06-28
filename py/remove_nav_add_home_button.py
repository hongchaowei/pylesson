#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除冻结导航条，只保留返回首页按钮
1. 移除nav-container div
2. 移除load-nav.js引用
3. 添加简单的返回首页按钮
4. 更新CSS样式
"""

import os
import re
import glob

def remove_nav_add_home_button():
    # 查找所有HTML文件
    html_files = []
    for pattern in ['part*/module*/*.html', '*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. 移除nav-container div
            content = re.sub(r'\s*<div class="nav-container"></div>\s*', '', content)
            
            # 2. 移除load-nav.js引用
            content = re.sub(r'\s*<script src="[^"]*load-nav\.js"[^>]*></script>\s*', '', content)
            
            # 3. 在body标签后添加返回首页按钮
            if '<body>' in content and '返回首页' not in content:
                # 计算相对路径深度
                depth = file_path.count('/') + file_path.count('\\')
                if depth == 0:  # 根目录文件
                    home_path = 'index.html'
                elif depth == 1:  # part目录下的index文件
                    home_path = '../index.html'
                else:  # module目录下的文件
                    home_path = '../../index.html'
                
                home_button = f'''    <div class="home-button-container">
        <a href="{home_path}" class="home-button">🏠 返回首页</a>
    </div>
'''
                
                content = content.replace('<body>', f'<body>\n{home_button}')
            
            # 4. 清理多余的空行
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"修复: {file_path}")
        
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    print(f"\n总共修复了 {fixed_count} 个文件")
    
    # 更新CSS文件，添加返回首页按钮样式
    update_css_for_home_button()

def update_css_for_home_button():
    """更新CSS文件，添加返回首页按钮样式"""
    css_file = 'css/style.css'
    if os.path.exists(css_file):
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # 添加返回首页按钮样式
            home_button_css = '''
/* 返回首页按钮样式 */
.home-button-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
}

.home-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--primary-color);
    color: white;
    padding: 12px 20px;
    border-radius: var(--border-radius);
    text-decoration: none;
    font-weight: 600;
    box-shadow: var(--box-shadow);
    transition: var(--transition);
    font-size: 14px;
}

.home-button:hover {
    background: var(--secondary-color);
    transform: translateY(-2px);
    box-shadow: var(--box-shadow-lg);
    color: white;
}

.home-button:active {
    transform: translateY(0);
}

/* 移动端适配 */
@media (max-width: 768px) {
    .home-button-container {
        top: 10px;
        right: 10px;
    }
    
    .home-button {
        padding: 10px 16px;
        font-size: 13px;
    }
}
'''
            
            # 检查是否已经有返回首页按钮样式
            if '.home-button-container' not in css_content:
                css_content += home_button_css
                
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write(css_content)
                print(f"已更新CSS文件: {css_file}")
            else:
                print("CSS文件已包含返回首页按钮样式")
                
        except Exception as e:
            print(f"更新CSS文件时出错: {e}")
    else:
        print(f"CSS文件不存在: {css_file}")

if __name__ == "__main__":
    remove_nav_add_home_button()