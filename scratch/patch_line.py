content = open(r'e:\submission\DataBaseAssignment1\scratch\fix_schemas2.py', 'r', encoding='utf-8').read()
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'WARNING: Derived col' in line:
        lines[i] = '        pv = re.sub(r"<[^>]+>", "", v); print(f"  WARNING: Derived col found: {cid} = {pv[:60]}")'
        print(f'Fixed line {i+1}')
        break
with open(r'e:\submission\DataBaseAssignment1\scratch\fix_schemas2.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Done')
