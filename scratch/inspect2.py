import sys, os, zlib, base64
sys.stdout.reconfigure(encoding='utf-8')
import xml.etree.ElementTree as ET

DRAWIO_PATH = r'e:\submission\DataBaseAssignment1\DriveNow.drawio'

with open(DRAWIO_PATH, 'r', encoding='utf-8') as f:
    drawio_content = f.read()

drawio_tree = ET.fromstring(drawio_content)
diagrams = drawio_tree.findall('.//diagram')

for d in diagrams:
    name = d.get('name','')
    text = d.text
    children = list(d)
    print(f'Page: {name!r}  text={repr((text or "")[:20])}  children={len(children)}')
    if children:
        print(f'  First child tag: {children[0].tag}')
