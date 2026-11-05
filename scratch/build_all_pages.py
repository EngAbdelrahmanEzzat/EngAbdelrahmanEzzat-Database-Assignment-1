import urllib.parse
import zlib
import base64

def drawio_compress(xml_str):
    quoted = urllib.parse.quote(xml_str, safe='~()*!\'')
    co = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    deflated = co.compress(quoted.encode('utf-8')) + co.flush()
    return base64.b64encode(deflated).decode('ascii')

def drawio_decompress(b64_str):
    raw = base64.b64decode(b64_str)
    inflated = zlib.decompress(raw, -15)
    return urllib.parse.unquote(inflated.decode('utf-8'))

class PageBuilder:
    def __init__(self, page_id, page_name, title, width=2800, height=2000):
        self.page_id = page_id
        self.page_name = page_name
        self.width = width
        self.height = height
        self.cells = []
        self.edge_count = 0
        
        self.cells.append('<mxCell id="0"/>')
        self.cells.append('<mxCell id="1" parent="0"/>')
        
        # Header banner
        title_id = f"{page_id}_header"
        self.cells.append(
            f'<mxCell id="{title_id}" value="{title}" '
            f'style="text;html=1;fontSize=18;fontStyle=1;align=center;verticalAlign=middle;'
            f'fillColor=#f8f9fa;strokeColor=#b0bec5;strokeWidth=2;rounded=1;shadow=0;" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="100" y="25" width="{width - 200}" height="55" as="geometry"/>'
            f'</mxCell>'
        )

    def add_entity(self, eid, label, x, y, w=150, h=60, is_weak=False, is_dashed=False):
        if is_dashed:
            style = "shape=rectangle;whiteSpace=wrap;html=1;fontSize=14;fontStyle=3;fillColor=#f5f5f5;strokeColor=#666666;dashed=1;"
        elif is_weak:
            # Native double rectangle for weak entity
            style = "shape=ext;double=1;whiteSpace=wrap;html=1;fontSize=14;fontStyle=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        else:
            style = "shape=rectangle;whiteSpace=wrap;html=1;fontSize=14;fontStyle=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        
        self.cells.append(
            f'<mxCell id="{eid}" value="{label}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
            f'</mxCell>'
        )
        return eid

    def add_attribute(self, aid, label, x, y, parent_id, w=125, h=40, is_key=False, is_partial=False, is_derived=False, is_multivalued=False, is_candidate_key=False):
        if is_key:
            display = f"&lt;u&gt;{label}&lt;/u&gt;"
        elif is_partial:
            display = f"&lt;span style=&quot;border-bottom: 2px dashed #000; padding-bottom: 2px; font-weight: bold;&quot;&gt;{label}&lt;/span&gt;"
        elif is_candidate_key:
            display = f"{label}&lt;br&gt;&lt;span style=&quot;font-size: 9px; color: #495057; font-weight: bold;&quot;&gt;(CK)&lt;/span&gt;"
        else:
            display = label
            
        if is_multivalued:
            # Native double ellipse for multivalued attribute
            style = "shape=doubleEllipse;whiteSpace=wrap;html=1;fontSize=11;fillColor=#fff2cc;strokeColor=#d6b656;"
        elif is_derived:
            style = "ellipse;whiteSpace=wrap;html=1;fontSize=11;fillColor=#fff2cc;strokeColor=#d6b656;dashed=1;"
        else:
            style = "ellipse;whiteSpace=wrap;html=1;fontSize=11;fillColor=#fff2cc;strokeColor=#d6b656;"
            
        self.cells.append(
            f'<mxCell id="{aid}" value="{display}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
            f'</mxCell>'
        )
        
        edge_id = f"e_{aid}"
        self.cells.append(
            f'<mxCell id="{edge_id}" style="endArrow=none;html=1;strokeWidth=1;strokeColor=#6c8ebf;" edge="1" source="{parent_id}" target="{aid}" parent="1">'
            f'<mxGeometry relative="1" as="geometry"/>'
            f'</mxCell>'
        )
        return aid

    def add_relationship(self, rid, label, x, y, w=135, h=65, is_identifying=False):
        if is_identifying:
            # Native double diamond for identifying relationship
            style = "shape=rhombus;double=1;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fontSize=12;fontStyle=1;fillColor=#d5e8d4;strokeColor=#82b366;"
        else:
            style = "shape=rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fontSize=12;fontStyle=1;fillColor=#d5e8d4;strokeColor=#82b366;"
            
        self.cells.append(
            f'<mxCell id="{rid}" value="{label}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
            f'</mxCell>'
        )
        return rid

    def add_isa(self, triangle_id, x, y, label="ISA\n(d)", size=65):
        style = "shape=triangle;direction=south;whiteSpace=wrap;html=1;fontSize=12;fontStyle=1;fillColor=#f8cecc;strokeColor=#b85450;"
        self.cells.append(
            f'<mxCell id="{triangle_id}" value="{label}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{size}" height="{size}" as="geometry"/>'
            f'</mxCell>'
        )
        return triangle_id

    def connect(self, source_id, target_id, card="", is_total=False, role="", edge_id=None):
        self.edge_count += 1
        if not edge_id:
            edge_id = f"{self.page_id}_edge_{self.edge_count}"
            
        sw = "3" if is_total else "1"
        style = f"endArrow=none;html=1;strokeWidth={sw};fontSize=12;fontStyle=1;strokeColor=#2c3e50;"
            
        label_parts = []
        if card:
            label_parts.append(card)
        if role:
            label_parts.append(f"({role})")
        val = " ".join(label_parts)
        
        self.cells.append(
            f'<mxCell id="{edge_id}" value="{val}" style="{style}" edge="1" source="{source_id}" target="{target_id}" parent="1">'
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

# ==============================================================================
# PAGE 1: 1-ERD-1-Staff
# ==============================================================================
def build_page_1():
    p = PageBuilder("p1", "1-ERD-1-Staff", "Page 1: Staff — DriveNow ERD (Chen Notation) — Name: عبدالرحمن عزت فتوح — Group 2", width=2600, height=1800)
    
    # BRANCH
    p.add_entity("p1_branch", "BRANCH", 320, 360, 150, 60)
    p.add_attribute("p1_b_code", "BranchCode", 150, 240, "p1_branch", is_key=True)
    p.add_attribute("p1_b_name", "Name", 310, 220, "p1_branch")
    p.add_attribute("p1_b_addr", "Address", 470, 240, "p1_branch")
    p.add_attribute("p1_b_street", "Street", 560, 160, "p1_b_addr", w=90, h=35)
    p.add_attribute("p1_b_city", "City", 660, 190, "p1_b_addr", w=90, h=35)
    p.add_attribute("p1_b_gov", "Governorate", 650, 250, "p1_b_addr", w=95, h=35)
    # Multivalued Phone
    p.add_attribute("p1_b_phone", "Phone", 130, 340, "p1_branch", is_multivalued=True)
    p.add_attribute("p1_b_opentime", "OpeningTime", 120, 420, "p1_branch")
    p.add_attribute("p1_b_closetime", "ClosingTime", 170, 490, "p1_branch")
    p.add_attribute("p1_b_is24h", "Is24Hours", 320, 500, "p1_branch")
    
    # EMPLOYEE
    p.add_entity("p1_employee", "EMPLOYEE", 1100, 520, 160, 65)
    p.add_attribute("p1_e_id", "EmployeeID", 900, 380, "p1_employee", is_key=True)
    # Candidate Keys: NationalID and Email marked as (CK)
    p.add_attribute("p1_e_natid", "NationalID", 1060, 360, "p1_employee", is_candidate_key=True)
    p.add_attribute("p1_e_name", "Name", 1240, 370, "p1_employee")
    p.add_attribute("p1_e_first", "First", 1380, 290, "p1_e_name", w=80, h=35)
    p.add_attribute("p1_e_mid", "Middle", 1460, 340, "p1_e_name", w=80, h=35)
    p.add_attribute("p1_e_last", "Last", 1460, 400, "p1_e_name", w=80, h=35)
    p.add_attribute("p1_e_dob", "DateOfBirth", 1370, 470, "p1_employee")
    p.add_attribute("p1_e_hire", "HireDate", 1380, 550, "p1_employee")
    p.add_attribute("p1_e_salary", "Salary", 1340, 630, "p1_employee")
    p.add_attribute("p1_e_email", "Email", 1240, 680, "p1_employee", is_candidate_key=True)
    p.add_attribute("p1_e_age", "Age", 1090, 690, "p1_employee", is_derived=True)
    
    # MANAGES
    p.add_relationship("p1_rel_manages", "MANAGES", 700, 340)
    p.add_attribute("p1_attr_mgr_start", "ManagerStartDate", 700, 240, "p1_rel_manages")
    p.connect("p1_branch", "p1_rel_manages", card="1", is_total=True)
    p.connect("p1_employee", "p1_rel_manages", card="1", is_total=False)
    
    # WORKS_AT
    p.add_relationship("p1_rel_works_at", "WORKS_AT", 700, 470)
    p.connect("p1_branch", "p1_rel_works_at", card="1", is_total=False)
    p.connect("p1_employee", "p1_rel_works_at", card="N", is_total=True)
    
    # SUPERVISES (Recursive)
    p.add_relationship("p1_rel_supervises", "SUPERVISES", 900, 520)
    p.connect("p1_employee", "p1_rel_supervises", card="1", role="Supervisor", is_total=False)
    p.connect("p1_rel_supervises", "p1_employee", card="N", role="Subordinate", is_total=False)
    
    # ISA Specialization
    p.add_isa("p1_isa", 1145, 820, label="ISA\n(d)")
    p.connect("p1_employee", "p1_isa", is_total=False)
    
    # RENTAL_AGENT
    p.add_entity("p1_rental_agent", "RENTAL_AGENT", 900, 1020, 150, 60)
    p.add_attribute("p1_ra_comm", "CommissionRate", 720, 1030, "p1_rental_agent")
    p.connect("p1_isa", "p1_rental_agent", is_total=False)
    
    # MECHANIC
    p.add_entity("p1_mechanic", "MECHANIC", 1300, 1020, 150, 60)
    p.add_attribute("p1_m_spec", "Specialization", 1490, 990, "p1_mechanic")
    p.add_attribute("p1_m_cert", "CertificationLevel", 1490, 1060, "p1_mechanic")
    p.connect("p1_isa", "p1_mechanic", is_total=False)
    
    # COURSE
    p.add_entity("p1_course", "COURSE", 1950, 520, 150, 60)
    p.add_attribute("p1_c_code", "CourseCode", 1950, 390, "p1_course", is_key=True)
    p.add_attribute("p1_c_title", "Title", 2130, 420, "p1_course")
    p.add_attribute("p1_c_hours", "Hours", 2150, 500, "p1_course")
    p.add_attribute("p1_c_mand", "IsMandatory", 2140, 580, "p1_course")
    
    # ENROLLMENT (Weak Entity)
    p.add_entity("p1_enrollment", "ENROLLMENT", 1700, 850, 150, 60, is_weak=True)
    # Partial key: AttemptNo
    p.add_attribute("p1_enr_attempt", "AttemptNo", 1520, 890, "p1_enrollment", is_partial=True)
    p.add_attribute("p1_enr_date", "EnrollDate", 1570, 970, "p1_enrollment")
    p.add_attribute("p1_enr_comp", "CompletionDate", 1720, 990, "p1_enrollment")
    p.add_attribute("p1_enr_score", "Score", 1880, 970, "p1_enrollment")
    p.add_attribute("p1_enr_res", "Result", 1920, 890, "p1_enrollment")
    
    # Identifying relationships: ENROLLS & FOR_COURSE
    p.add_relationship("p1_rel_enrolls", "ENROLLS", 1440, 720, is_identifying=True)
    p.connect("p1_employee", "p1_rel_enrolls", card="1", is_total=False)
    p.connect("p1_enrollment", "p1_rel_enrolls", card="N", is_total=True)
    
    p.add_relationship("p1_rel_for_course", "FOR_COURSE", 1880, 700, is_identifying=True)
    p.connect("p1_course", "p1_rel_for_course", card="1", is_total=False)
    p.connect("p1_enrollment", "p1_rel_for_course", card="N", is_total=True)
    
    return p.build_diagram_compressed()

# ==============================================================================
# PAGE 2: 1-ERD-2-Fleet
# ==============================================================================
def build_page_2():
    p = PageBuilder("p2", "1-ERD-2-Fleet", "Page 2: Fleet — DriveNow ERD (Chen Notation) — Name: عبدالرحمن عزت فتوح — Group 2", width=2800, height=2000)
    
    # CATEGORY
    p.add_entity("p2_category", "CATEGORY", 300, 250, 150, 60)
    p.add_attribute("p2_cat_name_key", "CategoryName", 130, 180, "p2_category", is_key=True)
    p.add_attribute("p2_cat_desc", "Name", 300, 150, "p2_category")
    
    # CATEGORY_RATE (Weak Entity)
    p.add_entity("p2_cat_rate", "CATEGORY_RATE", 300, 520, 160, 60, is_weak=True)
    # Partial key: ValidFrom
    p.add_attribute("p2_crate_from", "ValidFrom", 120, 480, "p2_cat_rate", is_partial=True)
    p.add_attribute("p2_crate_to", "ValidTo", 120, 560, "p2_cat_rate")
    p.add_attribute("p2_crate_rate", "DailyRate", 280, 640, "p2_cat_rate")
    
    # Identifying relationship: HAS_RATE
    p.add_relationship("p2_rel_has_rate", "HAS_RATE", 310, 380, is_identifying=True)
    p.connect("p2_category", "p2_rel_has_rate", card="1", is_total=False)
    p.connect("p2_cat_rate", "p2_rel_has_rate", card="N", is_total=True)
    
    # CAR_MODEL
    p.add_entity("p2_car_model", "CAR_MODEL", 820, 250, 150, 60)
    p.add_attribute("p2_cm_id", "ID", 670, 140, "p2_car_model", is_key=True)
    p.add_attribute("p2_cm_mfg", "Manufacturer", 820, 120, "p2_car_model")
    p.add_attribute("p2_cm_model", "ModelName", 970, 140, "p2_car_model")
    p.add_attribute("p2_cm_year", "Year", 1020, 220, "p2_car_model")
    p.add_attribute("p2_cm_seats", "Seats", 1020, 290, "p2_car_model")
    p.add_attribute("p2_cm_trans", "TransmissionType", 980, 360, "p2_car_model")
    p.add_attribute("p2_cm_fuel", "FuelType", 840, 370, "p2_car_model")
    
    p.add_relationship("p2_rel_belongs_to", "BELONGS_TO", 560, 250)
    p.connect("p2_category", "p2_rel_belongs_to", card="1", is_total=False)
    p.connect("p2_car_model", "p2_rel_belongs_to", card="N", is_total=True)
    
    # VEHICLE
    p.add_entity("p2_vehicle", "VEHICLE", 1250, 650, 160, 65)
    p.add_attribute("p2_v_vin", "VIN", 1060, 540, "p2_vehicle", is_key=True)
    # Candidate Key: PlateNumber
    p.add_attribute("p2_v_plate", "PlateNumber", 1200, 510, "p2_vehicle", is_candidate_key=True)
    p.add_attribute("p2_v_color", "Color", 1350, 520, "p2_vehicle")
    p.add_attribute("p2_v_odo", "OdometerReading", 1470, 570, "p2_vehicle")
    p.add_attribute("p2_v_pdate", "PurchaseDate", 1480, 650, "p2_vehicle")
    p.add_attribute("p2_v_pprice", "PurchasePrice", 1460, 730, "p2_vehicle")
    p.add_attribute("p2_v_stat", "Status", 1380, 790, "p2_vehicle")
    
    # GPS_DEVICE
    p.add_entity("p2_gps", "GPS_DEVICE", 1850, 400, 150, 60)
    p.add_attribute("p2_gps_sn", "SerialNo", 1750, 290, "p2_gps", is_key=True)
    p.add_attribute("p2_gps_mfg", "Manufacturer", 1920, 280, "p2_gps")
    p.add_attribute("p2_gps_sim", "SimCardNumber", 2040, 340, "p2_gps")
    
    p.add_relationship("p2_rel_installed", "INSTALLED_IN", 1580, 510)
    p.add_attribute("p2_attr_inst_date", "InstallDate", 1580, 420, "p2_rel_installed")
    p.connect("p2_gps", "p2_rel_installed", card="1", is_total=False)
    p.connect("p2_vehicle", "p2_rel_installed", card="1", is_total=False)
    
    # VEHICLE_STATUS_LOG (Weak Entity)
    p.add_entity("p2_vlog", "VEHICLE_STATUS_LOG", 1950, 750, 190, 60, is_weak=True)
    # Partial key: LogNo
    p.add_attribute("p2_vlog_no", "LogNo", 1880, 870, "p2_vlog", is_partial=True)
    p.add_attribute("p2_vlog_old", "OldStatus", 2010, 890, "p2_vlog")
    p.add_attribute("p2_vlog_new", "NewStatus", 2140, 870, "p2_vlog")
    p.add_attribute("p2_vlog_at", "ChangedAt", 2190, 780, "p2_vlog")
    
    # Identifying relationship: HAS_STATUS_LOG
    p.add_relationship("p2_rel_has_log", "HAS_STATUS_LOG", 1630, 700, is_identifying=True)
    p.connect("p2_vehicle", "p2_rel_has_log", card="1", is_total=False)
    p.connect("p2_vlog", "p2_rel_has_log", card="N", is_total=True)
    
    p.add_entity("p2_employee_dashed", "EMPLOYEE", 2250, 620, 140, 55, is_dashed=True)
    p.add_relationship("p2_rel_changed_by", "CHANGED_BY", 2130, 680)
    p.connect("p2_employee_dashed", "p2_rel_changed_by", card="1", is_total=False)
    p.connect("p2_vlog", "p2_rel_changed_by", card="N", is_total=True)
    
    p.add_entity("p2_branch_dashed", "BRANCH", 750, 850, 140, 55, is_dashed=True)
    p.add_relationship("p2_rel_home_branch", "HOME_BRANCH", 1000, 750)
    p.connect("p2_branch_dashed", "p2_rel_home_branch", card="1", is_total=False)
    p.connect("p2_vehicle", "p2_rel_home_branch", card="N", is_total=True)
    
    # VEHICLE_TRANSFER (Weak Entity)
    p.add_entity("p2_transfer", "VEHICLE_TRANSFER", 1150, 1250, 170, 60, is_weak=True)
    # Partial key: TransferNo
    p.add_attribute("p2_tr_no", "TransferNo", 980, 1370, "p2_transfer", is_partial=True)
    p.add_attribute("p2_tr_dt", "TransferDateTime", 1150, 1390, "p2_transfer")
    p.add_attribute("p2_tr_odo", "OdometerReading", 1330, 1370, "p2_transfer")
    
    # Identifying relationship: HAS_TRANSFER
    p.add_relationship("p2_rel_has_transfer", "HAS_TRANSFER", 1210, 980, is_identifying=True)
    p.connect("p2_vehicle", "p2_rel_has_transfer", card="1", is_total=False)
    p.connect("p2_transfer", "p2_rel_has_transfer", card="N", is_total=True)
    
    p.add_relationship("p2_rel_from_branch", "FROM_BRANCH", 820, 1080)
    p.connect("p2_branch_dashed", "p2_rel_from_branch", card="1", is_total=False)
    p.connect("p2_transfer", "p2_rel_from_branch", card="N", is_total=True)
    
    p.add_relationship("p2_rel_to_branch", "TO_BRANCH", 980, 1150)
    p.connect("p2_branch_dashed", "p2_rel_to_branch", card="1", is_total=False)
    p.connect("p2_transfer", "p2_rel_to_branch", card="N", is_total=True)
    
    p.add_relationship("p2_rel_driven_by", "DRIVEN_BY", 1600, 1150)
    p.connect("p2_employee_dashed", "p2_rel_driven_by", card="1", is_total=False)
    p.connect("p2_transfer", "p2_rel_driven_by", card="N", is_total=True)
    
    return p.build_diagram_compressed()

# ==============================================================================
# PAGE 3: 1-ERD-3-Customers
# ==============================================================================
def build_page_3():
    p = PageBuilder("p3", "1-ERD-3-Customers", "Page 3: Customers — DriveNow ERD (Chen Notation) — Name: عبدالرحمن عزت فتوح — Group 2", width=2800, height=2000)
    
    # CUSTOMER
    p.add_entity("p3_customer", "CUSTOMER", 950, 220, 160, 65)
    p.add_attribute("p3_c_no", "CustomerNo", 780, 130, "p3_customer", is_key=True)
    # Candidate key: Email
    p.add_attribute("p3_c_email", "Email", 950, 110, "p3_customer", is_candidate_key=True)
    p.add_attribute("p3_c_addr", "Address", 1110, 120, "p3_customer")
    p.add_attribute("p3_c_regdate", "RegistrationDate", 1190, 190, "p3_customer", w=130)
    # Multivalued Phone
    p.add_attribute("p3_c_phone", "Phone", 780, 220, "p3_customer", is_multivalued=True)
    
    # ISA Specialization (Total + Disjoint)
    p.add_isa("p3_isa", 995, 430, label="ISA\n(d)")
    p.connect("p3_customer", "p3_isa", is_total=True)
    
    # INDIVIDUAL
    p.add_entity("p3_individual", "INDIVIDUAL", 550, 680, 160, 65)
    p.connect("p3_isa", "p3_individual", is_total=False)
    p.add_attribute("p3_ind_name", "FullName", 380, 600, "p3_individual")
    p.add_attribute("p3_ind_dob", "DateOfBirth", 360, 670, "p3_individual")
    # Candidate Key: NationalID
    p.add_attribute("p3_ind_natid", "NationalID", 370, 740, "p3_individual", is_candidate_key=True)
    p.add_attribute("p3_ind_pass", "PassportNo", 410, 810, "p3_individual")
    p.add_attribute("p3_ind_lic", "License", 560, 830, "p3_individual")
    p.add_attribute("p3_lic_no", "LicenseNo", 450, 930, "p3_ind_lic", w=95, h=35)
    p.add_attribute("p3_lic_cntry", "IssuingCountry", 570, 950, "p3_ind_lic", w=110, h=35)
    p.add_attribute("p3_lic_exp", "ExpiryDate", 700, 930, "p3_ind_lic", w=95, h=35)
    
    # CORPORATE
    p.add_entity("p3_corporate", "CORPORATE", 1400, 680, 160, 65)
    p.connect("p3_isa", "p3_corporate", is_total=False)
    p.add_attribute("p3_corp_name", "CompanyName", 1230, 600, "p3_corporate")
    p.add_attribute("p3_corp_tax", "TaxRegistrationNumber", 1220, 750, "p3_corporate", w=145)
    p.add_attribute("p3_corp_contact", "ContactPerson", 1360, 820, "p3_corporate")
    p.add_attribute("p3_corp_limit", "CreditLimit", 1520, 820, "p3_corporate")
    
    # AUTHORIZED_DRIVER (Weak Entity)
    p.add_entity("p3_auth_driver", "AUTHORIZED_DRIVER", 1950, 680, 180, 65, is_weak=True)
    # Partial key: DriverNo
    p.add_attribute("p3_ad_no", "DriverNo", 1950, 560, "p3_auth_driver", is_partial=True)
    p.add_attribute("p3_ad_name", "Name", 2120, 610, "p3_auth_driver")
    p.add_attribute("p3_ad_licno", "LicenseNo", 2180, 680, "p3_auth_driver")
    p.add_attribute("p3_ad_licexp", "LicenseExpiry", 2160, 750, "p3_auth_driver")
    p.add_attribute("p3_ad_phone", "Phone", 2100, 820, "p3_auth_driver")
    
    # Identifying relationship: HAS_DRIVER
    p.add_relationship("p3_rel_has_driver", "HAS_DRIVER", 1680, 680, is_identifying=True)
    p.connect("p3_corporate", "p3_rel_has_driver", card="1", is_total=False)
    p.connect("p3_auth_driver", "p3_rel_has_driver", card="N", is_total=True)
    
    # BLACKLIST (Strong Entity with Key BlacklistID)
    p.add_entity("p3_blacklist", "BLACKLIST", 300, 220, 150, 60)
    p.add_attribute("p3_bl_id", "BlacklistID", 140, 140, "p3_blacklist", is_key=True)
    p.add_attribute("p3_bl_reason", "Reason", 140, 220, "p3_blacklist")
    p.add_attribute("p3_bl_date", "Date", 140, 290, "p3_blacklist")
    
    # BLACKLISTED: CUSTOMER (1) - BLACKLIST (N, total)
    p.add_relationship("p3_rel_blacklisted", "BLACKLISTED", 630, 220)
    p.connect("p3_customer", "p3_rel_blacklisted", card="1", is_total=False)
    p.connect("p3_blacklist", "p3_rel_blacklisted", card="N", is_total=True)
    
    p.add_entity("p3_employee_dashed", "EMPLOYEE", 300, 480, 140, 55, is_dashed=True)
    p.add_relationship("p3_rel_decided_by", "DECIDED_BY", 300, 350)
    p.connect("p3_employee_dashed", "p3_rel_decided_by", card="1", is_total=False)
    p.connect("p3_blacklist", "p3_rel_decided_by", card="N", is_total=True)
    
    # CORPORATE_DISCOUNT (Weak Entity)
    p.add_entity("p3_corp_discount", "CORPORATE_DISCOUNT", 1650, 1150, 200, 65, is_weak=True)
    # Partial key: StartDate
    p.add_attribute("p3_cd_start", "StartDate", 1520, 1260, "p3_corp_discount", is_partial=True)
    p.add_attribute("p3_cd_pct", "DiscountPct", 1670, 1270, "p3_corp_discount")
    p.add_attribute("p3_cd_end", "EndDate", 1820, 1260, "p3_corp_discount")
    
    # Identifying relationship: HAS_DISCOUNT
    p.add_relationship("p3_rel_has_discount", "HAS_DISCOUNT", 1520, 930, is_identifying=True)
    p.connect("p3_corporate", "p3_rel_has_discount", card="1", is_total=False)
    p.connect("p3_corp_discount", "p3_rel_has_discount", card="N", is_total=True)
    
    p.add_entity("p3_category_dashed", "CATEGORY", 1150, 1150, 140, 55, is_dashed=True)
    p.add_relationship("p3_rel_applies_to", "APPLIES_TO", 1400, 1150)
    p.connect("p3_category_dashed", "p3_rel_applies_to", card="1", is_total=False)
    p.connect("p3_corp_discount", "p3_rel_applies_to", card="N", is_total=True)
    
    return p.build_diagram_compressed()

# ==============================================================================
# PAGE 4: 1-ERD-4-Rentals
# ==============================================================================
def build_page_4():
    p = PageBuilder("p4", "1-ERD-4-Rentals", "Page 4: Rentals — DriveNow ERD (Chen Notation) — Name: عبدالرحمن عزت فتوح — Group 2", width=3000, height=2200)
    
    p.add_entity("p4_customer_dashed", "CUSTOMER", 200, 320, 140, 55, is_dashed=True)
    p.add_entity("p4_category_dashed", "CATEGORY", 800, 180, 140, 55, is_dashed=True)
    p.add_entity("p4_branch_dashed", "BRANCH", 200, 720, 140, 55, is_dashed=True)
    p.add_entity("p4_vehicle_dashed", "VEHICLE", 2150, 720, 140, 55, is_dashed=True)
    p.add_entity("p4_employee_dashed", "EMPLOYEE", 1200, 1450, 140, 55, is_dashed=True)
    p.add_entity("p4_authdriver_dashed", "AUTHORIZED_DRIVER", 2150, 1100, 180, 55, is_dashed=True)
    
    p.add_entity("p4_promo", "PROMO_CODE", 1450, 180, 150, 60)
    p.add_attribute("p4_pr_code", "Code", 1330, 90, "p4_promo", is_key=True)
    p.add_attribute("p4_pr_pct", "DiscountPct", 1470, 75, "p4_promo")
    p.add_attribute("p4_pr_from", "ValidFrom", 1610, 85, "p4_promo")
    p.add_attribute("p4_pr_to", "ValidTo", 1660, 150, "p4_promo")
    p.add_attribute("p4_pr_max", "MaxUses", 1660, 220, "p4_promo")
    p.add_attribute("p4_pr_used", "UsedCount", 1570, 270, "p4_promo", is_derived=True)
    
    p.add_entity("p4_reservation", "RESERVATION", 750, 480, 160, 65)
    p.add_attribute("p4_res_no", "ReservationNo", 570, 440, "p4_reservation", is_key=True)
    p.add_attribute("p4_res_made", "MadeDateTime", 600, 370, "p4_reservation")
    p.add_attribute("p4_res_pickdt", "RequestedPickupDateTime", 750, 350, "p4_reservation", w=160)
    p.add_attribute("p4_res_retdt", "RequestedReturnDateTime", 950, 360, "p4_reservation", w=160)
    p.add_attribute("p4_res_stat", "Status", 990, 440, "p4_reservation")
    p.add_attribute("p4_res_chan", "BookingChannel", 970, 520, "p4_reservation")
    
    p.add_relationship("p4_rel_makes", "MAKES", 480, 390)
    p.connect("p4_customer_dashed", "p4_rel_makes", card="1", is_total=False)
    p.connect("p4_reservation", "p4_rel_makes", card="N", is_total=True)
    
    p.add_relationship("p4_rel_reserves", "RESERVES", 800, 330)
    p.connect("p4_category_dashed", "p4_rel_reserves", card="1", is_total=False)
    p.connect("p4_reservation", "p4_rel_reserves", card="N", is_total=True)
    
    p.add_relationship("p4_rel_pick_at", "PICKUP_AT", 480, 560)
    p.connect("p4_branch_dashed", "p4_rel_pick_at", card="1", is_total=False)
    p.connect("p4_reservation", "p4_rel_pick_at", card="N", is_total=True)
    
    p.add_relationship("p4_rel_ret_at", "RETURN_AT", 480, 640)
    p.connect("p4_branch_dashed", "p4_rel_ret_at", card="1", is_total=False)
    p.connect("p4_reservation", "p4_rel_ret_at", card="N", is_total=True)
    
    p.add_relationship("p4_rel_uses_promo", "USES_PROMO", 1130, 330)
    p.connect("p4_promo", "p4_rel_uses_promo", card="1", is_total=False)
    p.connect("p4_reservation", "p4_rel_uses_promo", card="N", is_total=False)
    
    p.add_entity("p4_rental", "RENTAL", 1200, 800, 160, 65)
    p.add_attribute("p4_rent_no", "RentalNo", 1000, 710, "p4_rental", is_key=True)
    p.add_attribute("p4_rent_pickdt", "PickupDateTime", 1150, 690, "p4_rental")
    p.add_attribute("p4_rent_expdt", "ExpectedReturnDateTime", 1320, 690, "p4_rental", w=150)
    p.add_attribute("p4_rent_actdt", "ActualReturnDateTime", 1430, 750, "p4_rental", w=140)
    p.add_attribute("p4_rent_pickodo", "PickupOdometer", 1440, 830, "p4_rental")
    p.add_attribute("p4_rent_retodo", "ReturnOdometer", 1420, 910, "p4_rental")
    p.add_attribute("p4_rent_pickfuel", "PickupFuelPct", 1340, 970, "p4_rental")
    p.add_attribute("p4_rent_retfuel", "ReturnFuelPct", 1180, 980, "p4_rental")
    p.add_attribute("p4_rent_latefee", "LateFee", 1030, 950, "p4_rental")
    
    p.add_relationship("p4_rel_fulfills", "FULFILLS", 980, 630)
    p.connect("p4_reservation", "p4_rel_fulfills", card="1", is_total=False)
    p.connect("p4_rental", "p4_rel_fulfills", card="1", is_total=False)
    
    p.add_relationship("p4_rel_rents", "RENTS", 1720, 750)
    p.connect("p4_vehicle_dashed", "p4_rel_rents", card="1", is_total=False)
    p.connect("p4_rental", "p4_rel_rents", card="N", is_total=True)
    
    p.add_relationship("p4_rel_rented_by", "RENTED_BY", 600, 850)
    p.connect("p4_customer_dashed", "p4_rel_rented_by", card="1", is_total=False)
    p.connect("p4_rental", "p4_rel_rented_by", card="N", is_total=True)
    
    p.add_relationship("p4_rel_pick_br", "PICKUP_BRANCH", 600, 750)
    p.connect("p4_branch_dashed", "p4_rel_pick_br", card="1", is_total=False)
    p.connect("p4_rental", "p4_rel_pick_br", card="N", is_total=True)
    
    p.add_relationship("p4_rel_ret_br", "RETURN_BRANCH", 750, 880)
    p.connect("p4_branch_dashed", "p4_rel_ret_br", card="1", is_total=False)
    p.connect("p4_rental", "p4_rel_ret_br", card="N", is_total=True)
    
    p.add_relationship("p4_rel_handed", "HANDED_OVER_BY", 1080, 1150)
    p.connect("p4_employee_dashed", "p4_rel_handed", card="1", is_total=False)
    p.connect("p4_rental", "p4_rel_handed", card="N", is_total=True)
    
    p.add_relationship("p4_rel_received", "RECEIVED_BY", 1330, 1150)
    p.connect("p4_employee_dashed", "p4_rel_received", card="1", is_total=False)
    p.connect("p4_rental", "p4_rel_received", card="N", is_total=False)
    
    p.add_relationship("p4_rel_main_driver", "MAIN_DRIVER", 1750, 960)
    p.connect("p4_authdriver_dashed", "p4_rel_main_driver", card="1", is_total=False)
    p.connect("p4_rental", "p4_rel_main_driver", card="N", is_total=False)
    
    # Recursive 1:1 EXTENDS
    p.add_relationship("p4_rel_extends", "EXTENDS", 880, 830)
    p.connect("p4_rental", "p4_rel_extends", card="1", role="Original", is_total=False)
    p.connect("p4_rel_extends", "p4_rental", card="1", role="Extension", is_total=False)
    
    # ADDITIONAL_DRIVER (Weak Entity)
    p.add_entity("p4_add_driver", "ADDITIONAL_DRIVER", 1750, 1250, 180, 60, is_weak=True)
    # Partial key: DriverSeq
    p.add_attribute("p4_ad_seq", "DriverSeq", 1580, 1340, "p4_add_driver", is_partial=True)
    p.add_attribute("p4_ad_fee", "DailyFee", 1740, 1370, "p4_add_driver")
    p.add_attribute("p4_ad_name", "Name", 1890, 1370, "p4_add_driver")
    p.add_attribute("p4_ad_lic", "LicenseNo", 1990, 1320, "p4_add_driver")
    
    # Identifying relationship: HAS_ADDITIONAL
    p.add_relationship("p4_rel_has_add", "HAS_ADDITIONAL", 1540, 1070, is_identifying=True)
    p.connect("p4_rental", "p4_rel_has_add", card="1", is_total=False)
    p.connect("p4_add_driver", "p4_rel_has_add", card="N", is_total=True)
    
    return p.build_diagram_compressed()

# ==============================================================================
# PAGE 5: 1-ERD-5-Extras-Payments (FEEDBACK is now a Weak Entity!)
# ==============================================================================
def build_page_5():
    p = PageBuilder("p5", "1-ERD-5-Extras-Payments", "Page 5: Extras &amp; Payments — DriveNow ERD (Chen Notation) — Name: عبدالرحمن عزت فتوح — Group 2", width=2800, height=2000)
    
    p.add_entity("p5_rental_dashed", "RENTAL", 1000, 750, 160, 65, is_dashed=True)
    
    # EXTRA
    p.add_entity("p5_extra", "EXTRA", 300, 250, 150, 60)
    p.add_attribute("p5_ex_code", "ExtraCode", 150, 180, "p5_extra", is_key=True)
    p.add_attribute("p5_ex_name", "Name", 300, 150, "p5_extra")
    p.add_attribute("p5_ex_daily", "DailyCharge", 460, 180, "p5_extra")
    
    p.add_relationship("p5_rel_inc_extra", "INCLUDES_EXTRA", 650, 500)
    p.add_attribute("p5_attr_ex_qty", "Quantity", 570, 410, "p5_rel_inc_extra")
    p.add_attribute("p5_attr_ex_charge", "ChargeAtRental", 710, 410, "p5_rel_inc_extra", w=130)
    p.connect("p5_rental_dashed", "p5_rel_inc_extra", card="M", is_total=False)
    p.connect("p5_extra", "p5_rel_inc_extra", card="N", is_total=False)
    
    # INSURANCE_PACKAGE
    p.add_entity("p5_insurance", "INSURANCE_PACKAGE", 1750, 250, 180, 60)
    p.add_attribute("p5_ins_code", "PackageCode", 1600, 150, "p5_insurance", is_key=True)
    p.add_attribute("p5_ins_name", "Name", 1760, 130, "p5_insurance")
    p.add_attribute("p5_ins_daily", "DailyPrice", 1920, 150, "p5_insurance")
    p.add_attribute("p5_ins_cov", "MaxCoverage", 1960, 230, "p5_insurance")
    p.add_attribute("p5_ins_ded", "Deductible", 1950, 310, "p5_insurance")
    
    p.add_relationship("p5_rel_inc_ins", "INCLUDES_INSURANCE", 1380, 500, w=160)
    p.add_attribute("p5_attr_ins_price", "PriceCharged", 1470, 410, "p5_rel_inc_ins")
    p.connect("p5_rental_dashed", "p5_rel_inc_ins", card="M", is_total=False)
    p.connect("p5_insurance", "p5_rel_inc_ins", card="N", is_total=False)
    
    # PAYMENT
    p.add_entity("p5_payment", "PAYMENT", 300, 750, 150, 60)
    p.add_attribute("p5_pay_id", "PaymentID", 130, 650, "p5_payment", is_key=True)
    p.add_attribute("p5_pay_amt", "Amount", 110, 730, "p5_payment")
    p.add_attribute("p5_pay_dt", "PaymentDateTime", 110, 810, "p5_payment", w=135)
    p.add_attribute("p5_pay_type", "PaymentType", 180, 880, "p5_payment")
    p.add_attribute("p5_pay_meth", "Method", 310, 890, "p5_payment")
    p.add_attribute("p5_pay_ref", "TransactionRef", 440, 870, "p5_payment", w=130)
    
    p.add_relationship("p5_rel_pays", "PAYS", 650, 750)
    p.connect("p5_rental_dashed", "p5_rel_pays", card="1", is_total=False)
    p.connect("p5_payment", "p5_rel_pays", card="N", is_total=True)
    
    # FEEDBACK (Weak Entity on RENTAL)
    p.add_entity("p5_feedback", "FEEDBACK", 500, 1250, 160, 65, is_weak=True)
    # Partial key: FeedbackNo
    p.add_attribute("p5_fb_no", "FeedbackNo", 330, 1250, "p5_feedback", is_partial=True)
    p.add_attribute("p5_fb_rating", "Rating", 380, 1340, "p5_feedback")
    p.add_attribute("p5_fb_comm", "Comment", 520, 1370, "p5_feedback")
    p.add_attribute("p5_fb_date", "SubmissionDate", 660, 1350, "p5_feedback", w=130)
    
    # Identifying relationship: GIVES_FEEDBACK (1:1 Identifying, FEEDBACK total)
    p.add_relationship("p5_rel_feedback", "GIVES_FEEDBACK", 720, 1020, w=150, is_identifying=True)
    p.connect("p5_rental_dashed", "p5_rel_feedback", card="1", is_total=False)
    p.connect("p5_feedback", "p5_rel_feedback", card="1", is_total=True)
    
    # TRAFFIC_VIOLATION
    p.add_entity("p5_violation", "TRAFFIC_VIOLATION", 1600, 1250, 180, 65)
    p.add_attribute("p5_v_no", "ViolationNo", 1450, 1360, "p5_violation", is_key=True)
    p.add_attribute("p5_v_dt", "ViolationDateTime", 1600, 1390, "p5_violation", w=140)
    p.add_attribute("p5_v_loc", "Location", 1750, 1380, "p5_violation")
    p.add_attribute("p5_v_type", "Type", 1850, 1320, "p5_violation")
    p.add_attribute("p5_v_fine", "FineAmount", 1850, 1230, "p5_violation")
    
    p.add_relationship("p5_rel_occurred", "OCCURRED_DURING", 1320, 1020, w=160)
    p.connect("p5_rental_dashed", "p5_rel_occurred", card="1", is_total=False)
    p.connect("p5_violation", "p5_rel_occurred", card="N", is_total=True)
    
    return p.build_diagram_compressed()

# ==============================================================================
# PAGE 6: 1-ERD-6-Maintenance
# ==============================================================================
def build_page_6():
    p = PageBuilder("p6", "1-ERD-6-Maintenance", "Page 6: Maintenance — DriveNow ERD (Chen Notation) — Name: عبدالرحمن عزت فتوح — Group 2", width=2800, height=2000)
    
    p.add_entity("p6_rental_dashed", "RENTAL", 250, 320, 140, 55, is_dashed=True)
    p.add_entity("p6_employee_dashed", "EMPLOYEE", 250, 580, 140, 55, is_dashed=True)
    p.add_entity("p6_vehicle_dashed", "VEHICLE", 1750, 320, 140, 55, is_dashed=True)
    p.add_entity("p6_mechanic_dashed", "MECHANIC", 700, 1150, 140, 55, is_dashed=True)
    
    # DAMAGE_REPORT (Weak Entity)
    p.add_entity("p6_damage_rep", "DAMAGE_REPORT", 720, 450, 160, 60, is_weak=True)
    # Partial key: ReportNo
    p.add_attribute("p6_dr_no", "ReportNo", 560, 480, "p6_damage_rep", is_partial=True)
    p.add_attribute("p6_dr_desc", "Description", 600, 560, "p6_damage_rep")
    p.add_attribute("p6_dr_sev", "Severity", 730, 580, "p6_damage_rep")
    p.add_attribute("p6_dr_est", "EstimatedRepairCost", 860, 560, "p6_damage_rep", w=140)
    
    # Identifying relationship: HAS_DAMAGE
    p.add_relationship("p6_rel_has_damage", "HAS_DAMAGE", 480, 380, is_identifying=True)
    p.connect("p6_rental_dashed", "p6_rel_has_damage", card="1", is_total=False)
    p.connect("p6_damage_rep", "p6_rel_has_damage", card="N", is_total=True)
    
    p.add_relationship("p6_rel_rep_by", "REPORTED_BY", 480, 510)
    p.connect("p6_employee_dashed", "p6_rel_rep_by", card="1", is_total=False)
    p.connect("p6_damage_rep", "p6_rel_rep_by", card="N", is_total=True)
    
    # DAMAGE_PHOTO (Weak Entity)
    p.add_entity("p6_damage_photo", "DAMAGE_PHOTO", 1250, 260, 160, 60, is_weak=True)
    # Partial key: PhotoNo
    p.add_attribute("p6_dp_no", "PhotoNo", 1200, 150, "p6_damage_photo", is_partial=True)
    p.add_attribute("p6_dp_url", "PhotoURL", 1370, 160, "p6_damage_photo")
    
    # Identifying relationship: HAS_PHOTO
    p.add_relationship("p6_rel_has_photo", "HAS_PHOTO", 1020, 340, is_identifying=True)
    p.connect("p6_damage_rep", "p6_rel_has_photo", card="1", is_total=False)
    p.connect("p6_damage_photo", "p6_rel_has_photo", card="N", is_total=True)
    
    # JOB_CARD
    p.add_entity("p6_job_card", "JOB_CARD", 1250, 650, 150, 60)
    p.add_attribute("p6_jc_no", "JobNo", 1080, 600, "p6_job_card", is_key=True)
    p.add_attribute("p6_jc_in", "DateIn", 1130, 530, "p6_job_card")
    p.add_attribute("p6_jc_out", "DateOut", 1290, 520, "p6_job_card")
    p.add_attribute("p6_jc_work", "WorkType", 1430, 540, "p6_job_card")
    p.add_attribute("p6_jc_cost", "TotalCost", 1450, 620, "p6_job_card")
    
    p.add_relationship("p6_rel_for_veh", "FOR_VEHICLE", 1540, 480)
    p.connect("p6_vehicle_dashed", "p6_rel_for_veh", card="1", is_total=False)
    p.connect("p6_job_card", "p6_rel_for_veh", card="N", is_total=True)
    
    p.add_relationship("p6_rel_results", "RESULTS_FROM", 1020, 560)
    p.connect("p6_damage_rep", "p6_rel_results", card="1", is_total=False)
    p.connect("p6_job_card", "p6_rel_results", card="1", is_total=False)
    
    p.add_relationship("p6_rel_works_on", "WORKS_ON", 1020, 900)
    p.add_attribute("p6_attr_hours", "HoursSpent", 1020, 990, "p6_rel_works_on")
    p.connect("p6_mechanic_dashed", "p6_rel_works_on", card="M", is_total=False)
    p.connect("p6_job_card", "p6_rel_works_on", card="N", is_total=False)
    
    p.add_entity("p6_part", "PART", 1850, 650, 150, 60)
    p.add_attribute("p6_pt_no", "PartNo", 1750, 770, "p6_part", is_key=True)
    p.add_attribute("p6_pt_name", "Name", 1890, 780, "p6_part")
    p.add_attribute("p6_pt_cost", "CurrentUnitCost", 2030, 760, "p6_part")
    p.add_attribute("p6_pt_qty", "QtyInStock", 2050, 680, "p6_part")
    
    p.add_relationship("p6_rel_uses_part", "USES_PART", 1570, 650)
    p.add_attribute("p6_attr_qty_used", "QtyUsed", 1500, 750, "p6_rel_uses_part")
    p.add_attribute("p6_attr_unit_cost", "UnitCostAtTime", 1630, 750, "p6_rel_uses_part")
    p.connect("p6_job_card", "p6_rel_uses_part", card="M", is_total=False)
    p.connect("p6_part", "p6_rel_uses_part", card="N", is_total=False)
    
    p.add_entity("p6_supplier", "SUPPLIER", 1850, 1150, 150, 60)
    p.add_attribute("p6_sup_id", "SupplierID", 1680, 1260, "p6_supplier", is_key=True)
    p.add_attribute("p6_sup_name", "Name", 1840, 1280, "p6_supplier")
    p.add_attribute("p6_sup_phone", "Phone", 1990, 1260, "p6_supplier")
    p.add_attribute("p6_sup_email", "Email", 2050, 1180, "p6_supplier")
    
    p.add_relationship("p6_rel_supplies", "SUPPLIES", 1850, 900)
    p.add_attribute("p6_attr_uprice", "UnitPrice", 1720, 900, "p6_rel_supplies")
    p.add_attribute("p6_attr_lead", "LeadTimeDays", 1990, 900, "p6_rel_supplies")
    p.connect("p6_supplier", "p6_rel_supplies", card="M", is_total=False)
    p.connect("p6_part", "p6_rel_supplies", card="N", is_total=False)
    
    return p.build_diagram_compressed()

# ==============================================================================
# PAGE 7: 1-ERD-7-Loyalty
# ==============================================================================
def build_page_7():
    p = PageBuilder("p7", "1-ERD-7-Loyalty", "Page 7: Loyalty — DriveNow ERD (Chen Notation) — Name: عبدالرحمن عزت فتوح — Group 2", width=2200, height=1500)
    
    p.add_entity("p7_individual_dashed", "INDIVIDUAL", 200, 500, 150, 60, is_dashed=True)
    
    p.add_entity("p7_loyalty_account", "LOYALTY_ACCOUNT", 800, 500, 180, 65)
    p.add_attribute("p7_la_id", "AccountID", 720, 370, "p7_loyalty_account", is_key=True)
    p.add_attribute("p7_la_tier", "Tier", 880, 360, "p7_loyalty_account", is_derived=True)
    p.add_attribute("p7_la_points", "TotalPoints", 1020, 420, "p7_loyalty_account", is_derived=True)
    
    # HAS_ACCOUNT: 1:1, both total
    p.add_relationship("p7_rel_has_account", "HAS_ACCOUNT", 500, 500)
    p.connect("p7_individual_dashed", "p7_rel_has_account", card="1", is_total=True)
    p.connect("p7_loyalty_account", "p7_rel_has_account", card="1", is_total=True)
    
    # POINT_TRANSACTION (Weak Entity)
    p.add_entity("p7_point_txn", "POINT_TRANSACTION", 1500, 500, 190, 65, is_weak=True)
    # Partial key: TxnNo
    p.add_attribute("p7_pt_no", "TxnNo", 1450, 370, "p7_point_txn", is_partial=True)
    p.add_attribute("p7_pt_date", "TxnDate", 1600, 360, "p7_point_txn")
    p.add_attribute("p7_pt_points", "Points", 1720, 430, "p7_point_txn")
    p.add_attribute("p7_pt_type", "Type", 1730, 520, "p7_point_txn")
    
    # Identifying relationship: HAS_TXN
    p.add_relationship("p7_rel_has_txn", "HAS_TXN", 1180, 500, is_identifying=True)
    p.connect("p7_loyalty_account", "p7_rel_has_txn", card="1", is_total=False)
    p.connect("p7_point_txn", "p7_rel_has_txn", card="N", is_total=True)
    
    p.add_entity("p7_rental_dashed", "RENTAL", 1500, 950, 150, 60, is_dashed=True)
    
    p.add_relationship("p7_rel_related_to", "RELATED_TO", 1520, 750)
    p.connect("p7_rental_dashed", "p7_rel_related_to", card="1", is_total=False)
    p.connect("p7_point_txn", "p7_rel_related_to", card="N", is_total=False)
    
    return p.build_diagram_compressed()

# ==============================================================================
# MAIN ASSEMBLER
# ==============================================================================
def assemble_all():
    print("Building Page 1...")
    p1 = build_page_1()
    print("Building Page 2...")
    p2 = build_page_2()
    print("Building Page 3...")
    p3 = build_page_3()
    print("Building Page 4...")
    p4 = build_page_4()
    print("Building Page 5...")
    p5 = build_page_5()
    print("Building Page 6...")
    p6 = build_page_6()
    print("Building Page 7...")
    p7 = build_page_7()
    
    full_file = (
        '<mxfile host="Electron">\n'
        f'{p1}\n'
        f'{p2}\n'
        f'{p3}\n'
        f'{p4}\n'
        f'{p5}\n'
        f'{p6}\n'
        f'{p7}\n'
        '</mxfile>\n'
    )
    
    out_path = "e:/submission/DataBaseAssignment1/DriveNow.drawio"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_file)
    print(f"Successfully generated all 7 compressed pages into {out_path} ({len(full_file)} bytes)")

if __name__ == "__main__":
    assemble_all()
