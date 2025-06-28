import os
import re
from pathlib import Path

def fix_code_alignment():
    """
    修复所有lesson*.html文件中的代码块对齐问题，确保Python代码左对齐
    """
    
    # 项目根目录
    root_dir = Path('.')
    
    # 查找所有lesson*.html文件
    lesson_files = []
    for part_dir in root_dir.glob('part*'):
        if part_dir.is_dir():
            for module_dir in part_dir.glob('module*'):
                if module_dir.is_dir():
                    for lesson_file in module_dir.glob('lesson*.html'):
                        lesson_files.append(lesson_file)
    
    print(f"找到 {len(lesson_files)} 个lesson文件")
    
    # 要添加的CSS样式
    code_alignment_css = """
    <style>
    /* 确保代码块左对齐 */
    .lesson-content pre {
        text-align: left !important;
        font-family: 'Courier New', Courier, monospace;
        background-color: #f5f7fa;
        padding: 15px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 20px 0;
        border-left: 4px solid #4299e1;
    }
    
    .lesson-content code {
        text-align: left !important;
        font-family: 'Courier New', Courier, monospace;
        background-color: #f5f7fa;
        padding: 2px 5px;
        border-radius: 3px;
    }
    
    /* 确保pre标签内的内容左对齐 */
    pre * {
        text-align: left !important;
    }
    
    /* 确保所有代码相关元素都左对齐 */
    pre, code, .hljs {
        text-align: left !important;
    }
    </style>
    """
    
    modified_count = 0
    
    for lesson_file in lesson_files:
        try:
            # 读取文件内容
            with open(lesson_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经包含了代码对齐样式
            if 'text-align: left !important' in content:
                print(f"跳过 {lesson_file}（已包含对齐样式）")
                continue
            
            # 在</head>标签前插入CSS样式
            if '</head>' in content:
                content = content.replace('</head>', code_alignment_css + '\n</head>')
                
                # 写回文件
                with open(lesson_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                modified_count += 1
                print(f"✅ 已修复 {lesson_file}")
            else:
                print(f"⚠️  警告：{lesson_file} 中未找到</head>标签")
                
        except Exception as e:
            print(f"❌ 处理 {lesson_file} 时出错：{e}")
    
    print(f"\n🎉 修复完成！共修改了 {modified_count} 个文件")
    print("\n现在所有lesson*.html文件中的Python代码都将左对齐显示。")

if __name__ == "__main__":
    fix_code_alignment()