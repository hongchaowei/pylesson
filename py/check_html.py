import os
import re

def check_html_syntax(file_path):
    """检查HTML文件的语法错误"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        errors = []
        
        # 检查基本HTML结构
        if not content.strip().startswith('<!DOCTYPE html>'):
            errors.append('缺少DOCTYPE声明')
        
        # 检查是否有未闭合的标签
        open_tags = re.findall(r'<([a-zA-Z][^>]*)>', content)
        close_tags = re.findall(r'</([a-zA-Z][^>]*)>', content)
        
        # 简单的标签匹配检查
        tag_stack = []
        for match in re.finditer(r'<(/?)([a-zA-Z][^\s/>]*)[^>]*/?>', content):
            is_closing = match.group(1) == '/'
            tag_name = match.group(2).lower()
            
            # 跳过自闭合标签
            if tag_name in ['br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr']:
                continue
            
            if is_closing:
                if tag_stack and tag_stack[-1] == tag_name:
                    tag_stack.pop()
                else:
                    errors.append(f'未匹配的闭合标签: </{tag_name}>')
            else:
                # 检查是否是自闭合标签
                if not match.group(0).endswith('/>'):
                    tag_stack.append(tag_name)
        
        # 检查是否有未闭合的标签
        if tag_stack:
            errors.append(f'未闭合的标签: {", ".join(tag_stack)}')
        
        # 检查JavaScript语法
        js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        for i, js_block in enumerate(js_blocks):
            if 'function' in js_block and js_block.count('{') != js_block.count('}'):
                errors.append(f'JavaScript块 {i+1} 可能有语法错误：大括号不匹配')
        
        return errors
    
    except Exception as e:
        return [f'读取文件时出错: {str(e)}']

if __name__ == '__main__':
    file_path = 'blockchain_finance.html'
    errors = check_html_syntax(file_path)
    
    if errors:
        print(f'发现 {len(errors)} 个问题:')
        for i, error in enumerate(errors, 1):
            print(f'{i}. {error}')
    else:
        print('HTML文件语法检查通过！')