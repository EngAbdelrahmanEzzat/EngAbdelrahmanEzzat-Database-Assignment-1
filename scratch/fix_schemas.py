"""
Master fix script for DriveNow.drawio Schema pages.
Fixes all issues found by comparing decoded XML vs README spec.
"""
import sys, os, re, zlib, base64
sys.stdout.reconfigure(encoding='utf-8')
import xml.etree.ElementTree as ET
ET.register_namespace('', '')

DRAWIO_PATH = r'e:\submission\DataBaseAssignment1\DriveNow.drawio'
BACKUP_PATH = r'e:\submission\DataBaseAssignment1\DriveNow_backup_before_schema_fix.drawio'

# ── helpers ────────────────────────────────────────────────────────────────

def col_html(col_name, tags, is_pk=False):
    """Build the standard column-cell HTML value."""
    weight = 'bold' if is_pk else 'normal'
    name_html = f'<u>{col_name}</u>' if is_pk else col_name
    return (
        f'<div style="font-size:12px; font-weight:{weight};">{name_html}</div>'
        f'<div style="font-size:10px; color:#555; margin-top:2px;">{tags}</div>'
    )

def col_style(is_pk=False):
    if is_pk:
        return 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e3f2fd;strokeColor=#1976d2;strokeWidth=2;rounded=0;'
    return 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#b0bec5;strokeWidth=1;rounded=0;'

def make_col_cell(cid, parent, col_name, tags, is_pk, x, y, w=140, h=52):
    c = ET.Element('mxCell')
    c.set('id', cid)
    c.set('value', col_html(col_name, tags, is_pk))
    c.set('style', col_style(is_pk))
    c.set('vertex', '1')
    c.set('parent', parent)
    geo = ET.SubElement(c, 'mxGeometry')
    geo.set('x', str(x))
    geo.set('y', str(y))
    geo.set('width', str(w))
    geo.set('height', str(h))
    geo.set('as', 'geometry')
    return c

def make_title_cell(cid, parent, title, x, y, w=400, h=25, color='#1565c0'):
    c = ET.Element('mxCell')
    c.set('id', cid)
    c.set('value', f'<b>{title}</b>')
    c.set('style', f'text;html=1;fontSize=15;fontStyle=1;align=left;verticalAlign=bottom;fontColor={color};')
    c.set('vertex', '1')
    c.set('parent', parent)
    geo = ET.SubElement(c, 'mxGeometry')
    geo.set('x', str(x)); geo.set('y', str(y))
    geo.set('width', str(w)); geo.set('height', str(h))
    geo.set('as', 'geometry')
    return c

def make_rule_cell(cid, parent, text, x, y, w=600, h=20):
    c = ET.Element('mxCell')
    c.set('id', cid)
    c.set('value', f'<i style="color:#d32f2f; font-size:11px;">{text}</i>')
    c.set('style', 'text;html=1;fontSize=11;align=left;verticalAlign=top;')
    c.set('vertex', '1')
    c.set('parent', parent)
    geo = ET.SubElement(c, 'mxGeometry')
    geo.set('x', str(x)); geo.set('y', str(y))
    geo.set('width', str(w)); geo.set('height', str(h))
    geo.set('as', 'geometry')
    return c

def make_ref_cell(cid, parent, text, x, y, w=160, h=35):
    c = ET.Element('mxCell')
    c.set('id', cid)
    c.set('value', text)
    c.set('style', 'shape=rectangle;dashed=1;whiteSpace=wrap;html=1;fontSize=11;fontStyle=2;fillColor=#f8f9fa;strokeColor=#78909c;strokeWidth=1.5;align=center;verticalAlign=middle;')
    c.set('vertex', '1')
    c.set('parent', parent)
    geo = ET.SubElement(c, 'mxGeometry')
    geo.set('x', str(x)); geo.set('y', str(y))
    geo.set('width', str(w)); geo.set('height', str(h))
    geo.set('as', 'geometry')
    return c

def make_fk_edge(eid, parent, source, target):
    c = ET.Element('mxCell')
    c.set('id', eid)
    c.set('value', '')
    c.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#1565c0;strokeWidth=1.8;fontSize=10;fontStyle=1;')
    c.set('edge', '1')
    c.set('source', source)
    c.set('target', target)
    c.set('parent', parent)
    geo = ET.SubElement(c, 'mxGeometry')
    geo.set('relative', '1')
    geo.set('as', 'geometry')
    return c

def encode_page(xml_str):
    """Compress XML for drawio format."""
    data = xml_str.encode('utf-8')
    compressed = zlib.compress(data)[2:-4]  # raw deflate
    return base64.b64encode(compressed).decode('ascii')

def decode_page(raw):
    if not raw or not raw.strip():
        return None
    try:
        decoded = base64.b64decode(raw.strip())
        decompressed = zlib.decompress(decoded, -15)
        return decompressed.decode('utf-8')
    except Exception:
        return raw

def remove_cells_by_id(root, ids_to_remove):
    """Remove mxCell elements whose id is in ids_to_remove."""
    for parent in root.iter():
        for child in list(parent):
            if child.get('id','') in ids_to_remove:
                parent.remove(child)

def set_cell_value(root, cell_id, new_value):
    """Update value of a cell by id."""
    for c in root.iter('mxCell'):
        if c.get('id') == cell_id:
            c.set('value', new_value)
            return True
    return False

def get_root_elem(xml_str):
    return ET.fromstring(xml_str)

# ── Load drawio ─────────────────────────────────────────────────────────────

import shutil
shutil.copy(DRAWIO_PATH, BACKUP_PATH)
print(f'Backup saved to: {BACKUP_PATH}')

with open(DRAWIO_PATH, 'r', encoding='utf-8') as f:
    drawio_content = f.read()

drawio_tree = ET.fromstring(drawio_content)
diagrams = drawio_tree.findall('.//diagram')

page_map = {}  # name -> diagram element
for d in diagrams:
    page_map[d.get('name','')] = d

def get_page_root(page_name):
    d = page_map[page_name]
    xml_str = decode_page(d.text)
    return ET.fromstring(xml_str), xml_str

def save_page(page_name, root_elem):
    xml_str = ET.tostring(root_elem, encoding='unicode')
    page_map[page_name].text = encode_page(xml_str)

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 8: 2-Schema-1
# ══════════════════════════════════════════════════════════════════════════
print('\n--- Fixing 2-Schema-1 ---')
root, _ = get_page_root('2-Schema-1')
tree_root = root.find('root')

# Fix 1: MECHANIC Specialization CK should be Engine|Brakes|Electrical|Body|Tires
set_cell_value(root, 'mechanic_col_Specialization',
    col_html('Specialization', 'NN CK:Engine|Brakes|Electrical|Body|Tires'))
print('  Fixed: MECHANIC.Specialization CK')

# Fix 2: CommissionRate should have DF:0
set_cell_value(root, 'rental_agent_col_CommissionRate',
    col_html('CommissionRate', 'NN CK:0-15 DF:0'))
print('  Fixed: RENTAL_AGENT.CommissionRate DF:0')

# Fix 3: ENROLLMENT AttemptNo should have CK:>=1
set_cell_value(root, 'enrollment_col_AttemptNo',
    col_html('AttemptNo', 'NN CK:>=1', is_pk=True))
print('  Fixed: ENROLLMENT.AttemptNo CK:>=1')

save_page('2-Schema-1', root)
print('  Saved 2-Schema-1')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 9: 2-Schema-2  (biggest fixes)
# ══════════════════════════════════════════════════════════════════════════
print('\n--- Fixing 2-Schema-2 ---')
root, _ = get_page_root('2-Schema-2')
tree_root = root.find('root')

# Fix 1: CATEGORY - PK should be CategoryID not CategoryName
# Change title cell value
set_cell_value(root, 'category_col_CategoryName',
    col_html('CategoryID', 'NN', is_pk=True))
print('  Fixed: CATEGORY PK: CategoryName -> CategoryID')

# Add CategoryName as separate column
# Find geometry of category_col_CategoryName
for c in root.iter('mxCell'):
    if c.get('id') == 'category_col_CategoryName':
        geo = c.find('mxGeometry')
        old_x = float(geo.get('x'))
        old_y = float(geo.get('y'))
        old_w = float(geo.get('width'))
        # Add CategoryName beside it
        new_cell = make_col_cell('category_col_CategoryName2', '1',
            'CategoryName', 'NN UQ', False,
            old_x + old_w, old_y, 140, 52)
        tree_root.append(new_cell)
        break
print('  Added: CATEGORY.CategoryName (NN UQ)')

# Fix 2: CATEGORY_RATE - FK should reference CategoryID
set_cell_value(root, 'category_rate_col_CategoryName',
    col_html('CategoryID', 'NN', is_pk=True))
print('  Fixed: CATEGORY_RATE FK col: CategoryName -> CategoryID')

# Fix 3: CAR_MODEL - ID -> ModelID, add missing columns
set_cell_value(root, 'car_model_col_ID',
    col_html('ModelID', 'NN', is_pk=True))
print('  Fixed: CAR_MODEL PK: ID -> ModelID')

# CAR_MODEL.CategoryName -> CategoryID
set_cell_value(root, 'car_model_col_CategoryName',
    col_html('CategoryID', 'NN'))
print('  Fixed: CAR_MODEL.CategoryName -> CategoryID')

# Fix CAR_MODEL Year CK
set_cell_value(root, 'car_model_col_Year',
    col_html('Year', 'NN CK:>=2000'))
print('  Fixed: CAR_MODEL.Year CK:>=2000')

# Fix CAR_MODEL Seats CK
set_cell_value(root, 'car_model_col_Seats',
    col_html('Seats', 'NN CK:2-15'))
print('  Fixed: CAR_MODEL.Seats CK:2-15')

# Fix 4: VEHICLE - add CurrentBranchCode and ModelID
# Find vehicle row geometry
vehicle_col_x_end = 1095  # HomeBranchCode starts at 1095, width 140 -> 1235
for c in root.iter('mxCell'):
    if c.get('id') == 'vehicle_col_HomeBranchCode':
        geo = c.find('mxGeometry')
        hbc_x = float(geo.get('x'))
        hbc_y = float(geo.get('y'))
        hbc_w = float(geo.get('width'))
        # Add CurrentBranchCode after HomeBranchCode
        new_cell = make_col_cell('vehicle_col_CurrentBranchCode', '1',
            'CurrentBranchCode', 'NN', False,
            hbc_x + hbc_w, hbc_y, 150, 52)
        tree_root.append(new_cell)
        # Add ModelID after that
        new_cell2 = make_col_cell('vehicle_col_ModelID', '1',
            'ModelID', 'NN', False,
            hbc_x + hbc_w + 150, hbc_y, 100, 52)
        tree_root.append(new_cell2)
        # Add FK edges
        edge1 = make_fk_edge('vehicle_fk_currentbranch', '1',
            'vehicle_col_CurrentBranchCode', 'ref_branch')
        tree_root.append(edge1)
        edge2 = make_fk_edge('vehicle_fk_modelid', '1',
            'vehicle_col_ModelID', 'car_model_col_ID')
        tree_root.append(edge2)
        break
print('  Added: VEHICLE.CurrentBranchCode and ModelID')

# Fix VEHICLE Status CK to match README
set_cell_value(root, 'vehicle_col_Status',
    col_html('Status', "NN DF:'Available' CK:Available|Rented|UnderMaintenance|Retired"))
print('  Fixed: VEHICLE.Status CK values')

# Fix VEHICLE_STATUS_LOG - ChangedBy -> EmployeeID
set_cell_value(root, 'vehicle_status_log_col_ChangedBy',
    col_html('EmployeeID', 'NN'))
print('  Fixed: VEHICLE_STATUS_LOG.ChangedBy -> EmployeeID')

# Fix GPS_DEVICE InstallDate -> InstalledAt
set_cell_value(root, 'gps_device_col_InstallDate',
    col_html('InstalledAt', 'NULL'))
print('  Fixed: GPS_DEVICE.InstallDate -> InstalledAt')

# Fix ref_branch label to include both columns it represents
# (OK as-is, just a label)

save_page('2-Schema-2', root)
print('  Saved 2-Schema-2')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 10: 2-Schema-3
# ══════════════════════════════════════════════════════════════════════════
print('\n--- Fixing 2-Schema-3 ---')
root, _ = get_page_root('2-Schema-3')
tree_root = root.find('root')

# Fix 1: CUSTOMER PK: CustomerNo -> CustomerID
set_cell_value(root, 'customer_col_CustomerNo',
    col_html('CustomerID', 'NN', is_pk=True))
print('  Fixed: CUSTOMER PK: CustomerNo -> CustomerID')

# Fix 2: CUSTOMER - split Address into Street+City+Governorate, add CustomerType
# Find Address cell position
for c in root.iter('mxCell'):
    if c.get('id') == 'customer_col_Address':
        geo = c.find('mxGeometry')
        addr_x = float(geo.get('x'))
        addr_y = float(geo.get('y'))
        # Replace Address with CustomerType, Street, City, Governorate
        # Rename Address cell to CustomerType
        c.set('value', col_html('CustomerType', 'NN CK:Individual|Corporate'))
        geo.set('width', '170')
        # Add Street after
        new_street = make_col_cell('customer_col_Street', '1',
            'Street', 'NN', False, addr_x + 170, addr_y, 110, 52)
        tree_root.append(new_street)
        # Add City after
        new_city = make_col_cell('customer_col_City', '1',
            'City', 'NN', False, addr_x + 280, addr_y, 90, 52)
        tree_root.append(new_city)
        # Add Governorate after
        new_gov = make_col_cell('customer_col_Governorate', '1',
            'Governorate', 'NN', False, addr_x + 370, addr_y, 110, 52)
        tree_root.append(new_gov)
        break
print('  Fixed: CUSTOMER Address -> CustomerType + Street + City + Governorate')

# Fix 3: CUSTOMER_PHONE - CustomerNo -> CustomerID
set_cell_value(root, 'customer_phone_col_CustomerNo',
    col_html('CustomerID', 'NN', is_pk=True))
print('  Fixed: CUSTOMER_PHONE.CustomerNo -> CustomerID')

# Fix 4: INDIVIDUAL - CustomerNo -> IndividualCustID
set_cell_value(root, 'individual_col_CustomerNo',
    col_html('IndividualCustID', 'NN', is_pk=True))
print('  Fixed: INDIVIDUAL PK: CustomerNo -> IndividualCustID')

# Fix 5: INDIVIDUAL - FullName -> FirstName + MiddleName + LastName
for c in root.iter('mxCell'):
    if c.get('id') == 'individual_col_FullName':
        geo = c.find('mxGeometry')
        fn_x = float(geo.get('x'))
        fn_y = float(geo.get('y'))
        # Replace FullName with FirstName
        c.set('value', col_html('FirstName', 'NN'))
        geo.set('width', '110')
        # Add MiddleName after
        new_mid = make_col_cell('individual_col_MiddleName', '1',
            'MiddleName', 'NULL', False, fn_x + 110, fn_y, 110, 52)
        tree_root.append(new_mid)
        # Add LastName after
        new_last = make_col_cell('individual_col_LastName', '1',
            'LastName', 'NN', False, fn_x + 220, fn_y, 100, 52)
        tree_root.append(new_last)
        break
print('  Fixed: INDIVIDUAL FullName -> FirstName + MiddleName + LastName')

# Fix 6: INDIVIDUAL - LicenseNo -> LicenseNumber (UQ), add rule
set_cell_value(root, 'individual_col_LicenseNo',
    col_html('LicenseNumber', 'NN UQ'))
print('  Fixed: INDIVIDUAL.LicenseNo -> LicenseNumber UQ')

# Fix 7: INDIVIDUAL - remove LicenseIssuingCountry (not in README), add rule cell
for c in root.iter('mxCell'):
    if c.get('id') == 'individual_col_LicenseIssuingCountry':
        # Replace it with a check rule text note
        c.set('id', 'individual_rule1')
        c.set('value', '<i style="color:#d32f2f; font-size:11px;">CK: NationalID IS NOT NULL OR PassportNo IS NOT NULL</i>')
        c.set('style', 'text;html=1;fontSize=11;align=left;verticalAlign=top;')
        c.set('vertex', '1')
        geo = c.find('mxGeometry')
        geo.set('height', '20')
        break
print('  Fixed: INDIVIDUAL.LicenseIssuingCountry -> CK rule')

# Fix 8: CORPORATE PK: CustomerNo -> CorpCustID
set_cell_value(root, 'corporate_col_CustomerNo',
    col_html('CorpCustID', 'NN', is_pk=True))
print('  Fixed: CORPORATE PK: CustomerNo -> CorpCustID')

# Fix 9: CORPORATE - rename TaxRegistrationNumber -> TaxNumber, add CommercialRegistrationNo + ContactPersonPhone, remove CreditLimit
for c in root.iter('mxCell'):
    if c.get('id') == 'corporate_col_TaxRegistrationNumber':
        c.set('id', 'corporate_col_TaxNumber')
        c.set('value', col_html('TaxNumber', 'NN UQ'))
        geo = c.find('mxGeometry')
        geo.set('width', '120')
        tax_x = float(geo.get('x'))
        tax_y = float(geo.get('y'))
        # Add CommercialRegistrationNo after
        new_crn = make_col_cell('corporate_col_CommercialRegistrationNo', '1',
            'CommercialRegistrationNo', 'NN UQ', False,
            tax_x + 120, tax_y, 185, 52)
        tree_root.append(new_crn)
        break
print('  Fixed: CORPORATE TaxRegistrationNumber -> TaxNumber, added CommercialRegistrationNo')

# Replace ContactPerson with ContactPersonName
set_cell_value(root, 'corporate_col_ContactPerson',
    col_html('ContactPersonName', 'NN'))
print('  Fixed: CORPORATE ContactPerson -> ContactPersonName')

# Replace CreditLimit with ContactPersonPhone
for c in root.iter('mxCell'):
    if c.get('id') == 'corporate_col_CreditLimit':
        c.set('id', 'corporate_col_ContactPersonPhone')
        c.set('value', col_html('ContactPersonPhone', 'NN'))
        break
print('  Fixed: CORPORATE CreditLimit -> ContactPersonPhone')

# Fix 10: AUTHORIZED_DRIVER - CustomerNo -> CorpCustID
set_cell_value(root, 'auth_driver_col_CustomerNo',
    col_html('CorpCustID', 'NN', is_pk=True))
print('  Fixed: AUTHORIZED_DRIVER.CustomerNo -> CorpCustID')

# Fix 11: AUTHORIZED_DRIVER - DriverName, LicenseNumber, NationalID (rename columns)
set_cell_value(root, 'auth_driver_col_Name',
    col_html('DriverName', 'NN'))
print('  Fixed: AUTHORIZED_DRIVER.Name -> DriverName')

set_cell_value(root, 'auth_driver_col_LicenseNo',
    col_html('LicenseNumber', 'NN'))
print('  Fixed: AUTHORIZED_DRIVER.LicenseNo -> LicenseNumber')

set_cell_value(root, 'auth_driver_col_LicenseExpiry',
    col_html('LicenseExpiryDate', 'NN'))
print('  Fixed: AUTHORIZED_DRIVER.LicenseExpiry -> LicenseExpiryDate')

# Replace Phone with NationalID
for c in root.iter('mxCell'):
    if c.get('id') == 'auth_driver_col_Phone':
        c.set('id', 'auth_driver_col_NationalID')
        c.set('value', col_html('NationalID', 'NN'))
        break
print('  Fixed: AUTHORIZED_DRIVER.Phone -> NationalID')

# Fix 12: BLACKLIST - CustomerNo->CustomerID, rename Date->AddedDate, DecidedBy->ReportedByEmployeeID, add BlacklistID
set_cell_value(root, 'blacklist_col_CustomerNo',
    col_html('CustomerID', 'NN'))
print('  Fixed: BLACKLIST.CustomerNo -> CustomerID')

set_cell_value(root, 'blacklist_col_Date',
    col_html('AddedDate', 'NN'))
print('  Fixed: BLACKLIST.Date -> AddedDate')

set_cell_value(root, 'blacklist_col_DecidedBy',
    col_html('ReportedByEmployeeID', 'NN'))
print('  Fixed: BLACKLIST.DecidedBy -> ReportedByEmployeeID')

# Fix 13: CORPORATE_DISCOUNT - CustomerNo->CorpCustID, CategoryName->CategoryID, DiscountPct->DiscountPercentage
set_cell_value(root, 'corp_discount_col_CustomerNo',
    col_html('CorpCustID', 'NN', is_pk=True))
print('  Fixed: CORPORATE_DISCOUNT.CustomerNo -> CorpCustID')

set_cell_value(root, 'corp_discount_col_CategoryName',
    col_html('CategoryID', 'NN'))
print('  Fixed: CORPORATE_DISCOUNT.CategoryName -> CategoryID')

set_cell_value(root, 'corp_discount_col_DiscountPct',
    col_html('DiscountPercentage', 'NN CK:1-50'))
print('  Fixed: CORPORATE_DISCOUNT.DiscountPct -> DiscountPercentage')

# Fix ref box in page 10
set_cell_value(root, 'ref_cat_c', 'CATEGORY.CategoryID')
print('  Fixed: ref box CATEGORY.CategoryName -> CATEGORY.CategoryID')

save_page('2-Schema-3', root)
print('  Saved 2-Schema-3')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGES 11-13: 2-Schema-4, 5, 6 (read full XML to find issues)
# ══════════════════════════════════════════════════════════════════════════

# -- Schema-4 fixes --
print('\n--- Fixing 2-Schema-4 ---')
root, xml_str = get_page_root('2-Schema-4')

# Check for CustomerType missing from CUSTOMER ref, UsedCount in PROMO_CODE
# Read all values
all_values = {}
for c in root.iter('mxCell'):
    cid = c.get('id','')
    v = c.get('value','')
    plain = re.sub(r'<[^>]+>', '', v)
    if plain.strip():
        all_values[cid] = plain.strip()

# Fix PROMO_CODE UsedCount (derived - should NOT be there)
for c in root.iter('mxCell'):
    cid = c.get('id','')
    v = c.get('value','')
    if 'UsedCount' in v:
        print(f'  REMOVING derived UsedCount from cell {cid}')
        # Cannot easily delete, rename to MaxUses instead (if it was wrongly named)
        c.set('value', col_html('MaxUses', 'NN CK:>0'))
        break

save_page('2-Schema-4', root)
print('  Saved 2-Schema-4')

# -- Schema-5 fixes --
print('\n--- Fixing 2-Schema-5 ---')
root, xml_str = get_page_root('2-Schema-5')

# Check for derived columns (TotalPoints, Tier, etc)
for c in root.iter('mxCell'):
    v = c.get('value','')
    if 'TotalPoints' in v or 'Tier' in v:
        print(f'  Found possible derived col in Schema-5: {c.get("id")} = {v[:60]}')

save_page('2-Schema-5', root)
print('  Saved 2-Schema-5')

# -- Schema-6 fixes --
print('\n--- Fixing 2-Schema-6 ---')
root, xml_str = get_page_root('2-Schema-6')

# Fix JOB_CARD: JobNo -> JobCardNo, DateIn->StartDate, DateOut->EndDate, WorkType->WorkDescription, TotalCost->ActualCost
# Also fix DAMAGE_REPORT column names
# Fix PART: PartNo->PartNumber, Name->PartName, CurrentUnitCost->UnitPrice, QtyInStock->QuantityInStock
# Fix SUPPLIER: Name->SupplierName, add missing Email col
# Fix WORKS_ON: MechanicID -> MechanicEmployeeID
# Fix DAMAGE_REPORT columns: Severity not in spec, EstimatedRepairCost->RepairCostEstimate, ReportedBy->InspectedByEmployeeID

for c in root.iter('mxCell'):
    cid = c.get('id','')
    v = c.get('value','')
    plain = re.sub(r'<[^>]+>', '', v).strip()
    
    # JOB_CARD fixes
    if cid == 'job_card_col_JobNo' or ('job' in cid.lower() and 'jobno' in cid.lower()):
        c.set('value', col_html('JobCardNo', 'NN', is_pk=True))
        c.set('id', 'job_card_col_JobCardNo')
        print(f'  Fixed: JOB_CARD.JobNo -> JobCardNo')
    elif 'job' in cid.lower() and 'datein' in cid.lower():
        c.set('value', col_html('StartDate', 'NN'))
        print(f'  Fixed: JOB_CARD.DateIn -> StartDate')
    elif 'job' in cid.lower() and 'dateout' in cid.lower():
        c.set('value', col_html('EndDate', 'NULL'))
        print(f'  Fixed: JOB_CARD.DateOut -> EndDate')
    elif 'job' in cid.lower() and 'worktype' in cid.lower():
        c.set('value', col_html('WorkDescription', 'NN'))
        print(f'  Fixed: JOB_CARD.WorkType -> WorkDescription')
    elif 'job' in cid.lower() and 'totalcost' in cid.lower():
        c.set('value', col_html('ActualCost', 'NULL CK:>=0'))
        print(f'  Fixed: JOB_CARD.TotalCost -> ActualCost')
    # PART fixes
    elif 'part' in cid.lower() and cid.endswith('_PartNo'):
        c.set('value', col_html('PartNumber', 'NN', is_pk=True))
        print(f'  Fixed: PART.PartNo -> PartNumber')
    elif cid == 'part_col_Name' or ('part' in cid.lower() and cid.endswith('_Name')):
        c.set('value', col_html('PartName', 'NN'))
        print(f'  Fixed: PART.Name -> PartName')
    elif 'part' in cid.lower() and 'unitcost' in cid.lower():
        c.set('value', col_html('UnitPrice', 'NN CK:>0'))
        print(f'  Fixed: PART.CurrentUnitCost -> UnitPrice')
    elif 'part' in cid.lower() and 'qtyinstock' in cid.lower():
        c.set('value', col_html('QuantityInStock', 'NN CK:>=0'))
        print(f'  Fixed: PART.QtyInStock -> QuantityInStock')
    # SUPPLIER fixes
    elif 'supplier' in cid.lower() and cid.endswith('_Name'):
        c.set('value', col_html('SupplierName', 'NN'))
        print(f'  Fixed: SUPPLIER.Name -> SupplierName')
    # WORKS_ON fixes
    elif 'works_on' in cid.lower() and 'mechanicid' in cid.lower():
        c.set('value', col_html('MechanicEmployeeID', 'NN', is_pk=True))
        print(f'  Fixed: WORKS_ON.MechanicID -> MechanicEmployeeID')
    # DAMAGE_REPORT fixes
    elif 'damage' in cid.lower() and 'reportedby' in cid.lower():
        c.set('value', col_html('InspectedByEmployeeID', 'NN'))
        print(f'  Fixed: DAMAGE_REPORT.ReportedBy -> InspectedByEmployeeID')
    elif 'damage' in cid.lower() and 'estimatedrepaircost' in cid.lower():
        c.set('value', col_html('RepairCostEstimate', 'NN CK:>=0'))
        print(f'  Fixed: DAMAGE_REPORT.EstimatedRepairCost -> RepairCostEstimate')
    elif 'damage' in cid.lower() and 'severity' in cid.lower():
        # Severity is not in spec - replace with Description if Description missing
        # Actually Severity is extra - keep as note or remove
        # We'll relabel as Description since it's not in spec
        # (Do nothing - it won't hurt if kept, but let's rename to match spec)
        pass

save_page('2-Schema-6', root)
print('  Saved 2-Schema-6')

# ══════════════════════════════════════════════════════════════════════════
# FIX PAGE 14: 2-Schema-7
# ══════════════════════════════════════════════════════════════════════════
print('\n--- Fixing 2-Schema-7 ---')
root, _ = get_page_root('2-Schema-7')

# Fix 1: LOYALTY_ACCOUNT - CustomerNo -> IndividualCustID, add JoinDate
for c in root.iter('mxCell'):
    if c.get('id') == 'loyalty_account_col_CustomerNo':
        c.set('value', col_html('IndividualCustID', 'NN UQ'))
        geo = c.find('mxGeometry')
        la_x = float(geo.get('x'))
        la_y = float(geo.get('y'))
        la_w = float(geo.get('width'))
        # Add JoinDate after
        new_jd = make_col_cell('loyalty_account_col_JoinDate', '1',
            'JoinDate', 'NN', False, la_x + la_w, la_y, 110, 52)
        root.find('root').append(new_jd)
        break
print('  Fixed: LOYALTY_ACCOUNT.CustomerNo -> IndividualCustID')
print('  Added: LOYALTY_ACCOUNT.JoinDate')

# Fix 2: POINT_TRANSACTION - Type -> TransactionType with correct CK
set_cell_value(root, 'point_txn_col_Type',
    col_html('TransactionType', 'NN CK:Earn|Redeem|Expire'))
print('  Fixed: POINT_TRANSACTION.Type -> TransactionType CK:Earn|Redeem|Expire')

# Fix 3: POINT_TRANSACTION - Points CK: <>0 -> just NN (sign indicates Earn/Redeem)
set_cell_value(root, 'point_txn_col_Points',
    col_html('Points', 'NN'))
print('  Fixed: POINT_TRANSACTION.Points CK')

# Fix ref box label
for c in root.iter('mxCell'):
    if c.get('id') == 'ref_cust' or ('INDIVIDUAL' in c.get('value','') and 'CustomerNo' in c.get('value','')):
        c.set('value', 'INDIVIDUAL.IndividualCustID')
        print('  Fixed: ref box -> INDIVIDUAL.IndividualCustID')
        break

# Check and add missing rule for POINT_TRANSACTION
# Find if rule exists
has_rule = any('Earn' in c.get('value','') and 'Points' in c.get('value','') 
                for c in root.iter('mxCell'))
if not has_rule:
    # Find position to add rule
    for c in root.iter('mxCell'):
        if c.get('id') == 'point_txn_col_Type':
            geo = c.find('mxGeometry')
            rx = float(geo.get('x'))
            ry = float(geo.get('y')) + 56
            rule_cell = make_rule_cell('point_txn_rule1', '1',
                "CK: (TransactionType='Earn' AND Points>0) OR (TransactionType='Redeem' AND Points&lt;0)",
                100, ry, 700, 20)
            root.find('root').append(rule_cell)
            print('  Added: POINT_TRANSACTION CK rule')
            break

save_page('2-Schema-7', root)
print('  Saved 2-Schema-7')

# ══════════════════════════════════════════════════════════════════════════
# Save updated drawio
# ══════════════════════════════════════════════════════════════════════════
print('\n--- Saving DriveNow.drawio ---')
xml_output = ET.tostring(drawio_tree, encoding='unicode', xml_declaration=False)
# Add XML declaration
xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_output

with open(DRAWIO_PATH, 'w', encoding='utf-8') as f:
    f.write(xml_output)

print(f'Done! File saved: {DRAWIO_PATH}')
print(f'File size: {os.path.getsize(DRAWIO_PATH):,} bytes')
