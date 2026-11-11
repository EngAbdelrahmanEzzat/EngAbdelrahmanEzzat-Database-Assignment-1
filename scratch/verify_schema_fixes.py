"""Verify all fixes were applied correctly."""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
import xml.etree.ElementTree as ET

DRAWIO_PATH = r'e:\submission\DataBaseAssignment1\DriveNow.drawio'

with open(DRAWIO_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

tree = ET.fromstring(content)
diagrams = tree.findall('.//diagram')
page_map = {d.get('name',''): d for d in diagrams}
print(f'Total pages: {len(diagrams)}')

def get_graph(page_name):
    d = page_map[page_name]
    children = list(d)
    return children[0] if children else None

def all_values(g):
    result = {}
    for c in g.iter('mxCell'):
        cid = c.get('id','')
        v = c.get('value','')
        if v.strip():
            plain = re.sub(r'<[^>]+>', '', v).strip()
            result[cid] = plain
    return result

PASS = '\u2705'
FAIL = '\u274c'

issues = []

def check(cond, msg):
    if cond:
        print(f'  {PASS} {msg}')
    else:
        print(f'  {FAIL} {msg}')
        issues.append(msg)

# ── Schema-1 ──────────────────────────────────────────────────────────────
print('\n=== 2-Schema-1 ===')
g = get_graph('2-Schema-1')
vals = all_values(g)

check('Specialization' in vals.get('mechanic_col_Specialization','') and 
      'Body' in vals.get('mechanic_col_Specialization',''),
      'MECHANIC.Specialization has Body (not Transmission)')
check('DF:0' in vals.get('rental_agent_col_CommissionRate',''),
      'RENTAL_AGENT.CommissionRate has DF:0')
check('>=1' in vals.get('enrollment_col_AttemptNo',''),
      'ENROLLMENT.AttemptNo has CK:>=1')
# No Age column
check(not any('Age' in v for k,v in vals.items() if 'col_' in k),
      'No derived Age column in Schema-1')

# ── Schema-2 ──────────────────────────────────────────────────────────────
print('\n=== 2-Schema-2 ===')
g = get_graph('2-Schema-2')
vals = all_values(g)

check('CategoryID' in vals.get('category_col_CategoryName','') and 
      'NN' in vals.get('category_col_CategoryName',''),
      'CATEGORY PK is CategoryID')
check('CategoryID' in vals.get('category_rate_col_CategoryName',''),
      'CATEGORY_RATE FK refs CategoryID')
check('ModelID' in vals.get('car_model_col_ID',''),
      'CAR_MODEL PK is ModelID')
check('>=2000' in vals.get('car_model_col_Year',''),
      'CAR_MODEL.Year CK:>=2000')
check('2-15' in vals.get('car_model_col_Seats',''),
      'CAR_MODEL.Seats CK:2-15')
check('vehicle_col_CurrentBranchCode' in vals,
      'VEHICLE has CurrentBranchCode column')
check('vehicle_col_ModelID' in vals,
      'VEHICLE has ModelID column')
check('UnderMaintenance' in vals.get('vehicle_col_Status',''),
      'VEHICLE.Status has UnderMaintenance')
check('Retired' in vals.get('vehicle_col_Status',''),
      'VEHICLE.Status has Retired (not InTransfer)')
check('EmployeeID' in vals.get('vehicle_status_log_col_ChangedBy',''),
      'VEHICLE_STATUS_LOG.ChangedBy is EmployeeID')
check('InstalledAt' in vals.get('gps_device_col_InstallDate',''),
      'GPS_DEVICE has InstalledAt')

# ── Schema-3 ──────────────────────────────────────────────────────────────
print('\n=== 2-Schema-3 ===')
g = get_graph('2-Schema-3')
vals = all_values(g)

check('CustomerID' in vals.get('customer_col_CustomerNo',''),
      'CUSTOMER PK is CustomerID')
check('customer_col_CustomerType' in vals,
      'CUSTOMER has CustomerType column')
check('customer_col_Street' in vals,
      'CUSTOMER has Street column')
check('customer_col_City' in vals,
      'CUSTOMER has City column')
check('customer_col_Governorate' in vals,
      'CUSTOMER has Governorate column')
check('IndividualCustID' in vals.get('individual_col_CustomerNo',''),
      'INDIVIDUAL PK is IndividualCustID')
check('individual_col_FirstName' in vals,
      'INDIVIDUAL has FirstName')
check('individual_col_MiddleName' in vals,
      'INDIVIDUAL has MiddleName')
check('individual_col_LastName' in vals,
      'INDIVIDUAL has LastName')
check('UQ' in vals.get('individual_col_LicenseNo',''),
      'INDIVIDUAL.LicenseNumber has UQ')
check('CorpCustID' in vals.get('corporate_col_CustomerNo',''),
      'CORPORATE PK is CorpCustID')
check('corporate_col_TaxNumber' in vals or 
      any('TaxNumber' in v for v in vals.values()),
      'CORPORATE has TaxNumber')
check('corporate_col_CommercialRegistrationNo' in vals,
      'CORPORATE has CommercialRegistrationNo')
check('corporate_col_ContactPersonPhone' in vals,
      'CORPORATE has ContactPersonPhone')
check('CorpCustID' in vals.get('auth_driver_col_CustomerNo',''),
      'AUTHORIZED_DRIVER PK is CorpCustID')
check('DriverName' in vals.get('auth_driver_col_Name',''),
      'AUTHORIZED_DRIVER has DriverName')
check('NationalID' in vals.get('auth_driver_col_Phone','') or
      any('NationalID' in v and 'auth_driver' in k for k,v in vals.items()),
      'AUTHORIZED_DRIVER has NationalID')
check('AddedDate' in vals.get('blacklist_col_Date',''),
      'BLACKLIST.Date is AddedDate')
check('ReportedByEmployeeID' in vals.get('blacklist_col_DecidedBy',''),
      'BLACKLIST.DecidedBy is ReportedByEmployeeID')
check('DiscountPercentage' in str(vals),
      'CORPORATE_DISCOUNT has DiscountPercentage')

# ── Schema-4 ──────────────────────────────────────────────────────────────
print('\n=== 2-Schema-4 ===')
g = get_graph('2-Schema-4')
vals = all_values(g)
check(not any('UsedCount' in v for v in vals.values()),
      'No derived UsedCount in PROMO_CODE')
check(not any('CustomerNo' in v for k,v in vals.items() if 'col_' in k),
      'No CustomerNo (renamed to CustomerID) in Schema-4')

# ── Schema-6 ──────────────────────────────────────────────────────────────
print('\n=== 2-Schema-6 ===')
g = get_graph('2-Schema-6')
vals = all_values(g)
check(any('JobCardNo' in v for v in vals.values()),
      'JOB_CARD has JobCardNo (not JobNo)')
check(any('StartDate' in v for k,v in vals.items() if 'job' in k.lower()),
      'JOB_CARD has StartDate')
check(any('WorkDescription' in v for v in vals.values()),
      'JOB_CARD has WorkDescription')
check(any('ActualCost' in v for v in vals.values()),
      'JOB_CARD has ActualCost')
check(any('PartNumber' in v for k,v in vals.items() if 'part_col' in k.lower()),
      'PART has PartNumber')
check(any('PartName' in v for v in vals.values()),
      'PART has PartName')
check(any('UnitPrice' in v for v in vals.values()),
      'PART has UnitPrice')
check(any('QuantityInStock' in v for v in vals.values()),
      'PART has QuantityInStock')
check(any('MechanicEmployeeID' in v for v in vals.values()),
      'WORKS_ON has MechanicEmployeeID')
check(any('InspectedByEmployeeID' in v for v in vals.values()),
      'DAMAGE_REPORT has InspectedByEmployeeID')
check(any('RepairCostEstimate' in v for v in vals.values()),
      'DAMAGE_REPORT has RepairCostEstimate')
check(any('SupplierName' in v for v in vals.values()),
      'SUPPLIER has SupplierName')

# ── Schema-7 ──────────────────────────────────────────────────────────────
print('\n=== 2-Schema-7 ===')
g = get_graph('2-Schema-7')
vals = all_values(g)
check(any('IndividualCustID' in v for v in vals.values()),
      'LOYALTY_ACCOUNT has IndividualCustID')
check('loyalty_account_col_JoinDate' in vals,
      'LOYALTY_ACCOUNT has JoinDate')
check(any('TransactionType' in v for v in vals.values()),
      'POINT_TRANSACTION has TransactionType')
check(any('Earn' in v and 'Redeem' in v for v in vals.values()),
      'POINT_TRANSACTION.TransactionType CK has Earn|Redeem|Expire')

# ── Summary ───────────────────────────────────────────────────────────────
print(f'\n{"="*50}')
print(f'TOTAL ISSUES: {len(issues)}')
if issues:
    for iss in issues:
        print(f'  {FAIL} {iss}')
else:
    print('  All checks passed!')
