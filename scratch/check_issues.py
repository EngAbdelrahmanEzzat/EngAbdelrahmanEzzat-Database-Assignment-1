import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
import xml.etree.ElementTree as ET

decoded_dir = r'e:\submission\DataBaseAssignment1\scratch\decoded'

# Read all decoded pages
pages_xml = {}
for page_num in range(8, 15):
    files = [f for f in os.listdir(decoded_dir) if f.startswith(f'{page_num}_')]
    if not files:
        continue
    fname = os.path.join(decoded_dir, files[0])
    with open(fname, 'r', encoding='utf-8') as f:
        raw = f.read()
    tree = ET.fromstring(raw)
    cells = tree.findall('.//mxCell')
    
    issues = []
    
    # Build cell map
    cell_map = {c.get('id',''): c for c in cells}
    
    page_name = files[0]
    
    # ==== Check for each page ====
    if page_num == 8:  # 2-Schema-1
        # Check CATEGORY removed (not in this page)
        # Check column names match README
        checks = {
            'BRANCH': ['BranchCode', 'Name', 'Street', 'City', 'Governorate', 'OpeningTime', 'ClosingTime', 'Is24Hours', 'ManagerID', 'ManagerStartDate'],
            'BRANCH_PHONE': ['BranchCode', 'Phone'],
            'EMPLOYEE': ['EmployeeID', 'NationalID', 'FirstName', 'MiddleName', 'LastName', 'DateOfBirth', 'HireDate', 'Salary', 'Email', 'BranchCode', 'SupervisorID'],
            'RENTAL_AGENT': ['EmployeeID', 'CommissionRate'],
            'MECHANIC': ['EmployeeID', 'Specialization', 'CertificationLevel'],
            'COURSE': ['CourseCode', 'Title', 'Hours', 'IsMandatory'],
            'ENROLLMENT': ['EmployeeID', 'CourseCode', 'AttemptNo', 'EnrollDate', 'CompletionDate', 'Score', 'Result'],
        }
        # Find actual columns in diagram
        for c in cells:
            v = c.get('value', '')
            cid = c.get('id', '')
            # Detect column cells
            if 'col_' in cid:
                # Check for wrong column names
                pass
        
        # Check for forbidden derived columns (Age should NOT be present)
        for c in cells:
            v = c.get('value', '')
            if 'Age' in v and 'col_' in c.get('id',''):
                issues.append(f'  ISSUE: Derived column Age found in cell {c.get("id")}')
        
        # Check for CustomerType in CUSTOMER? Not in this page
        # Check specific cell IDs and values
        for c in cells:
            cid = c.get('id', '')
            v = c.get('value', '')
            # Check ENROLLMENT has AttemptNo
            if 'enrollment' in cid.lower() and 'attempt' in v.lower():
                pass  # Good
        
        print(f'\nPage 8 (2-Schema-1) issues:')
        
        # List all column cells and their current state
        col_cells = [(c.get('id',''), c.get('value','')) for c in cells if 'col_' in c.get('id','')]
        for cid, v in col_cells:
            # Strip HTML to get plain text
            import re
            plain = re.sub(r'<[^>]+>', '', v)
            print(f'  {cid}: {plain[:80]}')
    
    elif page_num == 9:  # 2-Schema-2
        print(f'\nPage 9 (2-Schema-2) issues:')
        col_cells = [(c.get('id',''), c.get('value','')) for c in cells if 'col_' in c.get('id','')]
        for cid, v in col_cells:
            import re
            plain = re.sub(r'<[^>]+>', '', v)
            print(f'  {cid}: {plain[:80]}')

    elif page_num == 10:  # 2-Schema-3
        print(f'\nPage 10 (2-Schema-3) issues:')
        col_cells = [(c.get('id',''), c.get('value','')) for c in cells if 'col_' in c.get('id','')]
        for cid, v in col_cells:
            import re
            plain = re.sub(r'<[^>]+>', '', v)
            print(f'  {cid}: {plain[:80]}')
    
    elif page_num == 14:  # 2-Schema-7
        print(f'\nPage 14 (2-Schema-7) issues:')
        col_cells = [(c.get('id',''), c.get('value','')) for c in cells if 'col_' in c.get('id','')]
        for cid, v in col_cells:
            import re
            plain = re.sub(r'<[^>]+>', '', v)
            print(f'  {cid}: {plain[:80]}')
