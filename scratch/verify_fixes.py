import xml.etree.ElementTree as ET
import base64, zlib, urllib.parse

def decompress(b64_str):
    raw = base64.b64decode(b64_str)
    inflated = zlib.decompress(raw, -15)
    return urllib.parse.unquote(inflated.decode('utf-8'))

tree = ET.parse('e:/submission/DataBaseAssignment1/DriveNow.drawio')
root = tree.getroot()

print("Verifying all 7 pages in DriveNow.drawio:")

for d in root.findall('diagram'):
    pname = d.get('name')
    payload = d.text.strip()
    xml_str = decompress(payload)
    model = ET.fromstring(xml_str)
    cells = model.findall('.//mxCell')
    
    print(f"\n--- {pname} ({len(cells)} cells) ---")
    
    # Check partial keys
    for c in cells:
        val = c.get('value', '')
        style = c.get('style', '')
        cid = c.get('id', '')
        
        # Check partial key styling
        if 'dashed' in val:
            print(f"  [Partial Key] {cid}: {val}")
        # Check candidate key styling
        if '(CK)' in val:
            print(f"  [Candidate Key] {cid}: {val}")
        # Check weak entity style
        if 'shape=ext;double=1' in style:
            print(f"  [Weak Entity] {cid}: {val}")
        # Check identifying relationship style
        if 'shape=rhombus;double=1' in style:
            print(f"  [Identifying Rel] {cid}: {val}")
        # Check multivalued attribute style
        if 'shape=doubleEllipse' in style:
            print(f"  [Multivalued Attr] {cid}: {val}")
        # Check BlacklistID
        if 'BlacklistID' in val:
            print(f"  [Blacklist Key] {cid}: {val}")
