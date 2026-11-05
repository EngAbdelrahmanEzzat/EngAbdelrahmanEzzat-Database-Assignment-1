# DriveNow - Database Assignment 1 (ERD - Chen Notation)

**الاسم:** عبدالرحمن عزت فتوح  
**Group / ID:** Group 2  

---

## 📌 نبذة عن المشروع
تم تصميم نموذج الكيانات والعلاقات (ERD) بنظام **Chen Notation** لمنظومة تأجير السيارات **DriveNow**، ومقسّم على **7 صفحات** داخل ملف `DriveNow.drawio` وفقاً لقواعد ونطاق الواجب مع مراعاة حد أقصى ~10 كيانات في كل صفحة وتجنب تكرار الكيانات والعلاقات.

---

## 🎨 قواعد وأشكال الرسم المتبعة (Chen Notation في draw.io)
1. **الكيانات (Entities):**
   - **Strong Entity:** مستطيل أزرق صلب (`shape=rectangle`).
   - **Weak Entity:** مستطيل مزدوج الإطار أصلي (`shape=ext;double=1;`).
   - **Dashed Entity:** مستطيل بخط منقط بدون خصائص للإشارة إلى كيان تم تعريفه في صفحة أخرى (`dashed=1`).
2. **العلاقات (Relationships):**
   - **Regular Relationship:** معيّن أخضر صلب (`shape=rhombus;perimeter=rhombusPerimeter;`).
   - **Identifying Relationship:** معيّن مزدوج الإطار أصلي (`shape=rhombus;double=1;perimeter=rhombusPerimeter;`).
   - **Recursive Relationship:** علاقة دائرية مع تحديد أسماء الأدوار (Role Names) على الخطوط.
   - **ISA Specialization:** مثلث يحدد نوع التصنيف (Disjoint / Overlapping).
3. **الخصائص (Attributes):**
   - **Normal Attribute:** بيضاوي أصفر (`ellipse`).
   - **Primary Key (PK):** نص تحته خط متصل صلب (`<u>Key</u>`).
   - **Partial Key (Discriminator):** نص تحته خط منقّط واضح ومميز (`border-bottom: 2px dashed #000;`).
   - **Candidate Key (CK / Unique):** تمييزه بعلامة `(CK)` مثل `PlateNumber`, `NationalID`, `Email`.
   - **Multivalued Attribute:** بيضاوي مزدوج الإطار أصلي (`shape=doubleEllipse;`).
   - **Derived Attribute:** بيضاوي بإطار منقط (`dashed=1`).
   - **Composite Attribute:** بيضاوي رئيسي يتفرع منه الخصائص الفرعية.
4. **المشاركة والتعددية (Participation & Cardinality):**
   - **Total Participation:** خط سميك صلب (`strokeWidth=3`).
   - **Partial Participation:** خط عادي (`strokeWidth=1`).
   - **Cardinality:** توضيح النسب (`1`, `N`, `M`) بجوار أطراف العلاقة.

---

## 📑 فهرس الصفحات داخل `DriveNow.drawio`

| # | اسم الصفحة | الكيانات الحقيقية (Real) | الكيانات المرجعية (Dashed) | إجمالي الكيانات |
|---|---|---|---|:---:|
| 1 | `1-ERD-1-Staff` | `BRANCH`, `EMPLOYEE`, `RENTAL_AGENT`, `MECHANIC`, `COURSE`, `ENROLLMENT` (Weak) | لا يوجد | 6 |
| 2 | `1-ERD-2-Fleet` | `CATEGORY`, `CATEGORY_RATE` (Weak), `CAR_MODEL`, `VEHICLE`, `VEHICLE_STATUS_LOG` (Weak), `GPS_DEVICE`, `VEHICLE_TRANSFER` (Weak) | `BRANCH`, `EMPLOYEE` | 9 |
| 3 | `1-ERD-3-Customers` | `CUSTOMER`, `INDIVIDUAL`, `CORPORATE`, `AUTHORIZED_DRIVER` (Weak), `BLACKLIST`, `CORPORATE_DISCOUNT` (Weak) | `EMPLOYEE`, `CATEGORY` | 8 |
| 4 | `1-ERD-4-Rentals` | `RESERVATION`, `RENTAL`, `ADDITIONAL_DRIVER` (Weak), `PROMO_CODE` | `CUSTOMER`, `CATEGORY`, `BRANCH`, `VEHICLE`, `EMPLOYEE`, `AUTHORIZED_DRIVER` | 10 |
| 5 | `1-ERD-5-Extras-Payments` | `EXTRA`, `INSURANCE_PACKAGE`, `PAYMENT`, `FEEDBACK` (Weak), `TRAFFIC_VIOLATION` | `RENTAL` | 6 |
| 6 | `1-ERD-6-Maintenance` | `DAMAGE_REPORT` (Weak), `DAMAGE_PHOTO` (Weak), `JOB_CARD`, `PART`, `SUPPLIER` | `RENTAL`, `VEHICLE`, `EMPLOYEE`, `MECHANIC` | 9 |
| 7 | `1-ERD-7-Loyalty` | `LOYALTY_ACCOUNT`, `POINT_TRANSACTION` (Weak) | `INDIVIDUAL`, `RENTAL` | 4 |

---

## 📝 الافتراضات والتفاصيل الخاصة (Assumptions & Design Decisions)

1. **الكيانات الضعيفة ومفاتيحها الجزئية (Weak Entities & Partial Keys):**
   - `ENROLLMENT`: كيان ضعيف معرّف عبر `EMPLOYEE` و `COURSE` بمفتاح جزئي **`AttemptNo`** (خط منقط).
   - `CATEGORY_RATE`: كيان ضعيف معرّف عبر `CATEGORY` بمفتاح جزئي **`ValidFrom`** (خط منقط).
   - `VEHICLE_STATUS_LOG`: كيان ضعيف معرّف عبر `VEHICLE` بمفتاح جزئي **`LogNo`** (خط منقط).
   - `VEHICLE_TRANSFER`: كيان ضعيف معرّف عبر `VEHICLE` بمفتاح جزئي **`TransferNo`** (خط منقط).
   - `AUTHORIZED_DRIVER`: كيان ضعيف معرّف عبر `CORPORATE` بمفتاح جزئي **`DriverNo`** (خط منقط).
   - `CORPORATE_DISCOUNT`: كيان ضعيف معرّف عبر `CORPORATE`، وبناءً على الافتراض تم تحديد **`StartDate`** كمفتاح جزئي (خط منقط).
   - `ADDITIONAL_DRIVER`: كيان ضعيف معرّف عبر `RENTAL` بمفتاح جزئي **`DriverSeq`** (خط منقط).
   - `FEEDBACK`: نظراً لعدم وجود مفتاح أساسي مستقل في الـ SRS، تم نمذجته كـ **Weak Entity** تابع لـ `RENTAL` عبر علاقة تعريفية **`GIVES_FEEDBACK`** (معيّن مزدوج)، ومفتاحه الجزئي **`FeedbackNo`** (خط منقط).
   - `DAMAGE_REPORT`: كيان ضعيف معرّف عبر `RENTAL` بمفتاح جزئي **`ReportNo`** (خط منقط).
   - `DAMAGE_PHOTO`: كيان ضعيف معرّف عبر `DAMAGE_REPORT` بمفتاح جزئي **`PhotoNo`** (خط منقط).
   - `POINT_TRANSACTION`: كيان ضعيف معرّف عبر `LOYALTY_ACCOUNT` بمفتاح جزئي **`TxnNo`** (خط منقط).

2. **كيان القائمة السوداء (`BLACKLIST`):**
   - لم يحدد الـ SRS مفتاحاً صريحاً لـ `BLACKLIST`، فتم افتراض إضافة **`BlacklistID`** كمفتاح أساسي (`<u>BlacklistID</u>`) لضمان صحة التصميم.

3. **المفاتيح البديلة والمميزة (Candidate Keys - CK):**
   - تم تمييز الخصائص الفريدة (Unique) غير المفتاح الأساسي بعلامة `(CK)` للتوضيح:
     - `PlateNumber (CK)` في `VEHICLE`.
     - `NationalID (CK)` و `Email (CK)` في `EMPLOYEE`.
     - `NationalID (CK)` في `INDIVIDUAL`.
     - `Email (CK)` في `CUSTOMER`.

---

## ✅ تحقيق المتطلبات الإلزامية (Part A Checklist)
- [x] **1:1 Relationship:** متحققة في `FULFILLS`، `INSTALLED_IN`، `HAS_ACCOUNT`، و `GIVES_FEEDBACK`.
- [x] **1:1 Recursive Relationship:** متحققة في `EXTENDS` (تمديد عقد الإيجار مع توضيح أدوار `Original` و `Extension`).
- [x] **1:N Recursive Relationship:** متحققة في `SUPERVISES` (إشراف الموظفين مع توضيح أدوار `Supervisor` و `Subordinate`).
- [x] **1:N Relationships:** موجودة مع تحديد دقيق للمشاركة الكلية (خط سميك) والجزئية (خط عادي).
- [x] **M:N Relationships:** متحققة في `INCLUDES_EXTRA`, `INCLUDES_INSURANCE`, `WORKS_ON`, `USES_PART`, `SUPPLIES`.
- [x] **الكيانات المزدوجة الأصلية:** استخدام `shape=ext;double=1;` للمستطيل المزدوج، و `shape=rhombus;double=1;` للمعيّن المزدوج، و `shape=doubleEllipse;` للبيضاوي المزدوج لضمان ظهورها بشكل مزدوج أصلي وواضح في draw.io.
- [x] **كيانات التاريخ والمعاملات (Historical & Transactional Entities):**
  - `ENROLLMENT` (تاريخ دورات الموظف ونتائجه)
  - `CATEGORY_RATE` (تاريخ أسعار الفئات حسب فترات الصلاحية)
  - `VEHICLE_STATUS_LOG` (سجل تاريخ تغير حالات المركبة)
  - `VEHICLE_TRANSFER` (سجل عمليات نقل المركبات بين الفروع)
  - `POINT_TRANSACTION` (سجل حركات نقاط الولاء)
  - `RENTAL` (عملية الإيجار الفعلية وتفاصيلها)
  - `PAYMENT` (المعاملات المالية)
  - `DAMAGE_REPORT` (تقارير الأضرار)
  - `JOB_CARD` (أوامر الشغل وتاريخ الصيانة)

---
*تم توليد الملفات وتحديثها طبقاً لمواصفات SRS وقواعد Chen Notation.*
