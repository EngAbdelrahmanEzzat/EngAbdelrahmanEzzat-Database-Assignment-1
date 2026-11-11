"""
Build human-style, natural Part C and Part D pages for DriveNow.drawio.
No AI buzzwords, no emojis, exact student phrasing as requested.
"""
import sys
import xml.etree.ElementTree as ET

def build_human_part_c():
    model = ET.Element('mxGraphModel', {
        'dx': '1600', 'dy': '1000', 'grid': '1', 'gridSize': '10',
        'guides': '1', 'tooltips': '1', 'connect': '1', 'arrows': '1',
        'fold': '1', 'page': '1', 'pageScale': '1',
        'pageWidth': '2800', 'pageHeight': '1800',
        'math': '0', 'shadow': '0'
    })
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    
    # Header Banner
    header = ET.SubElement(root, 'mxCell', {
        'id': 'part_c_header',
        'value': 'Part C: Questions, Assumptions &amp; Contradictions — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2',
        'style': 'text;html=1;fontSize=18;fontStyle=1;align=center;verticalAlign=middle;fillColor=#f8f9fa;strokeColor=#b0bec5;strokeWidth=2;rounded=1;shadow=0;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(header, 'mxGeometry', {'x': '100', 'y': '25', 'width': '2600', 'height': '55', 'as': 'geometry'})
    
    # ──────────────────────────────────────────────────────────────────────────
    # 1. Questions Section (Left Table)
    # ──────────────────────────────────────────────────────────────────────────
    q_title = ET.SubElement(root, 'mxCell', {
        'id': 'q_title',
        'value': '<b>1. Questions (الأسئلة)</b>',
        'style': 'text;html=1;fontSize=16;fontStyle=1;align=right;verticalAlign=middle;fontColor=#1565c0;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(q_title, 'mxGeometry', {'x': '100', 'y': '100', 'width': '1260', 'height': '30', 'as': 'geometry'})
    
    col_w_num = 50
    col_w_sec = 110
    col_w_text = 1100
    table_x = 100
    start_y = 140
    row_h = 60
    
    # Header row
    qh_num = ET.SubElement(root, 'mxCell', {
        'id': 'qh_num', 'value': '<b>#</b>',
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e3f2fd;strokeColor=#90caf9;strokeWidth=1.5;fontColor=#0d47a1;fontSize=13;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(qh_num, 'mxGeometry', {'x': str(table_x), 'y': str(start_y), 'width': str(col_w_num), 'height': '38', 'as': 'geometry'})
    
    qh_sec = ET.SubElement(root, 'mxCell', {
        'id': 'qh_sec', 'value': '<b>SRS Section</b>',
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e3f2fd;strokeColor=#90caf9;strokeWidth=1.5;fontColor=#0d47a1;fontSize=13;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(qh_sec, 'mxGeometry', {'x': str(table_x + col_w_num), 'y': str(start_y), 'width': str(col_w_sec), 'height': '38', 'as': 'geometry'})
    
    qh_text = ET.SubElement(root, 'mxCell', {
        'id': 'qh_text', 'value': '<b>السؤال</b>',
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e3f2fd;strokeColor=#90caf9;strokeWidth=1.5;fontColor=#0d47a1;fontSize=13;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(qh_text, 'mxGeometry', {'x': str(table_x + col_w_num + col_w_sec), 'y': str(start_y), 'width': str(col_w_text), 'height': '38', 'as': 'geometry'})
    
    questions = [
        ("1", "7.1", "هل يمكن نقل الموظف من فرع إلى فرع آخر؟ وهل نحتاج للاحتفاظ بتاريخ انتقالاته؟"),
        ("2", "7.1", "عندما يستبدل المدير بمدير آخر، هل يجب الاحتفاظ بتاريخ تولي كل مدير للفرع؟"),
        ("3", "7.2", "هل يمكن للموظف إعادة الكورس أكثر من مرة حتى بعد اجتيازه؟"),
        ("4", "7.3", "إذا كان للسيارة سعر خاص، مثل بعض سيارات Luxury، فهل هذا السعر يتغلب دائمًا على سعر الفئة؟"),
        ("5", "7.6", "هل يمكن إلغاء عملية نقل سيارة بعد تسجيلها؟ وإذا أمكن، هل يجب الاحتفاظ بسجل الإلغاء؟"),
        ("6", "7.7", "إذا كان السائق المعتمد لشركة هو نفسه عميلًا فرديًا، فهل يجب ربط سجليه بنفس الشخص؟"),
        ("7", "7.10", "هل تنتهي صلاحية نقاط الولاء بعد فترة معينة، أم تظل متاحة حتى استخدامها؟"),
        ("8", "7.12", "هل يمكن تمديد الإيجار أكثر من مرة؟ وكيف يتم التعامل مع سلسلة عقود الإيجار المرتبطة؟")
    ]
    
    cur_y = start_y + 38
    for idx, sec, q in questions:
        bg = "#ffffff" if int(idx) % 2 == 1 else "#fcfcfc"
        
        c_n = ET.SubElement(root, 'mxCell', {
            'id': f'q_num_{idx}', 'value': f'{idx}',
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;fontSize=12;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_n, 'mxGeometry', {'x': str(table_x), 'y': str(cur_y), 'width': str(col_w_num), 'height': str(row_h), 'as': 'geometry'})
        
        c_s = ET.SubElement(root, 'mxCell', {
            'id': f'q_sec_{idx}', 'value': f'<b>{sec}</b>',
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;fontSize=12;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_s, 'mxGeometry', {'x': str(table_x + col_w_num), 'y': str(cur_y), 'width': str(col_w_sec), 'height': str(row_h), 'as': 'geometry'})
        
        c_t = ET.SubElement(root, 'mxCell', {
            'id': f'q_text_{idx}', 'value': f'<div dir="rtl" style="text-align:right; font-size:12px; line-height:1.4; padding:0 8px;">{q}</div>',
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=right;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;fontSize=12;spacingRight=10;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_t, 'mxGeometry', {'x': str(table_x + col_w_num + col_w_sec), 'y': str(cur_y), 'width': str(col_w_text), 'height': str(row_h), 'as': 'geometry'})
        
        cur_y += row_h

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Assumptions Section (Right Table)
    # ──────────────────────────────────────────────────────────────────────────
    assump_x = 1440
    a_title = ET.SubElement(root, 'mxCell', {
        'id': 'a_title',
        'value': '<b>2. Assumptions (الافتراضات)</b>',
        'style': 'text;html=1;fontSize=16;fontStyle=1;align=right;verticalAlign=middle;fontColor=#2e7d32;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(a_title, 'mxGeometry', {'x': str(assump_x), 'y': '100', 'width': '1260', 'height': '30', 'as': 'geometry'})
    
    ah_num = ET.SubElement(root, 'mxCell', {
        'id': 'ah_num', 'value': '<b>#</b>',
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e8f5e9;strokeColor=#a5d6a7;strokeWidth=1.5;fontColor=#1b5e20;fontSize=13;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(ah_num, 'mxGeometry', {'x': str(assump_x), 'y': str(start_y), 'width': str(col_w_num), 'height': '38', 'as': 'geometry'})
    
    ah_sec = ET.SubElement(root, 'mxCell', {
        'id': 'ah_sec', 'value': '<b>SRS Section</b>',
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e8f5e9;strokeColor=#a5d6a7;strokeWidth=1.5;fontColor=#1b5e20;fontSize=13;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(ah_sec, 'mxGeometry', {'x': str(assump_x + col_w_num), 'y': str(start_y), 'width': str(col_w_sec), 'height': '38', 'as': 'geometry'})
    
    ah_text = ET.SubElement(root, 'mxCell', {
        'id': 'ah_text', 'value': '<b>الافتراض</b>',
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e8f5e9;strokeColor=#a5d6a7;strokeWidth=1.5;fontColor=#1b5e20;fontSize=13;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(ah_text, 'mxGeometry', {'x': str(assump_x + col_w_num + col_w_sec), 'y': str(start_y), 'width': str(col_w_text), 'height': '38', 'as': 'geometry'})
    
    assumptions = [
        ("1", "7.1", "لكل فرع مدير مسؤول واحد في أي وقت، مع الاحتفاظ بتاريخ تولي المديرين السابقين للفرع."),
        ("2", "7.1", "الموظف ينتمي إلى فرع واحد في الوقت نفسه، ويمكن أن يكون له مشرف مباشر واحد فقط."),
        ("3", "7.2", "كل محاولة تسجيل في كورس تُحفظ كسجل مستقل، ولا يتم استبدال المحاولات السابقة."),
        ("4", "7.3", "لكل سيارة فرع أساسي مسؤول عنها، بينما موقعها الحالي يمكن أن يتغير نتيجة عمليات النقل."),
        ("5", "7.3", "إذا كانت السيارة لها سعر خاص، يتم استخدام السعر الخاص بدلًا من سعر الفئة."),
        ("6", "7.6", "آخر عملية نقل ناجحة تحدد الموقع الحالي للسيارة."),
        ("7", "7.7", "السائق المعتمد للشركة يمكن أن يكون له سجل مستقل كعميل فردي، مع إمكانية الربط بين السجلين."),
        ("8", "7.10", "مستوى الولاء (Silver / Gold / Platinum) يتم تحديده بناءً على رصيد النقاط الحالي، وليس إدخاله يدويًا.")
    ]
    
    cur_y = start_y + 38
    for idx, sec, a in assumptions:
        bg = "#ffffff" if int(idx) % 2 == 1 else "#fcfcfc"
        
        c_n = ET.SubElement(root, 'mxCell', {
            'id': f'a_num_{idx}', 'value': f'{idx}',
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;fontSize=12;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_n, 'mxGeometry', {'x': str(assump_x), 'y': str(cur_y), 'width': str(col_w_num), 'height': str(row_h), 'as': 'geometry'})
        
        c_s = ET.SubElement(root, 'mxCell', {
            'id': f'a_sec_{idx}', 'value': f'<b>{sec}</b>',
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;fontSize=12;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_s, 'mxGeometry', {'x': str(assump_x + col_w_num), 'y': str(cur_y), 'width': str(col_w_sec), 'height': str(row_h), 'as': 'geometry'})
        
        c_t = ET.SubElement(root, 'mxCell', {
            'id': f'a_text_{idx}', 'value': f'<div dir="rtl" style="text-align:right; font-size:12px; line-height:1.4; padding:0 8px;">{a}</div>',
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=right;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;fontSize=12;spacingRight=10;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_t, 'mxGeometry', {'x': str(assump_x + col_w_num + col_w_sec), 'y': str(cur_y), 'width': str(col_w_text), 'height': str(row_h), 'as': 'geometry'})
        
        cur_y += row_h

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Contradictions Section (Bottom Container)
    # ──────────────────────────────────────────────────────────────────────────
    card_y = 690
    card_w = 2600
    card_h = 320
    
    c_box = ET.SubElement(root, 'mxCell', {
        'id': 'contra_box',
        'value': '',
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;fillColor=#fafafa;strokeColor=#b0bec5;strokeWidth=1.5;rounded=1;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(c_box, 'mxGeometry', {'x': '100', 'y': str(card_y), 'width': str(card_w), 'height': str(card_h), 'as': 'geometry'})
    
    c_title = ET.SubElement(root, 'mxCell', {
        'id': 'contra_title',
        'value': '<div dir="rtl" style="text-align:right;"><b>3. Contradictions (التعارضات)</b></div>',
        'style': 'text;html=1;fontSize=16;fontStyle=1;align=right;verticalAlign=middle;fontColor=#c2185b;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(c_title, 'mxGeometry', {'x': '120', 'y': str(card_y + 15), 'width': '2560', 'height': '25', 'as': 'geometry'})
    
    # Contradiction text using exact user words
    contra_body_html = (
        '<div dir="rtl" style="text-align:right; font-size:13px; line-height:1.6; padding:8px 14px; color:#263238;">'
        '<div style="font-weight:bold; font-size:14px; color:#d32f2f; margin-bottom:8px;">التعارض الأول المحتمل:</div>'
        '<div style="margin-bottom:6px;">• <b>Section 7.7:</b> ينص على أن بيانات السائقين المعتمدين للشركات معروفة من خلال الشركة فقط.</div>'
        '<div style="margin-bottom:12px;">• <b>Section 8:</b> يوضح أن السائق المعتمد للشركة يمكن أن يكون عميلًا فرديًا أيضًا.</div>'
        '<div style="font-weight:bold; font-size:13px; color:#37474f; margin-bottom:4px;">سبب التعارض المحتمل:</div>'
        '<div style="margin-bottom:12px;">قد يكون السائق مسجلًا داخل النظام كسائق تابع للشركة، وفي الوقت نفسه مسجلًا كعميل فردي مستقل. يحتاج الأمر إلى توضيح هل يتم إنشاء سجل شخص واحد وربطه بالشركة، أم يتم إنشاء سجلين منفصلين.</div>'
        '<div style="font-size:12px; color:#555; background-color:#f5f5f5; padding:8px 12px; border-radius:4px; border-right:3px solid #78909c;">'
        '<b>ملاحظة:</b> ده تعارض محتمل يحتاج توضيح، وليس تناقضًا مؤكدًا؛ لأن عبارة "معروف من خلال الشركة" قد تشير إلى علاقة التفويض فقط. ولا يوجد في الأجزاء التي راجعتها تعارض صريح آخر يستدعي اختراعه.'
        '</div>'
        '</div>'
    )
    c_body = ET.SubElement(root, 'mxCell', {
        'id': 'contra_body',
        'value': contra_body_html,
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e0e0e0;strokeWidth=1;rounded=1;align=right;verticalAlign=top;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(c_body, 'mxGeometry', {'x': '120', 'y': str(card_y + 50), 'width': '2560', 'height': '250', 'as': 'geometry'})
    
    return model

def build_human_part_d():
    model = ET.Element('mxGraphModel', {
        'dx': '1600', 'dy': '1000', 'grid': '1', 'gridSize': '10',
        'guides': '1', 'tooltips': '1', 'connect': '1', 'arrows': '1',
        'fold': '1', 'page': '1', 'pageScale': '1',
        'pageWidth': '2800', 'pageHeight': '1800',
        'math': '0', 'shadow': '0'
    })
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    
    # Header Banner
    header = ET.SubElement(root, 'mxCell', {
        'id': 'part_d_header',
        'value': 'Part D: Business Rules Beyond Constraints — DriveNow — Name: عبدالرحمن عزت فتوح — Group 2',
        'style': 'text;html=1;fontSize=18;fontStyle=1;align=center;verticalAlign=middle;fillColor=#f8f9fa;strokeColor=#b0bec5;strokeWidth=2;rounded=1;shadow=0;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(header, 'mxGeometry', {'x': '100', 'y': '25', 'width': '2600', 'height': '55', 'as': 'geometry'})
    
    # Subtitle
    sub_title = ET.SubElement(root, 'mxCell', {
        'id': 'd_subtitle',
        'value': '<div dir="rtl" style="text-align:right;"><b>Part D — Business Rules Beyond Constraints (قواعد عمل لا يمكن تنفيذها باستخدام PK و FK و CHECK و UNIQUE وحدها)</b></div>',
        'style': 'text;html=1;fontSize=15;fontStyle=1;align=right;verticalAlign=middle;fontColor=#1565c0;',
        'vertex': '1', 'parent': '1'
    })
    ET.SubElement(sub_title, 'mxGeometry', {'x': '100', 'y': '95', 'width': '2600', 'height': '30', 'as': 'geometry'})
    
    # Table columns
    w_num = 80
    w_sec = 280
    w_rule = 700
    w_why = 770
    w_how = 770
    table_x = 100
    start_y = 135
    header_h = 42
    
    headers = [
        ("dh_num", "<b>#</b>", w_num),
        ("dh_sec", "<b>SRS Section</b>", w_sec),
        ("dh_rule", "<b>Business Rule</b>", w_rule),
        ("dh_why", "<b>Why constraints are not enough</b>", w_why),
        ("dh_how", "<b>How to enforce it</b>", w_how)
    ]
    
    cur_hx = table_x
    for hid, title, w in headers:
        hc = ET.SubElement(root, 'mxCell', {
            'id': hid,
            'value': title,
            'style': 'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#e3f2fd;strokeColor=#90caf9;strokeWidth=1.5;fontColor=#0d47a1;fontSize=13;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(hc, 'mxGeometry', {'x': str(cur_hx), 'y': str(start_y), 'width': str(w), 'height': str(header_h), 'as': 'geometry'})
        cur_hx += w
        
    rules_data = [
        {
            "id": "1",
            "section": "Section 8 — Stakeholder Interview Notes",
            "rule": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'لا يُسمح بنقل السيارة إلى نفس الفرع الموجود فيه بالفعل.'
                '</div>'
            ),
            "why": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'لأن النظام يحتاج إلى معرفة الموقع الحالي للسيارة ومقارنته بالفرع المستهدف، والموقع الحالي يتغير مع عمليات النقل السابقة.'
                '</div>'
            ),
            "how": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'استخدام Trigger أو Stored Procedure للتحقق من موقع السيارة الحالي قبل تسجيل عملية النقل.'
                '</div>'
            ),
            "h": 140
        },
        {
            "id": "2",
            "section": "Section 7.3 — Fleet, Categories, and Pricing",
            "rule": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'يجب تسجيل كل تغيير يحدث في حالة السيارة، مع تحديد الموظف الذي أجرى التغيير وتاريخ ووقت حدوثه.'
                '</div>'
            ),
            "why": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'لأن القيود التقليدية لا تضمن إنشاء سجل تاريخي جديد تلقائيًا عند كل تغيير في حالة السيارة.'
                '</div>'
            ),
            "how": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'استخدام Database Trigger يعمل عند تغيير Status، ويضيف سجلًا جديدًا في جدول VehicleStatusHistory يحتوي على:<br/>'
                '• VehicleID<br/>'
                '• OldStatus<br/>'
                '• NewStatus<br/>'
                '• EmployeeID<br/>'
                '• ChangedAt'
                '</div>'
            ),
            "h": 160
        },
        {
            "id": "3",
            "section": "Section 7.2 — Training",
            "rule": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'عندما يفشل الموظف في أحد الكورسات ويعيده، يجب الاحتفاظ بكل محاولاته السابقة وعدم استبدالها بالمحاولة الجديدة.'
                '</div>'
            ),
            "why": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'لأن القيود التقليدية لا تضمن أن كل إعادة للكورس ستُسجل كمحاولة جديدة، مع الحفاظ على المحاولات السابقة دون تعديل أو حذف.'
                '</div>'
            ),
            "how": (
                '<div dir="rtl" style="text-align:right; padding:8px 12px; font-size:13px; line-height:1.5;">'
                'استخدام Application Logic لإنشاء TrainingAttempt جديد في كل مرة يعيد فيها الموظف الكورس، مع الاحتفاظ بسجلات المحاولات السابقة.'
                '</div>'
            ),
            "h": 140
        }
    ]
    
    cur_y = start_y + header_h
    for r in rules_data:
        rid = r["id"]
        rh = r["h"]
        bg = "#ffffff" if int(rid) % 2 == 1 else "#fcfcfc"
        
        # Num
        c_n = ET.SubElement(root, 'mxCell', {
            'id': f'd_rnum_{rid}',
            'value': f'<div style="font-size:14px; font-weight:bold;">{rid}</div>',
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_n, 'mxGeometry', {'x': str(table_x), 'y': str(cur_y), 'width': str(w_num), 'height': str(rh), 'as': 'geometry'})
        
        # Section
        c_s = ET.SubElement(root, 'mxCell', {
            'id': f'd_rsec_{rid}',
            'value': f'<div style="font-weight:bold; font-size:12px; color:#1a237e;">{r["section"]}</div>',
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_s, 'mxGeometry', {'x': str(table_x + w_num), 'y': str(cur_y), 'width': str(w_sec), 'height': str(rh), 'as': 'geometry'})
        
        # Rule
        c_r = ET.SubElement(root, 'mxCell', {
            'id': f'd_rrule_{rid}',
            'value': r["rule"],
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=right;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;spacingRight=10;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_r, 'mxGeometry', {'x': str(table_x + w_num + w_sec), 'y': str(cur_y), 'width': str(w_rule), 'height': str(rh), 'as': 'geometry'})
        
        # Why
        c_w = ET.SubElement(root, 'mxCell', {
            'id': f'd_rwhy_{rid}',
            'value': r["why"],
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=right;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;spacingRight=10;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_w, 'mxGeometry', {'x': str(table_x + w_num + w_sec + w_rule), 'y': str(cur_y), 'width': str(w_why), 'height': str(rh), 'as': 'geometry'})
        
        # How
        c_h = ET.SubElement(root, 'mxCell', {
            'id': f'd_rhow_{rid}',
            'value': r["how"],
            'style': f'shape=rectangle;whiteSpace=wrap;html=1;align=right;verticalAlign=middle;fillColor={bg};strokeColor=#cfd8dc;strokeWidth=1;spacingRight=10;',
            'vertex': '1', 'parent': '1'
        })
        ET.SubElement(c_h, 'mxGeometry', {'x': str(table_x + w_num + w_sec + w_rule + w_why), 'y': str(cur_y), 'width': str(w_how), 'height': str(rh), 'as': 'geometry'})
        
        cur_y += rh
        
    return model

print("Human-style Part C & D builders ready!")
