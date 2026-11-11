import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import xml.etree.ElementTree as ET

decoded_dir = r'e:\submission\DataBaseAssignment1\scratch\decoded'

# Analyze Schema pages (8-14)
for page_num in range(8, 15):
    files = [f for f in os.listdir(decoded_dir) if f.startswith(f'{page_num}_')]
    if not files:
        continue
    fname = os.path.join(decoded_dir, files[0])
    with open(fname, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    tree = ET.fromstring(raw)
    cells = tree.findall('.//mxCell')
    
    print(f'\n=== Page {page_num}: {files[0]} ===')
    print(f'  Total cells: {len(cells)}')
    
    labels = []
    for c in cells:
        v = c.get('value', '')
        if v and v.strip() and v != '0':
            labels.append(v)
    
    print(f'  Labeled cells: {len(labels)}')
    for l in labels[:40]:
        print(f'    {repr(l[:120])}')
