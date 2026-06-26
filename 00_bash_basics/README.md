# 00 — Bash Basics for Data Engineers 🐧

> Workshop พื้นฐาน Command Line สำหรับ Data Engineer
> เรียนผ่านสถานการณ์จริง (Business Scenario) ทีละบท แล้วลงมือทำเองในเครื่อง

ในงาน Data Engineer คุณจะต้อง SSH เข้า Server, ดู log, ย้ายไฟล์ข้อมูล,
ค้นหา error และรัน pipeline script — ทั้งหมดนี้ทำผ่าน **Terminal**
โมดูลนี้ปูพื้นฐาน Bash ให้พร้อมก่อนเข้าสู่งาน Data จริง

---

## วิธีใช้ Workshop นี้

1. `cd` เข้าไปในโฟลเดอร์ของแต่ละบท (เช่น `cd 01_basics`)
2. อ่าน **Business Scenario** เพื่อเข้าใจว่าทำไมต้องใช้คำสั่งนี้
3. ลองพิมพ์คำสั่งใน **Introduced Command**
4. ทำ **Student Activity** ด้วยตัวเอง
5. เทียบกับ **Expected Output**
6. ถ้าติด ให้อ่าน **Discussion**

> 💡 ทุกบทออกแบบให้รันได้จริงในโฟลเดอร์นี้ ไม่ต้องต่อ internet หรือ service ใด ๆ

### โครงสร้างโมดูล

```
00_bash_basics/
├── 01_basics/            # pwd, whoami, echo, cat — สำรวจตัวเองและระบบ
├── 02_navigation/        # pwd, ls, cd, tree — เดินใน file system
├── 03_file_management/   # mkdir, cp, mv, rm, touch — จัดการไฟล์ข้อมูล
├── 04_viewing_files/     # cat, less, head, tail, wc — อ่านไฟล์ใหญ่
├── 05_searching/         # grep, find — ค้นหา error และไฟล์
├── 06_pipe_redirect/     # | > >> sort uniq — ต่อท่อคำสั่ง + เขียนผลลัพธ์
├── 07_environment/       # env, export, source, ./script.sh — ตัวแปรและ script
└── mini_incident/        # โจทย์รวม: debug pipeline ที่ล่ม
```

---

# บทที่ 01 — Basics: รู้จักตัวเองและระบบ

📂 ทำงานในโฟลเดอร์ `01_basics/`

### 1. Learning Objective
เมื่อจบบทนี้ ผู้เรียนจะสามารถ
* เข้าใจว่า Terminal / Shell คืออะไร
* ใช้ `whoami`, `hostname`, `date`, `echo`
* อ่านไฟล์ข้อความด้วย `cat`

### 2. Business Scenario
**วันแรกของการทำงาน**

ยินดีต้อนรับสู่ทีม Data Engineering 🎉
Senior ส่งข้อความมาใน Microsoft Teams:

> **Senior Engineer:** "Morning 👋 ลอง SSH เข้า Server ดูก่อนนะ
> เช็กหน่อยว่าตอนนี้ login เป็น user อะไร เครื่องชื่ออะไร เดี๋ยวบ่ายเรา debug กัน"

ตอนนี้คุณเพิ่งเข้า Server มา แต่ยังไม่รู้ด้วยซ้ำว่า… *คุณเป็นใครในเครื่องนี้?*

### 3. Introduced Command
```bash
whoami            # ฉัน login เป็น user อะไร
hostname          # เครื่องนี้ชื่ออะไร
date              # ตอนนี้วันเวลาอะไร
echo "Hello DE"   # พิมพ์ข้อความออกหน้าจอ
cat hello.txt     # อ่านเนื้อหาไฟล์
```

### 4. Student Activity
> **Question:** เปิดไฟล์ `hello.txt` ออกมาอ่านด้วยคำสั่งเดียว
> และลองเปิด `system_info.txt` เพื่อดูข้อมูลระบบจำลอง

### 5. Expected Output
```text
Hello, Data Engineer!
ยินดีต้อนรับสู่โลกของ Command Line 🐧
...
```

### 6. Discussion
ยังคิดไม่ออก?
* `cat` ย่อมาจาก *concatenate* — ใช้พ่นเนื้อหาไฟล์ออกหน้าจอ
* ลองถามตัวเอง: ถ้าไฟล์ยาวมาก ๆ การ `cat` ทั้งไฟล์เป็นความคิดที่ดีไหม? (เก็บคำถามนี้ไว้ตอบในบท 04)

---

# บทที่ 02 — Navigation: เดินใน File System

📂 ทำงานในโฟลเดอร์ `02_navigation/`

### 1. Learning Objective
เมื่อจบบทนี้ ผู้เรียนจะสามารถ
* เข้าใจว่า Current Working Directory (CWD) คืออะไร
* ใช้ `pwd`, `ls`, `cd`, `tree`
* Navigate ภายใน Linux File System ได้
* อ่านโครงสร้าง Project ก่อนเริ่มทำงาน

### 2. Business Scenario
**สำรวจ Project ก่อน Debug**

> **Senior Engineer:** "Pipeline Project อยู่ใน Server แล้ว
> ลองเข้าไปดูโครงสร้าง Project ก่อนนะ เดี๋ยวบ่ายเรา debug กัน"

ตอนนี้… ❓ ไม่รู้ว่าอยู่ folder ไหน ❓ ไม่รู้ project อยู่ตรงไหน ❓ ไม่รู้ข้างในมีอะไร

### 3. Introduced Command
```bash
pwd                 # ฉันอยู่ folder ไหนตอนนี้
ls                  # มีอะไรใน folder นี้บ้าง
ls -la              # ดูแบบละเอียด (รวมไฟล์ซ่อน + สิทธิ์)
cd projects         # เดินเข้า folder projects
cd ..               # ถอยกลับขึ้นไป 1 ชั้น
cd ~                # กลับ home directory
tree                # ดูโครงสร้างทั้งหมดเป็นต้นไม้ (ถ้ามีติดตั้ง)
tree -L 2           # จำกัดความลึก 2 ชั้น
```

### 4. Student Activity
> **Question:** Current Directory ของคุณคืออะไร?
> จากนั้น `cd` เข้าไปใน `projects/ecommerce` แล้วเช็ก path อีกครั้ง
> สุดท้ายกลับมาที่ `02_navigation` แล้วใช้ `tree` ดูโครงสร้าง

### 5. Expected Output
```text
/.../00_bash_basics/02_navigation

/.../00_bash_basics/02_navigation/projects/ecommerce

.
├── archive
└── projects
    ├── banking
    └── ecommerce
```

### 6. Discussion
ยังคิดไม่ออก?
* `.` คือ folder ปัจจุบัน, `..` คือ folder แม่
* Path แบบ **absolute** เริ่มด้วย `/` ส่วน **relative** อ้างจากที่ที่เรายืนอยู่
* ทำไมต้องสำรวจโครงสร้างก่อนเริ่มงาน? เพราะถ้าไม่รู้ว่าข้อมูลอยู่ตรงไหน คุณจะ debug ไม่ได้เลย

---

# บทที่ 03 — File Management: จัดการไฟล์ข้อมูล

📂 ทำงานในโฟลเดอร์ `03_file_management/`

### 1. Learning Objective
เมื่อจบบทนี้ ผู้เรียนจะสามารถ
* สร้าง / คัดลอก / ย้าย / ลบ ไฟล์และโฟลเดอร์
* ใช้ `mkdir`, `touch`, `cp`, `mv`, `rm`
* เข้าใจ pattern raw → processed → backup

### 2. Business Scenario
**จัดระเบียบ Data ก่อนประมวลผล**

> **Senior Engineer:** "ไฟล์ raw มาแล้วใน `raw/`
> ช่วย backup ไว้ก่อน แล้วเตรียม folder `processed/` สำหรับผลลัพธ์ด้วยนะ"

คุณมี `customer.csv`, `sales.csv`, `product.csv` อยู่ใน `raw/`
ต้องสำเนาเก็บไว้ที่ `backup/` ก่อนแตะต้องของจริง

### 3. Introduced Command
```bash
mkdir staging                     # สร้าง folder ใหม่
mkdir -p a/b/c                    # สร้าง folder ซ้อนหลายชั้นทีเดียว
touch processed/empty.csv         # สร้างไฟล์เปล่า
cp raw/sales.csv backup/          # คัดลอกไฟล์
cp -r raw backup_raw              # คัดลอกทั้ง folder (-r = recursive)
mv staging archived_staging       # เปลี่ยนชื่อ / ย้าย
rm processed/empty.csv            # ลบไฟล์
rm -r archived_staging            # ลบทั้ง folder (ระวัง! ไม่มีถังขยะ)
```

### 4. Student Activity
> **Question:** สำเนาไฟล์ทั้ง 3 จาก `raw/` ไปไว้ที่ `backup/`
> แล้วตรวจสอบว่า `backup/` มีครบ 3 ไฟล์

### 5. Expected Output
```text
customer.csv  product.csv  sales.csv
```

### 6. Discussion
ยังคิดไม่ออก?
* `*` คือ wildcard — `*.csv` หมายถึงทุกไฟล์ที่ลงท้าย `.csv`
* ⚠️ `rm` บน Linux **ไม่มี Recycle Bin** ลบแล้วหายเลย — ตรวจ path ทุกครั้งก่อนกด Enter
* ทำไมต้อง backup ก่อนแก้? เพราะ data ที่หายไปอาจกู้ไม่ได้

---

# บทที่ 04 — Viewing Files: อ่านไฟล์ใหญ่อย่างชาญฉลาด

📂 ทำงานในโฟลเดอร์ `04_viewing_files/`

### 1. Learning Objective
เมื่อจบบทนี้ ผู้เรียนจะสามารถ
* เลือกใช้คำสั่งดูไฟล์ให้เหมาะกับขนาดไฟล์
* ใช้ `cat`, `less`, `head`, `tail`, `wc`
* ดู log แบบ real-time ด้วย `tail -f`

### 2. Business Scenario
**ไฟล์ log ใหญ่เกินกว่าจะเปิดทั้งหมด**

> **Senior Engineer:** "ไฟล์ `big_file.csv` มี 500 แถว ไม่ต้อง cat ทั้งไฟล์นะ
> ขอแค่ดู 5 แถวแรกพอว่า header หน้าตาเป็นยังไง แล้วเช็กด้วยว่าทั้งไฟล์มีกี่บรรทัด"

จำคำถามค้างจากบท 01 ได้ไหม? — `cat` ไฟล์ใหญ่ = หน้าจอท่วม

### 3. Introduced Command
```bash
head big_file.csv          # ดู 10 บรรทัดแรก
head -n 5 big_file.csv     # ดู 5 บรรทัดแรก
tail big_file.csv          # ดู 10 บรรทัดท้าย
tail -n 20 application.log  # ดู 20 บรรทัดท้าย
tail -f application.log     # ตามดู log ที่เขียนเข้ามาแบบ real-time (Ctrl+C ออก)
wc -l big_file.csv         # นับจำนวนบรรทัด
less big_file.csv          # เปิดดูแบบเลื่อนได้ (q เพื่อออก, / เพื่อค้นหา)
cat config.json            # ไฟล์เล็ก ๆ ใช้ cat ได้
```

### 4. Student Activity
> **Question:** `big_file.csv` มีทั้งหมดกี่บรรทัด (รวม header)?
> และ header (บรรทัดแรก) มี column อะไรบ้าง?

### 5. Expected Output
```text
501 big_file.csv

event_id,user_id,event_type,timestamp,value
```

### 6. Discussion
ยังคิดไม่ออก?
* ตารางเลือกใช้: ไฟล์เล็ก → `cat` / ดูหัวท้าย → `head`,`tail` / เลื่อนอ่าน → `less` / ตาม log สด → `tail -f`
* `501` บรรทัด = 500 แถวข้อมูล + 1 header
* `tail -f` คือเพื่อนสนิทของ Data Engineer ตอนเฝ้าดู pipeline กำลังรัน

---

# บทที่ 05 — Searching: ค้นหา Error และไฟล์

📂 ทำงานในโฟลเดอร์ `05_searching/`

### 1. Learning Objective
เมื่อจบบทนี้ ผู้เรียนจะสามารถ
* ค้นหาข้อความในไฟล์ด้วย `grep`
* ค้นหาไฟล์ในระบบด้วย `find`
* ใช้ option สำคัญ เช่น `-i`, `-n`, `-r`, `-c`

### 2. Business Scenario
**หา Error ในกองไฟล์ log**

> **Senior Engineer:** "มี log อยู่หลายไฟล์ใน `logs/`
> ช่วยหาหน่อยว่ามี ERROR กี่ครั้ง และเกิดที่บรรทัดไหนบ้าง"

การไล่อ่าน log ทีละบรรทัดด้วยตา = ช้าและพลาดง่าย

### 3. Introduced Command
```bash
grep "ERROR" logs/app.log            # หาบรรทัดที่มีคำว่า ERROR
grep -i "error" logs/app.log         # ไม่สนตัวพิมพ์เล็ก/ใหญ่
grep -n "ERROR" logs/app.log         # แสดงเลขบรรทัดด้วย
grep -c "ERROR" logs/app.log         # นับจำนวนบรรทัดที่เจอ
grep -r "ERROR" logs/                # ค้นทุกไฟล์ใน folder (recursive)
grep -r "timeout" logs/              # หาคำว่า timeout ทุกไฟล์

find . -name "*.log"                 # หาไฟล์ทุกตัวที่ลงท้าย .log
find . -name "requirement.txt"       # หาไฟล์ตามชื่อ
find . -type d                       # หาเฉพาะ folder
```

### 4. Student Activity
> **Question:** ใน `logs/` ทั้งหมด มีบรรทัดที่มีคำว่า ERROR กี่บรรทัด?
> และไฟล์ไหนบ้างที่มีคำว่า `timeout`?

### 5. Expected Output
```text
10

logs/pipeline.log
```

### 6. Discussion
ยังคิดไม่ออก?
* `grep -r` ค้นทั้ง folder, เติม `-l` เพื่อให้บอกแค่ "ชื่อไฟล์" ที่เจอ
* `grep` = ค้นหา *ข้อความในไฟล์*, `find` = ค้นหา *ตัวไฟล์/โฟลเดอร์เอง* — อย่าสับสน
* การ pipe `grep ... | wc -l` เพื่อ "นับ" คือ teaser ของบทถัดไป

---

# บทที่ 06 — Pipe & Redirect: ต่อท่อคำสั่งและเขียนผลลัพธ์

📂 ทำงานในโฟลเดอร์ `06_pipe_redirect/`

### 1. Learning Objective
เมื่อจบบทนี้ ผู้เรียนจะสามารถ
* ต่อ output ของคำสั่งหนึ่งเป็น input ของอีกคำสั่งด้วย `|`
* เขียนผลลัพธ์ลงไฟล์ด้วย `>` (เขียนทับ) และ `>>` (ต่อท้าย)
* ประกอบคำสั่ง `sort`, `uniq`, `cut`, `wc` เข้าด้วยกัน

### 2. Business Scenario
**สร้างรายงานสรุปจาก users.csv**

> **Senior Engineer:** "ช่วยทำ report สั้น ๆ หน่อย
> ว่ามี user จากประเทศ TH กี่คน แต่ละ plan มีกี่คน แล้ว save ลง `output/report.txt`"

### 3. Introduced Command
```bash
cat input/users.csv | wc -l                 # นับจำนวนบรรทัด
grep "TH" input/users.csv | wc -l           # นับ user ที่อยู่ TH
cut -d',' -f4 input/users.csv               # ตัดเอาเฉพาะ column ที่ 4 (plan)
cut -d',' -f4 input/users.csv | sort | uniq -c   # นับจำนวนแต่ละ plan

# Redirect: เขียนผลลัพธ์ลงไฟล์
echo "== Report ==" > output/report.txt      # > เขียนทับไฟล์
grep -c "TH" input/users.csv >> output/report.txt   # >> ต่อท้ายไฟล์
cat output/report.txt                        # ดูผลลัพธ์
```

### 4. Student Activity
> **Question:** เขียนคำสั่งชุดเดียวที่นับจำนวน user แยกตาม `plan`
> (free / pro / enterprise) แล้วบันทึกลง `output/report.txt`

### 5. Expected Output
```text
      7 free
      5 pro
      3 enterprise
```
*(ลำดับการแสดงผลอาจต่างกันเล็กน้อยตามการ sort)*

### 6. Discussion
ยังคิดไม่ออก?
* `|` (pipe) ส่ง output ของคำสั่งซ้ายไปเป็น input ของคำสั่งขวา
* `>` เขียนทับของเดิมทั้งหมด ส่วน `>>` ต่อท้าย — ระวังใช้ `>` ผิดแล้วข้อมูลเดิมหาย
* `tail -n +2` ใช้ตัด header (เริ่มอ่านจากบรรทัดที่ 2) ก่อนนับ
* แนวคิด "เอาคำสั่งเล็ก ๆ มาต่อกัน" คือหัวใจของ Unix philosophy

---

# บทที่ 07 — Environment & Scripts: ตัวแปรและ Shell Script

📂 ทำงานในโฟลเดอร์ `07_environment/`

### 1. Learning Objective
เมื่อจบบทนี้ ผู้เรียนจะสามารถ
* อ่าน/ตั้งค่า environment variable ด้วย `echo $VAR`, `export`
* เข้าใจความต่างของการรัน script แบบ `source` กับ `./`
* รัน shell script และให้สิทธิ์ execute ด้วย `chmod +x`

### 2. Business Scenario
**รัน Pipeline ผ่าน Script**

> **Senior Engineer:** "Pipeline เราสั่งรันด้วย `run_pipeline.sh`
> ค่าต่าง ๆ เก็บใน environment variable นะ ลอง `source config.sh` แล้วรันดู
> อ๋อ อย่า hardcode password ลง git ล่ะ ใช้ไฟล์ env เอา"

### 3. Introduced Command
```bash
echo $HOME                       # อ่านค่า environment variable
echo $PATH                       # ดู path ที่ระบบใช้หาโปรแกรม
export PIPELINE_NAME="daily"     # ตั้งค่าตัวแปรชั่วคราวใน shell นี้
env | grep PIPELINE              # ดูตัวแปร environment ที่มีคำว่า PIPELINE

source scripts/config.sh         # โหลดตัวแปรเข้า shell ปัจจุบัน
echo $WAREHOUSE_HOST             # เช็กว่าค่าถูกโหลดเข้ามาจริง

chmod +x scripts/run_pipeline.sh # ให้สิทธิ์ execute (ครั้งแรก)
./scripts/run_pipeline.sh        # รัน script
```

### 4. Student Activity
> **Question:** `source scripts/config.sh` แล้วตรวจสอบว่าตัวแปร
> `WAREHOUSE_HOST` มีค่าอะไร จากนั้นรัน `run_pipeline.sh`

### 5. Expected Output
```text
[config] environment loaded for pipeline: daily_sales

clickhouse-prod-01

 Running pipeline : daily_sales
 ...
Pipeline daily_sales finished successfully ✅
```

### 6. Discussion
ยังคิดไม่ออก?
* `source script.sh` รันใน shell ปัจจุบัน → ตัวแปรอยู่ต่อ; `./script.sh` รันใน sub-shell → ตัวแปรหายเมื่อจบ
* ทำไม secret ต้องอยู่ใน env ไม่ใช่ในโค้ด? เพื่อกัน password หลุดลง git (ดู `env_example.txt`)
* นี่คือ pattern เดียวกับที่โปรเจกต์นี้ใช้: `cp .env.example .env`

---

# 🚨 Mini Incident: Pipeline ล่มกลางดึก (โจทย์รวม)

📂 ทำงานในโฟลเดอร์ `mini_incident/`

บทนี้รวมทุกทักษะจากบท 01–07 มาแก้ปัญหาจริง — **ลองทำเองก่อนเปิดเฉลย**

### 1. Learning Objective
เมื่อจบบทนี้ ผู้เรียนจะสามารถ
* ประยุกต์ navigation + viewing + searching เพื่อ debug ปัญหาจริง
* ไล่หา root cause จาก log จนถึงไฟล์ข้อมูลที่ผิด
* เขียนสรุป incident report

### 2. Business Scenario
**02:00 — Alert ดังกลางดึก ⏰**

> **Microsoft Teams #data-eng-oncall:** "🔴 Pipeline `nightly_sales` FAILED"

> **Senior Engineer:** "ฝากดูหน่อยได้ไหม log อยู่ที่ `production/logs/`
> ไฟล์ข้อมูลที่ validate ไม่ผ่านถูกโยนไปที่ `production/data/`
> หา root cause ให้ทีว่าเกิดจากอะไร แล้วเขียนสรุปมา"

### 3. Introduced Command
*(ใช้คำสั่งที่เรียนมาทั้งหมด)*
```bash
cd mini_incident/production/logs
tail -n 20 pipeline_error.log        # ดู log ล่าสุด
grep "ERROR" pipeline_error.log      # กรองเฉพาะ ERROR
grep -n "5832" pipeline_error.log    # หา row ที่ระบบฟ้อง

cd ../data
cat failed_job.csv                   # ดูข้อมูลที่ validate ไม่ผ่าน
```

### 4. Student Activity
> **Question:**
> 1. Pipeline ชื่ออะไร และ FAILED ที่ stage ไหน?
> 2. แถวข้อมูล (order_id) ไหนที่ทำให้พัง และพังเพราะอะไร?
> 3. เขียนสรุป root cause + วิธีแก้ลงไฟล์ของคุณเอง

### 5. Expected Output
```text
... Schema mismatch on line 5832: expected 6 columns, got 5 (column 'amount' missing)
... NoneType has no attribute 'split' at transform.parse_amount (row 5832)
... Pipeline 'nightly_sales' FAILED after 9s

O5832,C055,P04,,2024-03-14        # <- ขาด column amount
```

### 6. Discussion
ยังคิดไม่ออก?
* ไล่จากบนลงล่าง: alert → เปิด log → `grep ERROR` → เจอเลขบรรทัด → เปิดไฟล์ข้อมูลที่ผิด
* Root cause: แถว `O5832` มี column ไม่ครบ (ขาด `amount`) ทำให้ transform พังเพราะค่าเป็น None
* เฉลยฉบับเต็มอยู่ที่ `solution/incident_report.txt` — **เปิดหลังจากลองทำเองแล้วเท่านั้น**

---

## 🎓 สรุปคำสั่งทั้งหมด (Cheat Sheet)

| หมวด | คำสั่ง |
|------|--------|
| ระบบ/ตัวเอง | `whoami` `hostname` `date` `echo` |
| Navigate | `pwd` `ls` `ls -la` `cd` `cd ..` `tree` |
| จัดการไฟล์ | `mkdir` `mkdir -p` `touch` `cp` `cp -r` `mv` `rm` `rm -r` |
| ดูไฟล์ | `cat` `head` `tail` `tail -f` `less` `wc -l` |
| ค้นหา | `grep` `grep -i/-n/-c/-r/-l` `find` |
| Pipe/Redirect | `\|` `>` `>>` `sort` `uniq -c` `cut` |
| Environment | `echo $VAR` `export` `env` `source` `chmod +x` `./script.sh` |

> ก้าวต่อไป: เมื่อคล่อง Bash แล้ว ไปต่อที่ `01_python_basics/` เพื่อเขียนโปรแกรมจัดการข้อมูล 🐍
