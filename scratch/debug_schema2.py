import xml.etree.ElementTree as ET
import base64, zlib, urllib.parse

def decompress(b64_str):
    raw = base64.b64decode(b64_str)
    inflated = zlib.decompress(raw, -15)
    return urllib.parse.unquote(inflated.decode('utf-8'))

tree = ET.parse(r'e:\submission\DataBaseAssignment1\DriveNow.drawio')
root = tree.getroot()
for d in root.findall('diagram'):
    if d.get('name') == '2-Schema-2':
        xml_str = decompress(d.text.strip())
        print("Total length:", len(xml_str))
        col = 24749
        start = max(0, col - 100)
        end = min(len(xml_str), col + 100)
        print("Around error:")
        print(repr(xml_str[start:end]))
