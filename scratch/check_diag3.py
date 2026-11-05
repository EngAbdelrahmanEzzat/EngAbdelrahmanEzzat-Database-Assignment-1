import re
import xml.etree.ElementTree as ET

with open('e:/submission/DataBaseAssignment1/DriveNow.drawio', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<diagram id="p3"[^>]*>(.*?)</diagram>', text, re.DOTALL)
if not m:
    print("Could not find p3")
else:
    d3 = m.group(1).strip()
    print("d3 starts with:", repr(d3[:50]))
    try:
        root = ET.fromstring(d3)
        print("Parsed tag:", root.tag)
        # Check all cells
        cells = root.findall('.//mxCell')
        print("Total cells in p3:", len(cells))
        for c in cells:
            val = c.get('value', '')
            if '&' in val:
                # check unescaped &
                print("Cell with &:", c.get('id'), val)
    except Exception as e:
        print("Parse error in d3:", e)
