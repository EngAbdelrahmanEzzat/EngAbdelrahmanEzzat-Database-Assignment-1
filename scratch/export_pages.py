import subprocess
import os

exe = r"C:\Users\NOUR SOFT\OneDrive\Desktop\draw.io\draw.io.exe"
input_file = r"e:\submission\DataBaseAssignment1\DriveNow.drawio"
exports_dir = r"e:\submission\DataBaseAssignment1\exports"

os.makedirs(exports_dir, exist_ok=True)

# In draw.io v27+, page indices are 1-based (1 to 7)
pages = [
    (1, "1-ERD-1-Staff"),
    (2, "1-ERD-2-Fleet"),
    (3, "1-ERD-3-Customers"),
    (4, "1-ERD-4-Rentals"),
    (5, "1-ERD-5-Extras-Payments"),
    (6, "1-ERD-6-Maintenance"),
    (7, "1-ERD-7-Loyalty")
]

print("Starting export of all 7 pages with 1-based indexing...")

for page_num, name in pages:
    out_path = os.path.join(exports_dir, f"{name}.png")
    # Parameters from user:
    # Zoom 100% (scale 1)
    # Border 20
    # Transparent not checked (white background)
    # Grid off
    # Name = page name
    cmd = [
        exe,
        "--export",
        "--format", "png",
        "--page-index", str(page_num),
        "--scale", "1",
        "--border", "20",
        "--output", out_path,
        input_file
    ]
    print(f"Exporting page {page_num}: {name} -> {out_path}")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    print(f"  Returncode: {res.returncode}")
    if res.stdout:
        print(f"  Stdout: {res.stdout.strip()}")
    if res.stderr:
        print(f"  Stderr: {res.stderr.strip()}")

print("\nVerifying exported files in exports folder:")
all_ok = True
for page_num, name in pages:
    out_path = os.path.join(exports_dir, f"{name}.png")
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f"  [OK] {name}.png ({size:,} bytes)")
    else:
        print(f"  [MISSING] {name}.png")
        all_ok = False

if all_ok:
    print("\nALL 7 PAGES EXPORTED SUCCESSFULLY!")
