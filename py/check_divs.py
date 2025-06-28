import re

with open('blockchain_finance.html', 'r', encoding='utf-8') as f:
    content = f.read()

open_divs = len(re.findall(r'<div[^>]*>', content))
close_divs = len(re.findall(r'</div>', content))

print(f'开放div标签: {open_divs}')
print(f'闭合div标签: {close_divs}')
print(f'差异: {open_divs - close_divs}')

# 找到最后几个div标签的位置
div_positions = []
for match in re.finditer(r'</?div[^>]*>', content):
    div_positions.append((match.start(), match.group()))

print('\n最后10个div标签:')
for pos, tag in div_positions[-10:]:
    line_num = content[:pos].count('\n') + 1
    print(f'行 {line_num}: {tag}')