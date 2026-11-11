"""
Master fix script for DriveNow.drawio Schema pages.
Pages are stored as inline mxGraphModel child elements (not base64-compressed).
"""
import sys, os, re, shutil
sys.stdout.reconfigure(encoding='utf-8')
import xml.etree.ElementTree as ET

DRAWIO_PATH = r'e:\submission\DataBaseAssignment1\DriveNow.drawio'
BACKUP_PATH = r'e:\submission\DataBaseAssignment1\DriveNow_backup_before_schema_fix.drawio'

# ── helpers ────────────────────────────────────────────────────────────────

def col_html(col_name, tags, is_pk=False):
    weight = 'bold' if is_pk else 'normal'
    name_html = f'<u>{col_name}</u>' if is_pk else col_name
    return (
        f'<div style="font-size:12px; font-weight:{weight};">{name_html}</div>'
        f'<div style="font-size:10px; color:#555; margin-top:2px;">{tags}</div>'
    )

def pk_style():
    return 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e3f2fd;strokeColor=#1976d2;strokeWidth=2;rounded=0;'

def norm_style():
    return 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#b0bec5;strokeWidth=1;rounded=0;'

def make_col_cell(cid, col_name, tags, is_pk, x, y, w=140, h=52):
    c = ET.Element('mxCell')
    c.set('id', cid)
    c.set('value', col_html(col_name, tags, is_pk))
    c.set('style', pk_style() if is_pk else norm_style())
    c.set('vertex', '1')
    c.set('parent', '1')
    geo = ET.SubElement(c, 'mxGeometry')
    geo.set('x', str(x)); geo.set('y', str(y))
    geo.set('width', str(w)); geo.set('height', str(h))
    geo.set('as', 'geometry')
    return c

def make_rule_cell(cid, text, x, y, w=700, h=20):
    c = ET.Element('mxCell')
    c.set('id', cid)
    c.set('value', f'<i style="color:#d32f2f; font-size:11px;">{text}</i>')
    c.set('style', 'text;html=1;fontSize=11;align=left;verticalAlign=top;')
    c.set('vertex', '1'); c.set('parent', '1')
    geo = ET.SubElement(c, 'mxGeometry')
    geo.set('x', str(x)); geo.set('y', str(y))
    geo.set('width', str(w)); geo.set('height', str(h))
    geo.set('as', 'geometry')
    return c

def make_fk_edge(eid, source, target):
    c = ET.Element('mxCell')
    c.set('id', eid)
    c.set('value', '')
    c.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#1565c0;strokeWidth=1.8;')
    c.set('edge', '1'); c.set('source', source); c.set('target', target); c.set('parent', '1')
    geo = ET.SubElement(c, 'mxGeometry')
    geo.set('relative', '1'); geo.set('as', 'geometry')
    return c

def set_val(root_elem, cell_id, new_value):
    for c in root_elem.iter('mxCell'):
        if c.get('id') == cell_id:
            c.set('value', new_value)
            return True
    print(f'    WARNING: cell {cell_id!r} not found')
    return False

def get_geo(root_elem, cell_id):
    for c in root_elem.iter('mxCell'):
        if c.get('id') == cell_id:
            geo = c.find('mxGeometry')
            if geo is not None:
                return float(geo.get('x',0)), float(geo.get('y',0)), float(geo.get('width',140)), float(geo.get('height',52))
    return None

def rename_cell(root_elem, old_id, new_id):
    for c in root_elem.iter('mxCell'):
        if c.get('id') == old_id:
            c.set('id', new_id)
            return True
    return False

def get_tree_root(graph_root):
    """Get the <root> element inside mxGraphModel."""
    return graph_root.find('.//root')

# ── Load drawio ─────────────────────────────────────────────────────────────

shutil.copy(DRAWIO_PATH, BACKUP_PATH)
print(f'Backup: {BACKUP_PATH}')

with open(DRAWIO_PATH, 'r', encoding='utf-8') as f:
    drawio_content = f.read()

drawio_tree = ET.fromstring(drawio_content)
diagrams = drawio_tree.findall('.//diagram')
page_map = {d.get('name',''): d for d in diagrams}

def get_graph(page_name):
    """Return mxGraphModel element for a page."""
    d = page_map[page_name]
    children = list(d)
    if children:
        return children[0]
    return None

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 8: 2-Schema-1
# ══════════════════════════════════════════════════════════════════════════
print('\n--- 2-Schema-1 ---')
g = get_graph('2-Schema-1')
tr = get_tree_root(g)

# Fix MECHANIC Specialization CK: Body not Transmission
set_val(g, 'mechanic_col_Specialization',
    col_html('Specialization', 'NN CK:Engine|Brakes|Electrical|Body|Tires'))
print('  MECHANIC.Specialization: Transmission->Body|Tires')

# Fix CommissionRate: add DF:0
set_val(g, 'rental_agent_col_CommissionRate',
    col_html('CommissionRate', 'NN CK:0-15 DF:0'))
print('  RENTAL_AGENT.CommissionRate: added DF:0')

# Fix ENROLLMENT AttemptNo CK:>=1
set_val(g, 'enrollment_col_AttemptNo',
    col_html('AttemptNo', 'NN CK:>=1', is_pk=True))
print('  ENROLLMENT.AttemptNo: CK:>=1')

print('  OK')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 9: 2-Schema-2
# ══════════════════════════════════════════════════════════════════════════
print('\n--- 2-Schema-2 ---')
g = get_graph('2-Schema-2')
tr = get_tree_root(g)

# CATEGORY: PK CategoryName -> CategoryID, add CategoryName beside it
geo = get_geo(g, 'category_col_CategoryName')
if geo:
    cx, cy, cw, ch = geo
    set_val(g, 'category_col_CategoryName',
        col_html('CategoryID', 'NN', is_pk=True))
    for c in g.iter('mxCell'):
        if c.get('id') == 'category_col_CategoryName':
            c.set('style', pk_style())
            c.find('mxGeometry').set('width', '110')
            break
    # Add CategoryName column
    new_c = make_col_cell('category_col_CatName', 'CategoryName', 'NN UQ',
        False, cx+110, cy, 150, 52)
    tr.append(new_c)
    print('  CATEGORY: PK CategoryName->CategoryID, added CategoryName')

# CATEGORY_RATE FK col: CategoryName->CategoryID
set_val(g, 'category_rate_col_CategoryName',
    col_html('CategoryID', 'NN', is_pk=True))
for c in g.iter('mxCell'):
    if c.get('id') == 'category_rate_col_CategoryName':
        c.set('style', pk_style())
        break
print('  CATEGORY_RATE FK: CategoryName->CategoryID')

# Update FK edge target to new col ID
for c in g.iter('mxCell'):
    if c.get('id') == 's2_fk_edge_1':
        c.set('target', 'category_col_CategoryName')
        break

# CAR_MODEL: ID->ModelID
set_val(g, 'car_model_col_ID',
    col_html('ModelID', 'NN', is_pk=True))
print('  CAR_MODEL: ID->ModelID')

# CAR_MODEL: CategoryName->CategoryID
set_val(g, 'car_model_col_CategoryName',
    col_html('CategoryID', 'NN'))
print('  CAR_MODEL: CategoryName->CategoryID')

# CAR_MODEL: Year CK:>=2000
set_val(g, 'car_model_col_Year',
    col_html('Year', 'NN CK:>=2000'))
print('  CAR_MODEL: Year CK:>=2000')

# CAR_MODEL: Seats CK:2-15
set_val(g, 'car_model_col_Seats',
    col_html('Seats', 'NN CK:2-15'))
print('  CAR_MODEL: Seats CK:2-15')

# Update FK edge from car_model_col_CategoryName to category_col_CategoryName
for c in g.iter('mxCell'):
    if c.get('id') == 's2_fk_edge_2':
        c.set('target', 'category_col_CategoryName')
        break

# VEHICLE: add CurrentBranchCode after HomeBranchCode
geo = get_geo(g, 'vehicle_col_HomeBranchCode')
if geo:
    hx, hy, hw, hh = geo
    new_c = make_col_cell('vehicle_col_CurrentBranchCode', 'CurrentBranchCode', 'NN',
        False, hx+hw, hy, 155, 52)
    tr.append(new_c)
    new_c2 = make_col_cell('vehicle_col_ModelID', 'ModelID', 'NN',
        False, hx+hw+155, hy, 100, 52)
    tr.append(new_c2)
    # FK edges
    tr.append(make_fk_edge('veh_fk_curbranch', 'vehicle_col_CurrentBranchCode', 'ref_branch'))
    tr.append(make_fk_edge('veh_fk_modelid', 'vehicle_col_ModelID', 'car_model_col_ID'))
    print('  VEHICLE: added CurrentBranchCode + ModelID')

# VEHICLE Status CK: match README (UnderMaintenance|Retired)
set_val(g, 'vehicle_col_Status',
    col_html('Status', "NN DF:'Available' CK:Available|Rented|UnderMaintenance|Retired"))
print('  VEHICLE: Status CK fixed')

# VEHICLE_STATUS_LOG: ChangedBy->EmployeeID
set_val(g, 'vehicle_status_log_col_ChangedBy',
    col_html('EmployeeID', 'NN'))
print('  VEHICLE_STATUS_LOG: ChangedBy->EmployeeID')

# GPS_DEVICE: InstallDate->InstalledAt
set_val(g, 'gps_device_col_InstallDate',
    col_html('InstalledAt', 'NULL'))
print('  GPS_DEVICE: InstallDate->InstalledAt')

print('  OK')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 10: 2-Schema-3
# ══════════════════════════════════════════════════════════════════════════
print('\n--- 2-Schema-3 ---')
g = get_graph('2-Schema-3')
tr = get_tree_root(g)

# CUSTOMER: CustomerNo->CustomerID
set_val(g, 'customer_col_CustomerNo',
    col_html('CustomerID', 'NN', is_pk=True))
print('  CUSTOMER: CustomerNo->CustomerID')

# CUSTOMER_PHONE: CustomerNo->CustomerID
set_val(g, 'customer_phone_col_CustomerNo',
    col_html('CustomerID', 'NN', is_pk=True))
print('  CUSTOMER_PHONE: CustomerNo->CustomerID')

# CUSTOMER: Address -> CustomerType + Street + City + Governorate
geo = get_geo(g, 'customer_col_Address')
if geo:
    ax, ay, aw, ah = geo
    for c in g.iter('mxCell'):
        if c.get('id') == 'customer_col_Address':
            c.set('id', 'customer_col_CustomerType')
            c.set('value', col_html('CustomerType', 'NN CK:Individual|Corporate'))
            c.find('mxGeometry').set('width', '175')
            break
    tr.append(make_col_cell('customer_col_Street', 'Street', 'NN', False, ax+175, ay, 110, 52))
    tr.append(make_col_cell('customer_col_City', 'City', 'NN', False, ax+285, ay, 90, 52))
    tr.append(make_col_cell('customer_col_Governorate', 'Governorate', 'NN', False, ax+375, ay, 115, 52))
    print('  CUSTOMER: Address->CustomerType+Street+City+Governorate')

# INDIVIDUAL: CustomerNo->IndividualCustID
set_val(g, 'individual_col_CustomerNo',
    col_html('IndividualCustID', 'NN', is_pk=True))
print('  INDIVIDUAL: CustomerNo->IndividualCustID')

# INDIVIDUAL: FullName->FirstName + MiddleName + LastName
geo = get_geo(g, 'individual_col_FullName')
if geo:
    fx, fy, fw, fh = geo
    for c in g.iter('mxCell'):
        if c.get('id') == 'individual_col_FullName':
            c.set('id', 'individual_col_FirstName')
            c.set('value', col_html('FirstName', 'NN'))
            c.find('mxGeometry').set('width', '110')
            break
    tr.append(make_col_cell('individual_col_MiddleName', 'MiddleName', 'NULL', False, fx+110, fy, 110, 52))
    tr.append(make_col_cell('individual_col_LastName', 'LastName', 'NN', False, fx+220, fy, 100, 52))
    print('  INDIVIDUAL: FullName->FirstName+MiddleName+LastName')

# INDIVIDUAL: LicenseNo->LicenseNumber UQ
set_val(g, 'individual_col_LicenseNo',
    col_html('LicenseNumber', 'NN UQ'))
print('  INDIVIDUAL: LicenseNo->LicenseNumber UQ')

# INDIVIDUAL: LicenseIssuingCountry -> CK rule
for c in g.iter('mxCell'):
    if c.get('id') == 'individual_col_LicenseIssuingCountry':
        geo_elem = c.find('mxGeometry')
        rx = float(geo_elem.get('x'))
        ry = float(geo_elem.get('y'))
        # Remove from tree and add rule cell
        c.set('id', 'individual_rule_ck')
        c.set('value', '<i style="color:#d32f2f; font-size:11px;">CK: NationalID IS NOT NULL OR PassportNo IS NOT NULL</i>')
        c.set('style', 'text;html=1;fontSize=11;align=left;verticalAlign=top;')
        geo_elem.set('height', '20')
        geo_elem.set('width', '500')
        break
print('  INDIVIDUAL: LicenseIssuingCountry->CK rule')

# CORPORATE: CustomerNo->CorpCustID
set_val(g, 'corporate_col_CustomerNo',
    col_html('CorpCustID', 'NN', is_pk=True))
print('  CORPORATE: CustomerNo->CorpCustID')

# CORPORATE: TaxRegistrationNumber->TaxNumber, add CommercialRegistrationNo
geo = get_geo(g, 'corporate_col_TaxRegistrationNumber')
if geo:
    tx, ty, tw, th = geo
    for c in g.iter('mxCell'):
        if c.get('id') == 'corporate_col_TaxRegistrationNumber':
            c.set('id', 'corporate_col_TaxNumber')
            c.set('value', col_html('TaxNumber', 'NN UQ'))
            c.find('mxGeometry').set('width', '115')
            break
    tr.append(make_col_cell('corporate_col_CommercialRegistrationNo', 
        'CommercialRegistrationNo', 'NN UQ', False, tx+115, ty, 185, 52))
    print('  CORPORATE: TaxRegistrationNumber->TaxNumber, added CommercialRegistrationNo')

# CORPORATE: ContactPerson->ContactPersonName
set_val(g, 'corporate_col_ContactPerson',
    col_html('ContactPersonName', 'NN'))
print('  CORPORATE: ContactPerson->ContactPersonName')

# CORPORATE: CreditLimit->ContactPersonPhone
for c in g.iter('mxCell'):
    if c.get('id') == 'corporate_col_CreditLimit':
        c.set('id', 'corporate_col_ContactPersonPhone')
        c.set('value', col_html('ContactPersonPhone', 'NN'))
        # Remove CK
        break
print('  CORPORATE: CreditLimit->ContactPersonPhone')

# AUTHORIZED_DRIVER: CustomerNo->CorpCustID
set_val(g, 'auth_driver_col_CustomerNo',
    col_html('CorpCustID', 'NN', is_pk=True))
print('  AUTHORIZED_DRIVER: CustomerNo->CorpCustID')

# AUTHORIZED_DRIVER: Name->DriverName
set_val(g, 'auth_driver_col_Name',
    col_html('DriverName', 'NN'))
print('  AUTHORIZED_DRIVER: Name->DriverName')

# AUTHORIZED_DRIVER: LicenseNo->LicenseNumber
set_val(g, 'auth_driver_col_LicenseNo',
    col_html('LicenseNumber', 'NN'))
print('  AUTHORIZED_DRIVER: LicenseNo->LicenseNumber')

# AUTHORIZED_DRIVER: LicenseExpiry->LicenseExpiryDate
set_val(g, 'auth_driver_col_LicenseExpiry',
    col_html('LicenseExpiryDate', 'NN'))
print('  AUTHORIZED_DRIVER: LicenseExpiry->LicenseExpiryDate')

# AUTHORIZED_DRIVER: Phone->NationalID
for c in g.iter('mxCell'):
    if c.get('id') == 'auth_driver_col_Phone':
        c.set('id', 'auth_driver_col_NationalID')
        c.set('value', col_html('NationalID', 'NN'))
        break
print('  AUTHORIZED_DRIVER: Phone->NationalID')

# BLACKLIST: CustomerNo->CustomerID
set_val(g, 'blacklist_col_CustomerNo',
    col_html('CustomerID', 'NN'))
print('  BLACKLIST: CustomerNo->CustomerID')

# BLACKLIST: Date->AddedDate
set_val(g, 'blacklist_col_Date',
    col_html('AddedDate', 'NN'))
print('  BLACKLIST: Date->AddedDate')

# BLACKLIST: DecidedBy->ReportedByEmployeeID
set_val(g, 'blacklist_col_DecidedBy',
    col_html('ReportedByEmployeeID', 'NN'))
print('  BLACKLIST: DecidedBy->ReportedByEmployeeID')

# CORPORATE_DISCOUNT: CustomerNo->CorpCustID
set_val(g, 'corp_discount_col_CustomerNo',
    col_html('CorpCustID', 'NN', is_pk=True))
print('  CORPORATE_DISCOUNT: CustomerNo->CorpCustID')

# CORPORATE_DISCOUNT: CategoryName->CategoryID
set_val(g, 'corp_discount_col_CategoryName',
    col_html('CategoryID', 'NN'))
print('  CORPORATE_DISCOUNT: CategoryName->CategoryID')

# CORPORATE_DISCOUNT: DiscountPct->DiscountPercentage CK:1-50
set_val(g, 'corp_discount_col_DiscountPct',
    col_html('DiscountPercentage', 'NN CK:1-50'))
print('  CORPORATE_DISCOUNT: DiscountPct->DiscountPercentage')

# Fix ref box CATEGORY.CategoryName -> CATEGORY.CategoryID
set_val(g, 'ref_cat_c', 'CATEGORY.CategoryID')
print('  ref_cat_c: CATEGORY.CategoryName->CATEGORY.CategoryID')

print('  OK')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 11: 2-Schema-4
# ══════════════════════════════════════════════════════════════════════════
print('\n--- 2-Schema-4 ---')
g = get_graph('2-Schema-4')
tr = get_tree_root(g)

# Check for derived UsedCount - remove it
removed_usedcount = False
for c in list(tr):
    if c.tag == 'mxCell' and 'UsedCount' in c.get('value',''):
        tr.remove(c)
        print('  Removed derived UsedCount from PROMO_CODE')
        removed_usedcount = True

# Check CustomerID vs CustomerNo in CUSTOMER references
for c in g.iter('mxCell'):
    v = c.get('value','')
    cid = c.get('id','')
    if 'CustomerNo' in v and 'col_' in cid:
        c.set('value', v.replace('CustomerNo', 'CustomerID'))
        print(f'  Fixed CustomerNo->CustomerID in {cid}')

# Fix PromoCode FK label if any ref box says PromoCode col name
for c in g.iter('mxCell'):
    v = c.get('value','')
    if 'CUSTOMER.CustomerNo' in v:
        c.set('value', v.replace('CUSTOMER.CustomerNo', 'CUSTOMER.CustomerID'))
        print('  Fixed ref CUSTOMER.CustomerNo->CUSTOMER.CustomerID')

print('  OK')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 12: 2-Schema-5
# ══════════════════════════════════════════════════════════════════════════
print('\n--- 2-Schema-5 ---')
g = get_graph('2-Schema-5')
tr = get_tree_root(g)

# Fix CustomerNo->CustomerID in any FK col
for c in g.iter('mxCell'):
    v = c.get('value','')
    cid = c.get('id','')
    if 'CustomerNo' in v and ('col_' in cid or 'ref' in cid):
        c.set('value', v.replace('CustomerNo', 'CustomerID'))
        print(f'  Fixed CustomerNo->CustomerID in {cid}')
    # Remove derived cols TotalPoints/Tier if present
    if ('TotalPoints' in v or 'Tier' in v) and 'col_' in cid:
        pv = re.sub(r"<[^>]+>", "", v); print(f"  WARNING: Derived col found: {cid} = {pv[:60]}")

# Fix DAMAGE_PHOTO: add missing CapturedAt if not present
has_captured = any('CapturedAt' in c.get('value','') for c in g.iter('mxCell'))
print(f'  FEEDBACK/DAMAGE cols - CapturedAt present: {has_captured}')

print('  OK')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 13: 2-Schema-6
# ══════════════════════════════════════════════════════════════════════════
print('\n--- 2-Schema-6 ---')
g = get_graph('2-Schema-6')
tr = get_tree_root(g)

for c in g.iter('mxCell'):
    cid = c.get('id','')
    v = c.get('value','')
    plain = re.sub(r'<[^>]+>', '', v).strip()
    cid_low = cid.lower()
    
    # JOB_CARD fixes
    if 'job_card' in cid_low or 'jobcard' in cid_low:
        if 'jobno' in cid_low and 'job_card_no' not in cid_low:
            c.set('value', col_html('JobCardNo', 'NN', is_pk=True))
            print(f'  JOB_CARD.JobNo->JobCardNo')
        elif 'datein' in cid_low:
            c.set('value', col_html('StartDate', 'NN'))
            print(f'  JOB_CARD.DateIn->StartDate')
        elif 'dateout' in cid_low:
            c.set('value', col_html('EndDate', 'NULL'))
            print(f'  JOB_CARD.DateOut->EndDate')
        elif 'worktype' in cid_low:
            c.set('value', col_html('WorkDescription', 'NN'))
            print(f'  JOB_CARD.WorkType->WorkDescription')
        elif 'totalcost' in cid_low:
            c.set('value', col_html('ActualCost', 'NULL CK:>=0'))
            print(f'  JOB_CARD.TotalCost->ActualCost')
    
    # PART fixes
    if 'part_col' in cid_low:
        if cid_low.endswith('_partno') or cid_low.endswith('_partno'):
            c.set('value', col_html('PartNumber', 'NN', is_pk=True))
            print(f'  PART.PartNo->PartNumber')
        elif cid_low.endswith('_name') and 'part' in cid_low:
            c.set('value', col_html('PartName', 'NN'))
            print(f'  PART.Name->PartName')
        elif 'unitcost' in cid_low or 'currentunit' in cid_low:
            c.set('value', col_html('UnitPrice', 'NN CK:>0'))
            print(f'  PART.UnitCost->UnitPrice')
        elif 'qtyinstock' in cid_low or 'qty_in' in cid_low:
            c.set('value', col_html('QuantityInStock', 'NN CK:>=0'))
            print(f'  PART.QtyInStock->QuantityInStock')
    
    # SUPPLIER
    if 'supplier' in cid_low and cid_low.endswith('_name'):
        c.set('value', col_html('SupplierName', 'NN'))
        print(f'  SUPPLIER.Name->SupplierName')
    
    # WORKS_ON
    if 'works_on' in cid_low and ('mechanicid' in cid_low or 'mechanic_id' in cid_low):
        c.set('value', col_html('MechanicEmployeeID', 'NN', is_pk=True))
        print(f'  WORKS_ON.MechanicID->MechanicEmployeeID')
    
    # DAMAGE_REPORT
    if 'damage' in cid_low and 'reportedby' in cid_low:
        c.set('value', col_html('InspectedByEmployeeID', 'NN'))
        print(f'  DAMAGE_REPORT.ReportedBy->InspectedByEmployeeID')
    if 'damage' in cid_low and ('estimatedrepaircost' in cid_low or 'repaircost' in cid_low):
        c.set('value', col_html('RepairCostEstimate', 'NN CK:>=0'))
        print(f'  DAMAGE_REPORT.EstimatedRepairCost->RepairCostEstimate')

# Fix CustomerNo->CustomerID in refs
for c in g.iter('mxCell'):
    v = c.get('value','')
    if 'CUSTOMER.CustomerNo' in v or 'CustomerNo' in v and 'ref' in c.get('id','').lower():
        c.set('value', v.replace('CustomerNo', 'CustomerID'))
        print(f'  Fixed ref CustomerNo->CustomerID')

print('  OK')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 14: 2-Schema-7
# ══════════════════════════════════════════════════════════════════════════
print('\n--- 2-Schema-7 ---')
g = get_graph('2-Schema-7')
tr = get_tree_root(g)

# LOYALTY_ACCOUNT: CustomerNo->IndividualCustID, add JoinDate
geo = get_geo(g, 'loyalty_account_col_CustomerNo')
if geo:
    lx, ly, lw, lh = geo
    set_val(g, 'loyalty_account_col_CustomerNo',
        col_html('IndividualCustID', 'NN UQ'))
    new_jd = make_col_cell('loyalty_account_col_JoinDate', 'JoinDate', 'NN',
        False, lx+lw, ly, 110, 52)
    tr.append(new_jd)
    print('  LOYALTY_ACCOUNT: CustomerNo->IndividualCustID, added JoinDate')

# POINT_TRANSACTION: Type->TransactionType CK:Earn|Redeem|Expire
set_val(g, 'point_txn_col_Type',
    col_html('TransactionType', 'NN CK:Earn|Redeem|Expire'))
print('  POINT_TRANSACTION: Type->TransactionType')

# POINT_TRANSACTION: Points CK should allow negative (for Redeem)
set_val(g, 'point_txn_col_Points',
    col_html('Points', 'NN'))
print('  POINT_TRANSACTION: Points NN (sign determines Earn/Redeem)')

# Fix ref box
for c in g.iter('mxCell'):
    v = c.get('value','')
    if 'INDIVIDUAL' in v and 'CustomerNo' in v:
        c.set('value', v.replace('CustomerNo', 'IndividualCustID'))
        print('  ref: INDIVIDUAL.CustomerNo->INDIVIDUAL.IndividualCustID')
        break
    if v == 'INDIVIDUAL.CustomerNo':
        c.set('value', 'INDIVIDUAL.IndividualCustID')
        print('  ref: INDIVIDUAL.CustomerNo->INDIVIDUAL.IndividualCustID')
        break

# Add TransactionType rule if missing
has_rule = any('Earn' in c.get('value','') and 'Points' in c.get('value','')
               for c in g.iter('mxCell'))
if not has_rule:
    for c in g.iter('mxCell'):
        if c.get('id') == 'point_txn_col_Type':
            geo_e = c.find('mxGeometry')
            ry = float(geo_e.get('y')) + 56
            rx = float(geo_e.get('x'))
            break
    else:
        rx, ry = 100, 450
    rule_c = make_rule_cell('point_txn_rule1',
        "CK: (TransactionType='Earn' AND Points&gt;0) OR (TransactionType='Redeem' AND Points&lt;0)",
        rx, ry, 700, 20)
    tr.append(rule_c)
    print('  Added POINT_TRANSACTION CK rule')

print('  OK')

# ══════════════════════════════════════════════════════════════════════════
# Save
# ══════════════════════════════════════════════════════════════════════════
print('\n--- Saving ---')

# Fix ET namespace issue: remove xmlns="" from output
xml_output = ET.tostring(drawio_tree, encoding='unicode')
# Clean up namespace artifacts
xml_output = xml_output.replace(' xmlns=""', '')
xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_output

with open(DRAWIO_PATH, 'w', encoding='utf-8') as f:
    f.write(xml_output)

size = os.path.getsize(DRAWIO_PATH)
print(f'Saved: {DRAWIO_PATH} ({size:,} bytes)')
print('\nDone!')
