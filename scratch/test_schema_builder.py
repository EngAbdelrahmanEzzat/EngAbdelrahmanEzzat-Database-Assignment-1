import urllib.parse
import zlib
import base64

def drawio_compress(xml_str):
    quoted = urllib.parse.quote(xml_str, safe='~()*!\'')
    co = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    deflated = co.compress(quoted.encode('utf-8')) + co.flush()
    return base64.b64encode(deflated).decode('ascii')

class SchemaPageBuilder:
    def __init__(self, page_id, page_name, title, width=2800, height=2200):
        self.page_id = page_id
        self.page_name = page_name
        self.width = width
        self.height = height
        self.cells = []
        self.edge_count = 0
        self.box_count = 0
        
        self.cells.append('<mxCell id="0"/>')
        self.cells.append('<mxCell id="1" parent="0"/>')
        
        # Header banner with student name and group
        header_id = f"{page_id}_header"
        # Escaping title
        safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.cells.append(
            f'<mxCell id="{header_id}" value="{safe_title}" '
            f'style="text;html=1;fontSize=18;fontStyle=1;align=center;verticalAlign=middle;'
            f'fillColor=#f8f9fa;strokeColor=#b0bec5;strokeWidth=2;rounded=1;shadow=0;" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="100" y="25" width="{width - 200}" height="55" as="geometry"/>'
            f'</mxCell>'
        )

    def add_table(self, table_id, table_name, x, y, columns, rules=None, is_sub=False):
        # 1. Table Title above the table
        title_id = f"{table_id}_title"
        title_color = "#1565c0" if not is_sub else "#2e7d32"
        self.cells.append(
            f'<mxCell id="{title_id}" value="&lt;b&gt;{table_name}&lt;/b&gt;" '
            f'style="text;html=1;fontSize=15;fontStyle=1;align=left;verticalAlign=bottom;fontColor={title_color};" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y - 30}" width="300" height="25" as="geometry"/>'
            f'</mxCell>'
        )
        
        # 2. Columns row (boxes side by side)
        cur_x = x
        col_boxes = {}
        for col in columns:
            self.box_count += 1
            col_id = f"{table_id}_col_{col['name']}"
            w = col.get("width", 115)
            h = 52
            
            # Label: Name (underlined if PK) + tags below
            name_display = f"&lt;u&gt;{col['name']}&lt;/u&gt;" if col.get("is_pk") else col['name']
            raw_tags = col.get("tags", "NN")
            safe_tags = raw_tags.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            
            box_label = (
                f"&lt;div style=&quot;font-size:12px; font-weight:{'bold' if col.get('is_pk') else 'normal'};&quot;&gt;{name_display}&lt;/div&gt;"
                f"&lt;div style=&quot;font-size:10px; color:#555; margin-top:2px;&quot;&gt;{safe_tags}&lt;/div&gt;"
            )
            
            fill = "#e3f2fd" if col.get("is_pk") else "#ffffff"
            stroke = "#1976d2" if col.get("is_pk") else "#b0bec5"
            sw = "2" if col.get("is_pk") else "1"
            
            box_style = (
                f"shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
                f"fillColor={fill};strokeColor={stroke};strokeWidth={sw};rounded=0;"
            )
            
            self.cells.append(
                f'<mxCell id="{col_id}" value="{box_label}" style="{box_style}" vertex="1" parent="1">'
                f'<mxGeometry x="{cur_x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
                f'</mxCell>'
            )
            col_boxes[col['name']] = col_id
            cur_x += w
            
        # 3. Multi-column rules below table
        if rules:
            rules_id = f"{table_id}_rules"
            joined_rules = " | ".join(rules)
            safe_rules = joined_rules.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            self.cells.append(
                f'<mxCell id="{rules_id}" value="&lt;i style=&quot;color:#d32f2f; font-size:11px;&quot;&gt;{safe_rules}&lt;/i&gt;" '
                f'style="text;html=1;fontSize=11;align=left;verticalAlign=top;" vertex="1" parent="1">'
                f'<mxGeometry x="{x}" y="{y + 56}" width="{max(400, cur_x - x)}" height="20" as="geometry"/>'
                f'</mxCell>'
            )
            
        return col_boxes

    def add_external_ref(self, ref_id, ref_name, x, y, w=150, h=35):
        style = (
            "shape=rectangle;dashed=1;whiteSpace=wrap;html=1;fontSize=11;fontStyle=2;"
            "fillColor=#f8f9fa;strokeColor=#78909c;strokeWidth=1.5;align=center;verticalAlign=middle;"
        )
        safe_name = ref_name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.cells.append(
            f'<mxCell id="{ref_id}" value="{safe_name}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
            f'</mxCell>'
        )
        return ref_id

    def add_fk_arrow(self, source_col_id, target_col_id, edge_id=None, label="", color="#0277bd", exit_pos="bottom", entry_pos="top"):
        self.edge_count += 1
        if not edge_id:
            edge_id = f"{self.page_id}_fk_edge_{self.edge_count}"
            
        exit_coords = {"bottom": "exitX=0.5;exitY=1;", "top": "exitX=0.5;exitY=0;", "right": "exitX=1;exitY=0.5;", "left": "exitX=0;exitY=0.5;"}
        entry_coords = {"top": "entryX=0.5;entryY=0;", "bottom": "entryX=0.5;entryY=1;", "left": "entryX=0;entryY=0.5;", "right": "entryX=1;entryY=0.5;"}
        
        style = (
            f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
            f"endArrow=block;endFill=1;strokeColor={color};strokeWidth=1.8;fontSize=10;fontStyle=1;"
            f"{exit_coords.get(exit_pos, '')}{entry_coords.get(entry_pos, '')}"
        )
        
        self.cells.append(
            f'<mxCell id="{edge_id}" value="{label}" style="{style}" edge="1" source="{source_col_id}" target="{target_col_id}" parent="1">'
            f'<mxGeometry relative="1" as="geometry"/>'
            f'</mxCell>'
        )
        return edge_id

    def build_diagram_compressed(self):
        inner = "".join(self.cells)
        model_xml = (
            f'<mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.width}" pageHeight="{self.height}" math="0" shadow="0">'
            f'<root>{inner}</root>'
            f'</mxGraphModel>'
        )
        compressed_payload = drawio_compress(model_xml)
        return f'  <diagram id="{self.page_id}" name="{self.page_name}">{compressed_payload}</diagram>'
