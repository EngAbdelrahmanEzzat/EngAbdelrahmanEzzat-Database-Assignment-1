import os
import xml.etree.ElementTree as ET
import base64
import zlib
import urllib.parse

from build_all_pages import (
    build_page_1,
    build_page_2,
    build_page_3,
    build_page_4,
    build_page_5,
    build_page_6,
    build_page_7
)
from build_all_schemas import (
    build_schema_1,
    build_schema_2,
    build_schema_3,
    build_schema_4,
    build_schema_5,
    build_schema_6,
    build_schema_7
)

def decompress(b64_str):
    raw = base64.b64decode(b64_str)
    inflated = zlib.decompress(raw, -15)
    return urllib.parse.unquote(inflated.decode('utf-8'))

def assemble_master():
    print("=== Building Part A: 7 ERD Pages ===")
    erd_1 = build_page_1()
    erd_2 = build_page_2()
    erd_3 = build_page_3()
    erd_4 = build_page_4()
    erd_5 = build_page_5()
    erd_6 = build_page_6()
    erd_7 = build_page_7()
    
    print("=== Building Part B: 7 Relational Schema Pages ===")
    sch_1 = build_schema_1()
    sch_2 = build_schema_2()
    sch_3 = build_schema_3()
    sch_4 = build_schema_4()
    sch_5 = build_schema_5()
    sch_6 = build_schema_6()
    sch_7 = build_schema_7()
    
    master_xml = (
        '<mxfile host="Electron">\n'
        f'{erd_1}\n'
        f'{erd_2}\n'
        f'{erd_3}\n'
        f'{erd_4}\n'
        f'{erd_5}\n'
        f'{erd_6}\n'
        f'{erd_7}\n'
        f'{sch_1}\n'
        f'{sch_2}\n'
        f'{sch_3}\n'
        f'{sch_4}\n'
        f'{sch_5}\n'
        f'{sch_6}\n'
        f'{sch_7}\n'
        '</mxfile>\n'
    )
    
    out_path = r"e:\submission\DataBaseAssignment1\DriveNow.drawio"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(master_xml)
        
    print(f"\nSuccessfully wrote master file to {out_path} ({len(master_xml)} bytes)")
    
    # Verification
    print("\n=== Verifying All 14 Diagrams in DriveNow.drawio ===")
    tree = ET.parse(out_path)
    root = tree.getroot()
    diagrams = root.findall('diagram')
    print(f"Total diagrams found: {len(diagrams)}")
    
    assert len(diagrams) == 14, f"Expected 14 diagrams, got {len(diagrams)}"
    
    for idx, d in enumerate(diagrams, 1):
        name = d.get('name')
        did = d.get('id')
        payload = d.text.strip()
        xml_str = decompress(payload)
        model = ET.fromstring(xml_str)
        cells = model.findall('.//mxCell')
        print(f"  [{idx:2d}/14] {name:<25} (id={did:<4}): {len(cells):3d} cells - OK")

if __name__ == "__main__":
    assemble_master()
