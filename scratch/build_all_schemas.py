import os
from test_schema_builder import SchemaPageBuilder

# ==============================================================================
# SCHEMA PAGE 1: Staff
# ==============================================================================
def build_schema_1():
    p = SchemaPageBuilder("s1", "2-Schema-1", "Part B: Relational Schema 1 (Staff) — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2", width=2800, height=1800)
    
    # 1. BRANCH
    cols_branch = [
        {"name": "BranchCode", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "Name", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "Street", "is_pk": False, "tags": "NN", "width": 100},
        {"name": "City", "is_pk": False, "tags": "NN", "width": 95},
        {"name": "Governorate", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "OpeningTime", "is_pk": False, "tags": "NULL", "width": 110},
        {"name": "ClosingTime", "is_pk": False, "tags": "NULL", "width": 110},
        {"name": "Is24Hours", "is_pk": False, "tags": "NN DF:0", "width": 105},
        {"name": "ManagerID", "is_pk": False, "tags": "NN UQ", "width": 115},
        {"name": "ManagerStartDate", "is_pk": False, "tags": "NN", "width": 130}
    ]
    b_cells = p.add_table("branch", "BRANCH", 100, 150, cols_branch)
    
    # 2. BRANCH_PHONE (multivalued)
    cols_bphone = [
        {"name": "BranchCode", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "Phone", "is_pk": True, "tags": "NN", "width": 120}
    ]
    bp_cells = p.add_table("branch_phone", "BRANCH_PHONE", 100, 320, cols_bphone)
    p.add_fk_arrow(bp_cells["BranchCode"], b_cells["BranchCode"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 3. EMPLOYEE
    cols_emp = [
        {"name": "EmployeeID", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "NationalID", "is_pk": False, "tags": "NN UQ", "width": 115},
        {"name": "FirstName", "is_pk": False, "tags": "NN", "width": 105},
        {"name": "MiddleName", "is_pk": False, "tags": "NULL", "width": 105},
        {"name": "LastName", "is_pk": False, "tags": "NN", "width": 105},
        {"name": "DateOfBirth", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "HireDate", "is_pk": False, "tags": "NN", "width": 105},
        {"name": "Salary", "is_pk": False, "tags": "NN CK:>0", "width": 110},
        {"name": "Email", "is_pk": False, "tags": "NN UQ", "width": 130},
        {"name": "BranchCode", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "SupervisorID", "is_pk": False, "tags": "NULL", "width": 115}
    ]
    e_cells = p.add_table("employee", "EMPLOYEE", 100, 490, cols_emp)
    
    # Arrow from BRANCH.ManagerID -> EMPLOYEE.EmployeeID
    p.add_fk_arrow(b_cells["ManagerID"], e_cells["EmployeeID"], color="#0277bd", exit_pos="bottom", entry_pos="top")
    # Arrow from EMPLOYEE.BranchCode -> BRANCH.BranchCode
    p.add_fk_arrow(e_cells["BranchCode"], b_cells["BranchCode"], color="#2e7d32", exit_pos="top", entry_pos="bottom")
    # Recursive SupervisorID -> EmployeeID
    p.add_fk_arrow(e_cells["SupervisorID"], e_cells["EmployeeID"], color="#6a1b9a", exit_pos="bottom", entry_pos="bottom")
    
    # 4. RENTAL_AGENT (Subtype)
    cols_ra = [
        {"name": "EmployeeID", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "CommissionRate", "is_pk": False, "tags": "NN CK:0-15", "width": 150}
    ]
    ra_cells = p.add_table("rental_agent", "RENTAL_AGENT (Subtype)", 100, 690, cols_ra, is_sub=True)
    p.add_fk_arrow(ra_cells["EmployeeID"], e_cells["EmployeeID"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 5. MECHANIC (Subtype)
    cols_mech = [
        {"name": "EmployeeID", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "Specialization", "is_pk": False, "tags": "NN CK:Engine|Brakes|Electrical|Transmission|Body", "width": 240},
        {"name": "CertificationLevel", "is_pk": False, "tags": "NN CK:1-5", "width": 150}
    ]
    m_cells = p.add_table("mechanic", "MECHANIC (Subtype)", 450, 690, cols_mech, is_sub=True)
    p.add_fk_arrow(m_cells["EmployeeID"], e_cells["EmployeeID"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 6. COURSE
    cols_course = [
        {"name": "CourseCode", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "Title", "is_pk": False, "tags": "NN", "width": 150},
        {"name": "Hours", "is_pk": False, "tags": "NN CK:>0", "width": 110},
        {"name": "IsMandatory", "is_pk": False, "tags": "NN DF:0", "width": 110}
    ]
    c_cells = p.add_table("course", "COURSE", 100, 890, cols_course)
    
    # 7. ENROLLMENT (Weak entity)
    cols_enr = [
        {"name": "EmployeeID", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "CourseCode", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "AttemptNo", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "EnrollDate", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "CompletionDate", "is_pk": False, "tags": "NULL", "width": 125},
        {"name": "Score", "is_pk": False, "tags": "NULL CK:0-100", "width": 120},
        {"name": "Result", "is_pk": False, "tags": "NULL CK:Pass|Fail", "width": 125}
    ]
    enr_cells = p.add_table("enrollment", "ENROLLMENT (Weak)", 700, 890, cols_enr, rules=["CK: CompletionDate IS NULL OR CompletionDate >= EnrollDate"])
    p.add_fk_arrow(enr_cells["EmployeeID"], e_cells["EmployeeID"], color="#0277bd", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(enr_cells["CourseCode"], c_cells["CourseCode"], color="#e65100", exit_pos="left", entry_pos="right")
    
    return p.build_diagram_compressed()


# ==============================================================================
# SCHEMA PAGE 2: Fleet
# ==============================================================================
def build_schema_2():
    p = SchemaPageBuilder("s2", "2-Schema-2", "Part B: Relational Schema 2 (Fleet) — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2", width=2800, height=1800)
    
    # External reference boxes
    ref_branch = p.add_external_ref("ref_branch", "BRANCH.BranchCode", 1500, 150)
    ref_emp = p.add_external_ref("ref_emp", "EMPLOYEE.EmployeeID", 1500, 220)
    
    # 1. CATEGORY
    cols_cat = [
        {"name": "CategoryName", "is_pk": True, "tags": "NN", "width": 140},
        {"name": "Name", "is_pk": False, "tags": "NN", "width": 140}
    ]
    cat_cells = p.add_table("category", "CATEGORY", 100, 150, cols_cat)
    
    # 2. CATEGORY_RATE (Weak)
    cols_crate = [
        {"name": "CategoryName", "is_pk": True, "tags": "NN", "width": 140},
        {"name": "ValidFrom", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "ValidTo", "is_pk": False, "tags": "NULL", "width": 120},
        {"name": "DailyRate", "is_pk": False, "tags": "NN CK:>0", "width": 120}
    ]
    crate_cells = p.add_table("category_rate", "CATEGORY_RATE (Weak)", 450, 150, cols_crate, rules=["CK: ValidTo IS NULL OR ValidTo >= ValidFrom"])
    p.add_fk_arrow(crate_cells["CategoryName"], cat_cells["CategoryName"], color="#1565c0", exit_pos="left", entry_pos="right")
    
    # 3. CAR_MODEL
    cols_cm = [
        {"name": "ID", "is_pk": True, "tags": "NN", "width": 90},
        {"name": "CategoryName", "is_pk": False, "tags": "NN", "width": 135},
        {"name": "Manufacturer", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "ModelName", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "Year", "is_pk": False, "tags": "NN", "width": 90},
        {"name": "Seats", "is_pk": False, "tags": "NN CK:>0", "width": 105},
        {"name": "TransmissionType", "is_pk": False, "tags": "NN CK:Manual|Automatic", "width": 170},
        {"name": "FuelType", "is_pk": False, "tags": "NN CK:Petrol|Diesel|Electric|Hybrid", "width": 180}
    ]
    cm_cells = p.add_table("car_model", "CAR_MODEL", 100, 330, cols_cm)
    p.add_fk_arrow(cm_cells["CategoryName"], cat_cells["CategoryName"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 4. VEHICLE
    cols_veh = [
        {"name": "VIN", "is_pk": True, "tags": "NN", "width": 130},
        {"name": "PlateNumber", "is_pk": False, "tags": "NN UQ", "width": 120},
        {"name": "Color", "is_pk": False, "tags": "NN", "width": 100},
        {"name": "OdometerReading", "is_pk": False, "tags": "NN CK:>=0", "width": 140},
        {"name": "PurchaseDate", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "PurchasePrice", "is_pk": False, "tags": "NN CK:>0", "width": 130},
        {"name": "Status", "is_pk": False, "tags": "NN DF:'Available' CK:Available|Rented|Maintenance|InTransfer", "width": 260},
        {"name": "HomeBranchCode", "is_pk": False, "tags": "NN", "width": 140}
    ]
    veh_cells = p.add_table("vehicle", "VEHICLE", 100, 520, cols_veh)
    p.add_fk_arrow(veh_cells["HomeBranchCode"], ref_branch, color="#2e7d32", exit_pos="right", entry_pos="left")
    
    # 5. GPS_DEVICE
    cols_gps = [
        {"name": "SerialNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "Manufacturer", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "SimCardNumber", "is_pk": False, "tags": "NN UQ", "width": 130},
        {"name": "InstalledInVIN", "is_pk": False, "tags": "NULL UQ", "width": 130},
        {"name": "InstallDate", "is_pk": False, "tags": "NULL", "width": 110}
    ]
    gps_cells = p.add_table("gps_device", "GPS_DEVICE", 100, 710, cols_gps)
    p.add_fk_arrow(gps_cells["InstalledInVIN"], veh_cells["VIN"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 6. VEHICLE_STATUS_LOG (Weak)
    cols_vlog = [
        {"name": "VIN", "is_pk": True, "tags": "NN", "width": 130},
        {"name": "LogNo", "is_pk": True, "tags": "NN", "width": 95},
        {"name": "OldStatus", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "NewStatus", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "ChangedAt", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "ChangedBy", "is_pk": False, "tags": "NN", "width": 115}
    ]
    vlog_cells = p.add_table("vehicle_status_log", "VEHICLE_STATUS_LOG (Weak)", 800, 710, cols_vlog)
    p.add_fk_arrow(vlog_cells["VIN"], veh_cells["VIN"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(vlog_cells["ChangedBy"], ref_emp, color="#e65100", exit_pos="right", entry_pos="left")
    
    # 7. VEHICLE_TRANSFER (Weak)
    cols_tr = [
        {"name": "VIN", "is_pk": True, "tags": "NN", "width": 130},
        {"name": "TransferNo", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "TransferDateTime", "is_pk": False, "tags": "NN", "width": 135},
        {"name": "OdometerReading", "is_pk": False, "tags": "NN CK:>=0", "width": 140},
        {"name": "FromBranchCode", "is_pk": False, "tags": "NN", "width": 135},
        {"name": "ToBranchCode", "is_pk": False, "tags": "NN", "width": 135},
        {"name": "DriverEmployeeID", "is_pk": False, "tags": "NN", "width": 140}
    ]
    tr_cells = p.add_table("vehicle_transfer", "VEHICLE_TRANSFER (Weak)", 100, 910, cols_tr, rules=["CK: FromBranchCode <> ToBranchCode"])
    p.add_fk_arrow(tr_cells["VIN"], veh_cells["VIN"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(tr_cells["FromBranchCode"], ref_branch, color="#2e7d32", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(tr_cells["ToBranchCode"], ref_branch, color="#2e7d32", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(tr_cells["DriverEmployeeID"], ref_emp, color="#e65100", exit_pos="right", entry_pos="left")
    
    return p.build_diagram_compressed()


# ==============================================================================
# SCHEMA PAGE 3: Customers
# ==============================================================================
def build_schema_3():
    p = SchemaPageBuilder("s3", "2-Schema-3", "Part B: Relational Schema 3 (Customers) — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2", width=2800, height=1800)
    
    # External reference boxes
    ref_emp = p.add_external_ref("ref_emp_c", "EMPLOYEE.EmployeeID", 1500, 150)
    ref_cat = p.add_external_ref("ref_cat_c", "CATEGORY.CategoryName", 1500, 220)
    
    # 1. CUSTOMER
    cols_cust = [
        {"name": "CustomerNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "Email", "is_pk": False, "tags": "NN UQ", "width": 140},
        {"name": "Address", "is_pk": False, "tags": "NN", "width": 130},
        {"name": "RegistrationDate", "is_pk": False, "tags": "NN", "width": 135}
    ]
    cust_cells = p.add_table("customer", "CUSTOMER", 100, 150, cols_cust)
    
    # 2. CUSTOMER_PHONE (multivalued)
    cols_cphone = [
        {"name": "CustomerNo", "is_pk": True, "tags": "NN", "width": 125},
        {"name": "Phone", "is_pk": True, "tags": "NN", "width": 125}
    ]
    cp_cells = p.add_table("customer_phone", "CUSTOMER_PHONE (Multivalued)", 700, 150, cols_cphone)
    p.add_fk_arrow(cp_cells["CustomerNo"], cust_cells["CustomerNo"], color="#1565c0", exit_pos="left", entry_pos="right")
    
    # 3. INDIVIDUAL (Subtype)
    cols_ind = [
        {"name": "CustomerNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "FullName", "is_pk": False, "tags": "NN", "width": 130},
        {"name": "DateOfBirth", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "NationalID", "is_pk": False, "tags": "NN UQ", "width": 120},
        {"name": "PassportNo", "is_pk": False, "tags": "NULL UQ", "width": 120},
        {"name": "LicenseNo", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "LicenseIssuingCountry", "is_pk": False, "tags": "NN", "width": 155},
        {"name": "LicenseExpiryDate", "is_pk": False, "tags": "NN", "width": 135}
    ]
    ind_cells = p.add_table("individual", "INDIVIDUAL (Subtype)", 100, 330, cols_ind, is_sub=True)
    p.add_fk_arrow(ind_cells["CustomerNo"], cust_cells["CustomerNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 4. CORPORATE (Subtype)
    cols_corp = [
        {"name": "CustomerNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "CompanyName", "is_pk": False, "tags": "NN", "width": 140},
        {"name": "TaxRegistrationNumber", "is_pk": False, "tags": "NN UQ", "width": 160},
        {"name": "ContactPerson", "is_pk": False, "tags": "NN", "width": 130},
        {"name": "CreditLimit", "is_pk": False, "tags": "NN CK:>=0", "width": 120}
    ]
    corp_cells = p.add_table("corporate", "CORPORATE (Subtype)", 100, 520, cols_corp, is_sub=True)
    p.add_fk_arrow(corp_cells["CustomerNo"], cust_cells["CustomerNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 5. AUTHORIZED_DRIVER (Weak)
    cols_ad = [
        {"name": "CustomerNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "DriverNo", "is_pk": True, "tags": "NN", "width": 100},
        {"name": "Name", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "LicenseNo", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "LicenseExpiry", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "Phone", "is_pk": False, "tags": "NN", "width": 110}
    ]
    ad_cells = p.add_table("auth_driver", "AUTHORIZED_DRIVER (Weak)", 800, 520, cols_ad, rules=["UQ(CustomerNo, LicenseNo)"])
    p.add_fk_arrow(ad_cells["CustomerNo"], corp_cells["CustomerNo"], color="#1565c0", exit_pos="left", entry_pos="right")
    
    # 6. BLACKLIST
    cols_bl = [
        {"name": "BlacklistID", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "CustomerNo", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "Reason", "is_pk": False, "tags": "NN", "width": 150},
        {"name": "Date", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "DecidedBy", "is_pk": False, "tags": "NN", "width": 115}
    ]
    bl_cells = p.add_table("blacklist", "BLACKLIST", 100, 710, cols_bl)
    p.add_fk_arrow(bl_cells["CustomerNo"], cust_cells["CustomerNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(bl_cells["DecidedBy"], ref_emp, color="#e65100", exit_pos="right", entry_pos="left")
    
    # 7. CORPORATE_DISCOUNT (Weak)
    cols_cd = [
        {"name": "CustomerNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "StartDate", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "CategoryName", "is_pk": False, "tags": "NN", "width": 135},
        {"name": "DiscountPct", "is_pk": False, "tags": "NN CK:0-50", "width": 135},
        {"name": "EndDate", "is_pk": False, "tags": "NN", "width": 115}
    ]
    cd_cells = p.add_table("corp_discount", "CORPORATE_DISCOUNT (Weak)", 100, 890, cols_cd, rules=["CK: EndDate >= StartDate"])
    p.add_fk_arrow(cd_cells["CustomerNo"], corp_cells["CustomerNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(cd_cells["CategoryName"], ref_cat, color="#2e7d32", exit_pos="right", entry_pos="left")
    
    return p.build_diagram_compressed()


# ==============================================================================
# SCHEMA PAGE 4: Rentals
# ==============================================================================
def build_schema_4():
    p = SchemaPageBuilder("s4", "2-Schema-4", "Part B: Relational Schema 4 (Rentals) — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2", width=3000, height=2000)
    
    # External reference boxes
    ref_cust = p.add_external_ref("ref_cust_r", "CUSTOMER.CustomerNo", 1600, 150)
    ref_cat = p.add_external_ref("ref_cat_r", "CATEGORY.CategoryName", 1600, 205)
    ref_br = p.add_external_ref("ref_br_r", "BRANCH.BranchCode", 1600, 260)
    ref_veh = p.add_external_ref("ref_veh_r", "VEHICLE.VIN", 1600, 315)
    ref_emp = p.add_external_ref("ref_emp_r", "EMPLOYEE.EmployeeID", 1600, 370)
    ref_ad = p.add_external_ref("ref_ad_r", "AUTHORIZED_DRIVER.(CustomerNo, DriverNo)", 1600, 425, w=230)
    
    # 1. PROMO_CODE
    cols_promo = [
        {"name": "Code", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "DiscountPct", "is_pk": False, "tags": "NN CK:0-100", "width": 135},
        {"name": "ValidFrom", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "ValidTo", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "MaxUses", "is_pk": False, "tags": "NN CK:>0", "width": 115}
    ]
    pr_cells = p.add_table("promo_code", "PROMO_CODE", 100, 150, cols_promo, rules=["CK: ValidTo >= ValidFrom"])
    
    # 2. RESERVATION
    cols_res = [
        {"name": "ReservationNo", "is_pk": True, "tags": "NN", "width": 130},
        {"name": "CustomerNo", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "CategoryName", "is_pk": False, "tags": "NN", "width": 135},
        {"name": "PickupBranchCode", "is_pk": False, "tags": "NN", "width": 140},
        {"name": "ReturnBranchCode", "is_pk": False, "tags": "NN", "width": 140},
        {"name": "PromoCode", "is_pk": False, "tags": "NULL", "width": 115},
        {"name": "MadeDateTime", "is_pk": False, "tags": "NN", "width": 125},
        {"name": "RequestedPickupDateTime", "is_pk": False, "tags": "NN", "width": 170},
        {"name": "RequestedReturnDateTime", "is_pk": False, "tags": "NN", "width": 170},
        {"name": "Status", "is_pk": False, "tags": "NN DF:'Pending' CK:Pending|Confirmed|Cancelled|Completed", "width": 260},
        {"name": "BookingChannel", "is_pk": False, "tags": "NN CK:Web|Mobile|Branch|Phone", "width": 175}
    ]
    res_cells = p.add_table("reservation", "RESERVATION", 100, 330, cols_res, rules=["CK: RequestedReturnDateTime > RequestedPickupDateTime"])
    p.add_fk_arrow(res_cells["CustomerNo"], ref_cust, color="#1565c0", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(res_cells["CategoryName"], ref_cat, color="#2e7d32", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(res_cells["PickupBranchCode"], ref_br, color="#00838f", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(res_cells["ReturnBranchCode"], ref_br, color="#00838f", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(res_cells["PromoCode"], pr_cells["Code"], color="#6a1b9a", exit_pos="top", entry_pos="bottom")
    
    # 3. RENTAL
    cols_rent = [
        {"name": "RentalNo", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "ReservationNo", "is_pk": False, "tags": "NULL UQ", "width": 135},
        {"name": "VIN", "is_pk": False, "tags": "NN", "width": 125},
        {"name": "CustomerNo", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "PickupBranchCode", "is_pk": False, "tags": "NN", "width": 140},
        {"name": "ReturnBranchCode", "is_pk": False, "tags": "NN", "width": 140},
        {"name": "HandedOverBy", "is_pk": False, "tags": "NN", "width": 125},
        {"name": "ReceivedBy", "is_pk": False, "tags": "NULL", "width": 120},
        {"name": "CorpDriverCustNo", "is_pk": False, "tags": "NULL", "width": 140},
        {"name": "CorpDriverNo", "is_pk": False, "tags": "NULL", "width": 120},
        {"name": "PickupDateTime", "is_pk": False, "tags": "NN", "width": 130},
        {"name": "ExpectedReturnDateTime", "is_pk": False, "tags": "NN", "width": 160},
        {"name": "ActualReturnDateTime", "is_pk": False, "tags": "NULL", "width": 150},
        {"name": "PickupOdometer", "is_pk": False, "tags": "NN CK:>=0", "width": 135},
        {"name": "ReturnOdometer", "is_pk": False, "tags": "NULL", "width": 130},
        {"name": "PickupFuelPct", "is_pk": False, "tags": "NN CK:0-100", "width": 130},
        {"name": "ReturnFuelPct", "is_pk": False, "tags": "NULL CK:0-100", "width": 130},
        {"name": "LateFee", "is_pk": False, "tags": "NN DF:0 CK:>=0", "width": 135},
        {"name": "ExtendedFromRentalNo", "is_pk": False, "tags": "NULL UQ", "width": 160}
    ]
    rent_rules = [
        "FK: (CorpDriverCustNo, CorpDriverNo) -> AUTHORIZED_DRIVER(CustomerNo, DriverNo)",
        "CK: ExpectedReturnDateTime > PickupDateTime",
        "CK: ActualReturnDateTime IS NULL OR ActualReturnDateTime >= PickupDateTime",
        "CK: ReturnOdometer IS NULL OR ReturnOdometer >= PickupOdometer"
    ]
    rent_cells = p.add_table("rental", "RENTAL", 100, 560, cols_rent, rules=rent_rules)
    p.add_fk_arrow(rent_cells["ReservationNo"], res_cells["ReservationNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(rent_cells["VIN"], ref_veh, color="#c2185b", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(rent_cells["CustomerNo"], ref_cust, color="#1565c0", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(rent_cells["PickupBranchCode"], ref_br, color="#00838f", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(rent_cells["ReturnBranchCode"], ref_br, color="#00838f", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(rent_cells["HandedOverBy"], ref_emp, color="#e65100", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(rent_cells["ReceivedBy"], ref_emp, color="#e65100", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(rent_cells["CorpDriverCustNo"], ref_ad, color="#4e342e", exit_pos="right", entry_pos="left")
    # Recursive ExtendedFromRentalNo -> RentalNo
    p.add_fk_arrow(rent_cells["ExtendedFromRentalNo"], rent_cells["RentalNo"], color="#6a1b9a", exit_pos="bottom", entry_pos="bottom")
    
    # 4. ADDITIONAL_DRIVER (Weak)
    cols_add = [
        {"name": "RentalNo", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "DriverSeq", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "DailyFee", "is_pk": False, "tags": "NN CK:>=0", "width": 125},
        {"name": "Name", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "LicenseNo", "is_pk": False, "tags": "NN", "width": 115}
    ]
    add_cells = p.add_table("add_driver", "ADDITIONAL_DRIVER (Weak)", 100, 830, cols_add)
    p.add_fk_arrow(add_cells["RentalNo"], rent_cells["RentalNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    return p.build_diagram_compressed()


# ==============================================================================
# SCHEMA PAGE 5: Extras-Payments
# ==============================================================================
def build_schema_5():
    p = SchemaPageBuilder("s5", "2-Schema-5", "Part B: Relational Schema 5 (Extras &amp; Payments) — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2", width=2800, height=1800)
    
    # External reference box
    ref_rent = p.add_external_ref("ref_rent_ep", "RENTAL.RentalNo", 1400, 150)
    
    # 1. EXTRA
    cols_ex = [
        {"name": "ExtraCode", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "Name", "is_pk": False, "tags": "NN", "width": 130},
        {"name": "DailyCharge", "is_pk": False, "tags": "NN CK:>0", "width": 125}
    ]
    ex_cells = p.add_table("extra", "EXTRA", 100, 150, cols_ex)
    
    # 2. INSURANCE_PACKAGE
    cols_ins = [
        {"name": "PackageCode", "is_pk": True, "tags": "NN", "width": 125},
        {"name": "Name", "is_pk": False, "tags": "NN", "width": 130},
        {"name": "DailyPrice", "is_pk": False, "tags": "NN CK:>0", "width": 120},
        {"name": "MaxCoverage", "is_pk": False, "tags": "NN CK:>0", "width": 125},
        {"name": "Deductible", "is_pk": False, "tags": "NN CK:>=0", "width": 125}
    ]
    ins_cells = p.add_table("insurance_pkg", "INSURANCE_PACKAGE", 600, 150, cols_ins)
    
    # 3. RENTAL_EXTRA (M:N)
    cols_re = [
        {"name": "RentalNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "ExtraCode", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "Quantity", "is_pk": False, "tags": "NN DF:1 CK:>0", "width": 135},
        {"name": "ChargeAtRental", "is_pk": False, "tags": "NN CK:>=0", "width": 135}
    ]
    re_cells = p.add_table("rental_extra", "RENTAL_EXTRA (M:N)", 100, 330, cols_re)
    p.add_fk_arrow(re_cells["RentalNo"], ref_rent, color="#1565c0", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(re_cells["ExtraCode"], ex_cells["ExtraCode"], color="#e65100", exit_pos="top", entry_pos="bottom")
    
    # 4. RENTAL_INSURANCE (M:N)
    cols_ri = [
        {"name": "RentalNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "PackageCode", "is_pk": True, "tags": "NN", "width": 125},
        {"name": "PriceCharged", "is_pk": False, "tags": "NN CK:>=0", "width": 130}
    ]
    ri_cells = p.add_table("rental_ins", "RENTAL_INSURANCE (M:N)", 700, 330, cols_ri)
    p.add_fk_arrow(ri_cells["RentalNo"], ref_rent, color="#1565c0", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(ri_cells["PackageCode"], ins_cells["PackageCode"], color="#e65100", exit_pos="top", entry_pos="bottom")
    
    # 5. PAYMENT
    cols_pay = [
        {"name": "PaymentID", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "RentalNo", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "Amount", "is_pk": False, "tags": "NN CK:>0", "width": 115},
        {"name": "PaymentDateTime", "is_pk": False, "tags": "NN", "width": 135},
        {"name": "PaymentType", "is_pk": False, "tags": "NN CK:Deposit|RentalFee|LateFee|DamageCharge|Violation", "width": 240},
        {"name": "Method", "is_pk": False, "tags": "NN CK:Cash|Card|BankTransfer", "width": 180},
        {"name": "TransactionRef", "is_pk": False, "tags": "NULL UQ", "width": 135}
    ]
    pay_cells = p.add_table("payment", "PAYMENT", 100, 520, cols_pay)
    p.add_fk_arrow(pay_cells["RentalNo"], ref_rent, color="#1565c0", exit_pos="right", entry_pos="left")
    
    # 6. FEEDBACK (Weak entity)
    cols_fb = [
        {"name": "RentalNo", "is_pk": True, "tags": "NN UQ", "width": 125},
        {"name": "FeedbackNo", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "Rating", "is_pk": False, "tags": "NN CK:1-5", "width": 115},
        {"name": "Comment", "is_pk": False, "tags": "NULL", "width": 130},
        {"name": "SubmissionDate", "is_pk": False, "tags": "NN", "width": 130}
    ]
    fb_cells = p.add_table("feedback", "FEEDBACK (Weak)", 100, 710, cols_fb)
    p.add_fk_arrow(fb_cells["RentalNo"], ref_rent, color="#1565c0", exit_pos="right", entry_pos="left")
    
    # 7. TRAFFIC_VIOLATION
    cols_tv = [
        {"name": "ViolationNo", "is_pk": True, "tags": "NN", "width": 125},
        {"name": "RentalNo", "is_pk": False, "tags": "NN", "width": 120},
        {"name": "ViolationDateTime", "is_pk": False, "tags": "NN", "width": 140},
        {"name": "Location", "is_pk": False, "tags": "NN", "width": 125},
        {"name": "Type", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "FineAmount", "is_pk": False, "tags": "NN CK:>0", "width": 125}
    ]
    tv_cells = p.add_table("traffic_violation", "TRAFFIC_VIOLATION", 100, 890, cols_tv)
    p.add_fk_arrow(tv_cells["RentalNo"], ref_rent, color="#1565c0", exit_pos="right", entry_pos="left")
    
    return p.build_diagram_compressed()


# ==============================================================================
# SCHEMA PAGE 6: Maintenance
# ==============================================================================
def build_schema_6():
    p = SchemaPageBuilder("s6", "2-Schema-6", "Part B: Relational Schema 6 (Maintenance) — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2", width=3000, height=2000)
    
    # External reference boxes
    ref_rent = p.add_external_ref("ref_rent_m", "RENTAL.RentalNo", 1500, 150)
    ref_veh = p.add_external_ref("ref_veh_m", "VEHICLE.VIN", 1500, 210)
    ref_emp = p.add_external_ref("ref_emp_m", "EMPLOYEE.EmployeeID", 1500, 270)
    ref_mech = p.add_external_ref("ref_mech_m", "MECHANIC.EmployeeID", 1500, 330)
    
    # 1. DAMAGE_REPORT (Weak)
    cols_dr = [
        {"name": "RentalNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "ReportNo", "is_pk": True, "tags": "NN", "width": 105},
        {"name": "ReportedBy", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "Description", "is_pk": False, "tags": "NN", "width": 150},
        {"name": "Severity", "is_pk": False, "tags": "NN CK:Minor|Moderate|Severe", "width": 170},
        {"name": "EstimatedRepairCost", "is_pk": False, "tags": "NN CK:>=0", "width": 160}
    ]
    dr_cells = p.add_table("damage_report", "DAMAGE_REPORT (Weak)", 100, 150, cols_dr)
    p.add_fk_arrow(dr_cells["RentalNo"], ref_rent, color="#1565c0", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(dr_cells["ReportedBy"], ref_emp, color="#e65100", exit_pos="right", entry_pos="left")
    
    # 2. DAMAGE_PHOTO (Weak on Damage Report)
    cols_dp = [
        {"name": "RentalNo", "is_pk": True, "tags": "NN", "width": 120},
        {"name": "ReportNo", "is_pk": True, "tags": "NN", "width": 105},
        {"name": "PhotoNo", "is_pk": True, "tags": "NN", "width": 105},
        {"name": "PhotoURL", "is_pk": False, "tags": "NN", "width": 150}
    ]
    dp_cells = p.add_table("damage_photo", "DAMAGE_PHOTO (Weak)", 100, 330, cols_dp, rules=["FK: (RentalNo, ReportNo) -> DAMAGE_REPORT(RentalNo, ReportNo)"])
    p.add_fk_arrow(dp_cells["RentalNo"], dr_cells["RentalNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(dp_cells["ReportNo"], dr_cells["ReportNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 3. JOB_CARD
    cols_jc = [
        {"name": "JobNo", "is_pk": True, "tags": "NN", "width": 105},
        {"name": "VIN", "is_pk": False, "tags": "NN", "width": 125},
        {"name": "DamageRentalNo", "is_pk": False, "tags": "NULL", "width": 140},
        {"name": "DamageReportNo", "is_pk": False, "tags": "NULL", "width": 140},
        {"name": "DateIn", "is_pk": False, "tags": "NN", "width": 110},
        {"name": "DateOut", "is_pk": False, "tags": "NULL", "width": 110},
        {"name": "WorkType", "is_pk": False, "tags": "NN CK:RoutineService|DamageRepair|Inspection|TireReplacement", "width": 260},
        {"name": "TotalCost", "is_pk": False, "tags": "NN DF:0 CK:>=0", "width": 135}
    ]
    jc_rules = [
        "FK: (DamageRentalNo, DamageReportNo) -> DAMAGE_REPORT(RentalNo, ReportNo)",
        "UQ(DamageRentalNo, DamageReportNo)",
        "CK: DateOut IS NULL OR DateOut >= DateIn"
    ]
    jc_cells = p.add_table("job_card", "JOB_CARD", 100, 520, cols_jc, rules=jc_rules)
    p.add_fk_arrow(jc_cells["VIN"], ref_veh, color="#c2185b", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(jc_cells["DamageRentalNo"], dr_cells["RentalNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(jc_cells["DamageReportNo"], dr_cells["ReportNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 4. PART
    cols_part = [
        {"name": "PartNo", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "Name", "is_pk": False, "tags": "NN", "width": 130},
        {"name": "CurrentUnitCost", "is_pk": False, "tags": "NN CK:>0", "width": 135},
        {"name": "QtyInStock", "is_pk": False, "tags": "NN DF:0 CK:>=0", "width": 140}
    ]
    pt_cells = p.add_table("part", "PART", 100, 710, cols_part)
    
    # 5. SUPPLIER
    cols_sup = [
        {"name": "SupplierID", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "Name", "is_pk": False, "tags": "NN", "width": 130},
        {"name": "Phone", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "Email", "is_pk": False, "tags": "NN UQ", "width": 130}
    ]
    sup_cells = p.add_table("supplier", "SUPPLIER", 700, 710, cols_sup)
    
    # 6. WORKS_ON (M:N)
    cols_wo = [
        {"name": "MechanicID", "is_pk": True, "tags": "NN", "width": 125},
        {"name": "JobNo", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "HoursSpent", "is_pk": False, "tags": "NN CK:>0", "width": 130}
    ]
    wo_cells = p.add_table("works_on", "WORKS_ON (M:N)", 100, 890, cols_wo)
    p.add_fk_arrow(wo_cells["MechanicID"], ref_mech, color="#7b1fa2", exit_pos="right", entry_pos="left")
    p.add_fk_arrow(wo_cells["JobNo"], jc_cells["JobNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    
    # 7. USES_PART (M:N)
    cols_up = [
        {"name": "JobNo", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "PartNo", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "QtyUsed", "is_pk": False, "tags": "NN CK:>0", "width": 120},
        {"name": "UnitCostAtTime", "is_pk": False, "tags": "NN CK:>0", "width": 135}
    ]
    up_cells = p.add_table("uses_part", "USES_PART (M:N)", 600, 890, cols_up)
    p.add_fk_arrow(up_cells["JobNo"], jc_cells["JobNo"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(up_cells["PartNo"], pt_cells["PartNo"], color="#e65100", exit_pos="top", entry_pos="bottom")
    
    # 8. SUPPLIES (M:N)
    cols_sp = [
        {"name": "SupplierID", "is_pk": True, "tags": "NN", "width": 115},
        {"name": "PartNo", "is_pk": True, "tags": "NN", "width": 110},
        {"name": "UnitPrice", "is_pk": False, "tags": "NN CK:>0", "width": 125},
        {"name": "LeadTimeDays", "is_pk": False, "tags": "NN CK:>=0", "width": 135}
    ]
    sp_cells = p.add_table("supplies", "SUPPLIES (M:N)", 1200, 890, cols_sp)
    p.add_fk_arrow(sp_cells["SupplierID"], sup_cells["SupplierID"], color="#00838f", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(sp_cells["PartNo"], pt_cells["PartNo"], color="#e65100", exit_pos="top", entry_pos="bottom")
    
    return p.build_diagram_compressed()


# ==============================================================================
# SCHEMA PAGE 7: Loyalty
# ==============================================================================
def build_schema_7():
    p = SchemaPageBuilder("s7", "2-Schema-7", "Part B: Relational Schema 7 (Loyalty) — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2", width=2400, height=1500)
    
    # External reference boxes
    ref_ind = p.add_external_ref("ref_ind_l", "INDIVIDUAL.CustomerNo", 800, 150)
    ref_rent = p.add_external_ref("ref_rent_l", "RENTAL.RentalNo", 800, 330)
    
    # 1. LOYALTY_ACCOUNT
    cols_la = [
        {"name": "AccountID", "is_pk": True, "tags": "NN", "width": 130},
        {"name": "CustomerNo", "is_pk": False, "tags": "NN UQ", "width": 140}
    ]
    la_cells = p.add_table("loyalty_account", "LOYALTY_ACCOUNT", 100, 150, cols_la)
    p.add_fk_arrow(la_cells["CustomerNo"], ref_ind, color="#1565c0", exit_pos="right", entry_pos="left")
    
    # 2. POINT_TRANSACTION (Weak)
    cols_pt = [
        {"name": "AccountID", "is_pk": True, "tags": "NN", "width": 130},
        {"name": "TxnNo", "is_pk": True, "tags": "NN", "width": 105},
        {"name": "RentalNo", "is_pk": False, "tags": "NULL", "width": 125},
        {"name": "TxnDate", "is_pk": False, "tags": "NN", "width": 115},
        {"name": "Points", "is_pk": False, "tags": "NN CK:<>0", "width": 120},
        {"name": "Type", "is_pk": False, "tags": "NN CK:Earned|Redeemed", "width": 160}
    ]
    pt_cells = p.add_table("point_txn", "POINT_TRANSACTION (Weak)", 100, 330, cols_pt)
    p.add_fk_arrow(pt_cells["AccountID"], la_cells["AccountID"], color="#1565c0", exit_pos="top", entry_pos="bottom")
    p.add_fk_arrow(pt_cells["RentalNo"], ref_rent, color="#2e7d32", exit_pos="right", entry_pos="left")
    
    return p.build_diagram_compressed()

print("Schema generation functions defined successfully")
