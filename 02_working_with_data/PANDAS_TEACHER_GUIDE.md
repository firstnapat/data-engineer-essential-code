# 02 — pandas · คู่มือผู้สอน (Teacher Guide) 🐼

> เอกสารนี้สำหรับ **ผู้สอน** เท่านั้น — มีบทพูด (Speaker Notes), ลำดับการสอน,
> และจุดที่นักเรียนมักพลาด ใช้คู่กับ notebook `01_pandas/01_pandas.ipynb`
> และ assignment ใน `02_assignment/` (ซึ่งรันบนข้อมูล QuickMart `datasets/new-raw/`)
>
> ⚠️ **อย่า merge ไฟล์นี้เข้า `main`** — เก็บไว้บน branch `teacher-guide` เท่านั้น

---

## ภาพรวมการสอน

| รายการ | รายละเอียด |
|--------|-----------|
| กลุ่มเป้าหมาย | junior ที่ผ่าน Python basics แล้ว เริ่มจับข้อมูลจริง |
| เวลารวม | 2.5–3 ชม. (notebook) + 1–1.5 ชม. (assignment) |
| รูปแบบ | รัน notebook ทีละ cell → อธิบาย → ให้ทำ assignment บนข้อมูลจริง |

**Mental model ที่ต้องปักให้แน่นตั้งแต่ต้น:**
> DataFrame = **ตาราง Excel ที่สั่งงานด้วยโค้ดได้** · Series = **1 คอลัมน์** ของตารางนั้น
> ทุกอย่างใน pandas คือการเล่นกับ "ตาราง" กับ "คอลัมน์" — ให้นักเรียนนึกภาพ Excel ตลอดเวลา

### Pacing ที่แนะนำ
| Section | เวลา | โหมด |
|---------|------|------|
| 1 Intro / 2 Series / 3 DataFrame | 30 นาที | สาธิต — ปู mental model |
| 4 Read/Write | 15 นาที | สาธิต `read_csv` |
| 5 Select (loc/iloc) | 30 นาที | **ลงมือ — จุดสับสนสุด** |
| 6 Statistics | 15 นาที | สาธิต `describe`, `groupby` |
| 7 Manipulation | 25 นาที | ลงมือ |
| 8 Cleaning | 30 นาที | **ลงมือ — หัวใจงาน DE** |
| 9 Merge/Join | 30 นาที | ลงมือ (ยากสุด) |

> 💡 ถ้าเวลาจำกัด: บีบ section 2 ได้ แต่ **ห้ามตัด** 5, 8, 9 เพราะเป็นแกนของงานจริง

---

## Section 5 — Accessing & Selecting (`loc` vs `iloc`) ⭐

### 🎤 Speaker Notes (ผู้สอน)
> เอาล่ะครับ section นี้คือจุดที่นักเรียนสับสนกันเยอะที่สุด — ผมจะสอนช้า ๆ
>
> pandas มี 2 วิธีหลักในการ "ชี้" ไปที่ข้อมูล
>
> *(เว้นจังหวะ)*
>
> `loc` ชี้ด้วย **ชื่อ (label)** — เหมือนเรียกชื่อคน
>
> `iloc` ชี้ด้วย **ตำแหน่ง (index ตัวเลข)** — เหมือนเรียกลำดับที่ยืน
>
> จำง่าย ๆ ครับ: **i**loc = **i**nteger position
>
> ถ้าจำสองตัวนี้แยกกันได้ ที่เหลือสบายเลย

### นักเรียนมักพลาด
- ใช้ `df[0]` หวังได้แถวแรก → พัง/ได้ column ชื่อ `0` แทน (ต้อง `df.iloc[0]`)
- `loc` กับ slice **รวมปลายทาง** (`df.loc[0:2]` ได้ 3 แถว) แต่ `iloc[0:2]` ได้ 2 แถว ตามปกติ Python
- สับสน `df["col"]` (เลือก column) กับ `df.loc[row]` (เลือก row)

### Teaching tip
ให้เทียบกับ Excel: `loc` = อ้างด้วยหัวตาราง, `iloc` = อ้างด้วยพิกัด R1C1

---

## Section 8 — Data Cleaning ⭐ (หัวใจงาน DE)

### 🎤 Speaker Notes (ผู้สอน)
> ทุกคนครับ ในงานจริง 80% ของเวลา Data Engineer หมดไปกับ "ทำความสะอาดข้อมูล"
>
> ข้อมูลจาก source ไม่เคยสะอาดครับ — มีค่าซ้ำ มีช่องว่าง มี type ผิด
>
> *(เว้นจังหวะ)*
>
> เดี๋ยวพอไปทำ assignment ทุกคนจะเจอข้อมูล QuickMart ที่ผม "ทำให้สกปรกตั้งใจ"
>
> มี email ว่าง, ราคาติดลบ, status พิมพ์เล็กพิมพ์ใหญ่ปนกัน, แถวซ้ำ
>
> section นี้คืออาวุธที่เราจะใช้จัดการมัน

### เครื่องมือหลักที่ต้องสอน
| งาน | คำสั่ง |
|-----|--------|
| หาค่า null | `df.isnull().sum()` |
| ลบ/เติม null | `dropna()` / `fillna(0)` |
| ลบแถวซ้ำ | `drop_duplicates(subset=["id"])` |
| แก้ type | `astype()` / `pd.to_numeric(errors="coerce")` |
| ปรับ string | `.str.strip()`, `.str.lower()`, `.str.title()` |
| กรองแถว | `df[df["price"] > 0]` |

### ⚠️ จุดที่ต้องเตือน — `SettingWithCopyWarning`
นักเรียนจะเจอ warning นี้แน่นอน ต้องเตรียมอธิบาย:
```python
# ❌ chained indexing — อาจไม่เปลี่ยนจริง + ขึ้น warning
df[df["price"] > 0]["price"] = 0
# ✅ ใช้ .loc ทีเดียว
df.loc[df["price"] > 0, "price"] = 0
# ✅ ถ้าตั้งใจทำงานบนสำเนา ให้ .copy() ก่อน
clean = df[df["price"] > 0].copy()
```
> สอนกฎง่าย ๆ: "ถ้าจะ **แก้ค่า** ใช้ `.loc[row, col] =` · ถ้าจะ **กรองมาทำต่อ** ใช้ `.copy()`"

---

## Section 9 — Merge, Join & Concatenate ⭐ (ยากสุด)

### 🎤 Speaker Notes (ผู้สอน)
> section สุดท้ายนี้คือเวทมนตร์ของ DE ครับ — เอาหลายตารางมาต่อกัน
>
> นึกภาพ QuickMart นะครับ: ตาราง orders มีแค่ `customer_id`
>
> แต่เราอยากรู้ "ชื่อลูกค้า" ซึ่งอยู่อีกตาราง
>
> *(รอฟังคำตอบ)* เราจะเอามาต่อกันยังไง?
>
> นั่นแหละครับคือ `merge` — ต่อตารางด้วย "key" ที่ตรงกัน

### `how=` ต้องสอนให้เห็นภาพ
| how | ได้อะไร |
|-----|---------|
| `inner` (default) | เฉพาะแถวที่ key ตรงกัน **ทั้งสอง** ตาราง |
| `left` | ทุกแถวของตารางซ้าย (ขวาไม่มี → NaN) |
| `right` / `outer` | เจอน้อยกว่า — สอนผ่าน ๆ ได้ |

### นักเรียนมักพลาด (เยอะที่สุดในบทนี้)
- **key dtype ไม่ตรง** — `customer_id` ฝั่งนึงเป็น int อีกฝั่งเป็น str → merge ได้ 0 แถว!
  (สอนให้เช็ก `df.dtypes` ก่อน merge เสมอ)
- ลืมว่า `inner` ทิ้งแถวที่ไม่ match — ข้อมูลหายโดยไม่รู้ตัว → ให้เช็ก `len()` ก่อน-หลัง merge
- สับสน `merge` (ต่อตามคอลัมน์/key) กับ `concat` (แปะต่อกันตรง ๆ บน-ล่าง)
- key ซ้ำทั้งสองฝั่ง → แถวบานปลาย (row explosion) — ให้ `drop_duplicates` key ก่อน

### ✍️ Mini Exercise (ใช้ข้อมูล QuickMart จริง)
```python
import pandas as pd
RAW = "datasets/new-raw"
orders   = pd.read_csv(f"{RAW}/orders.csv")
customers= pd.read_csv(f"{RAW}/customers.csv")

# โจทย์: ตอบให้ได้ว่า ลูกค้า tier ไหนสั่งซื้อรวมเยอะสุด
df = orders.merge(customers[["customer_id","sub_tier"]], on="customer_id", how="left")
print(df.groupby("sub_tier")["amount"].sum().sort_values(ascending=False))
```
ให้นักเรียนลองเปลี่ยน `how="left"` เป็น `inner` แล้วสังเกตว่าจำนวนแถวต่างกันไหม (orphan customer_id)

---

## เชื่อมโยงกับ Assignment
- `02_assignment/pandas_practice_project.ipynb` — ฝึก clean → join → วิเคราะห์ ทีละ TASK
- `02_assignment/workshop_eda.ipynb` — EDA เต็มรูปแบบ + กราฟ (revenue by category/brand/tier)
- ทั้งคู่รันบน `datasets/new-raw/` (ข้อมูลสกปรกจริง) → นักเรียนได้ใช้ section 8 + 9 ของจริง

## คำถามนำสนทนา (ปิดท้ายคาบ)
- "ทำไม merge แล้วข้อมูลหายไปครึ่งนึง?" → โยง `how=inner` + key dtype
- "ถ้า groupby แล้วได้ค่าแปลก ๆ ควรเช็กอะไรก่อน?" → โยงกลับ section 8 (ข้อมูลยังไม่ clean)
