import xml.etree.ElementTree as ET
import zlib, base64, json, re

with open(r'e:\submission\DataBaseAssignment1\DriveNow.drawio', 'r', encoding='utf-8') as f:
    content = f.read()

tree = ET.fromstring(content)
pages = tree.findall('.//diagram')
print(f'Total pages: {len(pages)}')
for i, p in enumerate(pages):
    pname = p.get('name', '')
    pid = p.get('id', '')
    # Try to decode content
    raw = p.text or ''
    print(f'  Page {i+1}: name={pname}, id={pid}, content_len={len(raw)}')
