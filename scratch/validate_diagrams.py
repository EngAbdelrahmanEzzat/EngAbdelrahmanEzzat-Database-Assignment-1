import xml.etree.ElementTree as ET

tree = ET.parse('e:/submission/DataBaseAssignment1/DriveNow.drawio')
root = tree.getroot()

for d in root.findall('diagram'):
    name = d.get('name')
    model = d.find('mxGraphModel')
    if model is None:
        print(f"ERROR: {name} has NO mxGraphModel!")
        continue
    r = model.find('root')
    if r is None:
        print(f"ERROR: {name} has NO root inside mxGraphModel!")
        continue
    cells = r.findall('mxCell')
    print(f"Checking {name}: {len(cells)} cells")
    for cell in cells:
        cid = cell.get('id')
        val = cell.get('value', '')
        style = cell.get('style', '')
        source = cell.get('source')
        target = cell.get('target')
        # Check if source or target exists if specified
        if source and not any(c.get('id') == source for c in cells):
            print(f"  Missing source {source} in cell {cid} of {name}")
        if target and not any(c.get('id') == target for c in cells):
            print(f"  Missing target {target} in cell {cid} of {name}")
