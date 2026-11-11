import xml.etree.ElementTree as ET
import zlib, base64
import sys
import os

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open(r'e:\submission\DataBaseAssignment1\DriveNow.drawio', 'r', encoding='utf-8') as f:
    content = f.read()

tree = ET.fromstring(content)
pages = tree.findall('.//diagram')

def decode_page(p):
    raw = p.text or ''
    if raw.strip():
        try:
            decoded = base64.b64decode(raw.strip())
            decompressed = zlib.decompress(decoded, -15)
            return decompressed.decode('utf-8')
        except Exception as e:
            return raw
    children = list(p)
    if children:
        return ET.tostring(children[0], encoding='unicode')
    return ''

# Save each Schema page decoded XML to files
os.makedirs(r'e:\submission\DataBaseAssignment1\scratch\decoded', exist_ok=True)
for i, p in enumerate(pages):
    name = p.get('name', f'page_{i+1}')
    decoded = decode_page(p)
    fname = r'e:\submission\DataBaseAssignment1\scratch\decoded' + f'\\{i+1}_{name}.xml'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(decoded)
    print(f'Saved page {i+1} ({name}): {len(decoded)} chars')
