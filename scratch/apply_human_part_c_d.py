"""
Apply human-style Part C and Part D to DriveNow.drawio
"""
import xml.etree.ElementTree as ET
from build_human_part_c_d import build_human_part_c, build_human_part_d

DRAWIO_PATH = r"e:\submission\DataBaseAssignment1\DriveNow.drawio"

tree = ET.parse(DRAWIO_PATH)
root = tree.getroot()

# Remove existing Part C and Part D
to_remove = []
for d in root.findall(".//diagram"):
    if d.get("name") in ["3-Questions-Assumptions", "4-Business-Rules"]:
        to_remove.append(d)

for d in to_remove:
    root.remove(d)
    print(f"Removed previous: {d.get('name')}")

# Append human-style Part C
diag_c = ET.SubElement(root, "diagram", {
    "id": "p_c",
    "name": "3-Questions-Assumptions"
})
diag_c.append(build_human_part_c())
print("Appended human-style: 3-Questions-Assumptions")

# Append human-style Part D
diag_d = ET.SubElement(root, "diagram", {
    "id": "p_d",
    "name": "4-Business-Rules"
})
diag_d.append(build_human_part_d())
print("Appended human-style: 4-Business-Rules")

xml_output = ET.tostring(root, encoding="unicode")
xml_output = xml_output.replace(' xmlns=""', '')
if not xml_output.startswith("<?xml"):
    xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_output

with open(DRAWIO_PATH, "w", encoding="utf-8") as f:
    f.write(xml_output)

print("Updated DriveNow.drawio successfully!")

# Verify
tree2 = ET.parse(DRAWIO_PATH)
diags = tree2.findall(".//diagram")
print(f"Total diagrams: {len(diags)}")
for idx, d in enumerate(diags, 1):
    cells = d.findall(".//mxCell")
    print(f"  [{idx:2d}/16] {d.get('name'):<28}: {len(cells)} cells")
