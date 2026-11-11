import xml.etree.ElementTree as ET
import zlib, base64

with open(r'e:\submission\DataBaseAssignment1\DriveNow.drawio', 'r', encoding='utf-8') as f:
    content = f.read()

tree = ET.fromstring(content)
pages = tree.findall('.//diagram')

def decode_page(p):
    raw = p.text or ''
    # Check if it's compressed (base64+zlib)
    if raw.strip():
        try:
            decoded = base64.b64decode(raw.strip())
            decompressed = zlib.decompress(decoded, -15)
            return decompressed.decode('utf-8')
        except Exception as e:
            # Maybe it's already XML
            return raw
    # Check for child elements
    children = list(p)
    if children:
        return ET.tostring(children[0], encoding='unicode')
    return ''

# Try page 8 (2-Schema-1)
p = pages[7]
print(f'Page: {p.get("name")}')
content_decoded = decode_page(p)
print(f'Decoded len: {len(content_decoded)}')
print(content_decoded[:2000])
