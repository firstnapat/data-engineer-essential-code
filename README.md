# Data Engineer Essential

## Scenario

**Refreshco** คือบริษัทจัดจำหน่ายเครื่องดื่มให้ร้านค้าทั่วประเทศ ธุรกิจกำลังโต แต่ข้อมูลกระจายอยู่ตามระบบต่าง ๆ — ทีมขายเก็บออเดอร์ในระบบ CRM, ทีมโลจิสติกส์มีระบบขนส่งของตัวเอง, ทีม Product เก็บ catalog ไว้ใน JSON

ทุกสัปดาห์ผู้บริหารต้องการคำตอบว่า _"ภาคไหนยอดตก สินค้าไหนขายดี"_ แต่ตอนนี้ต้องรอให้ทีม Finance รวม Excel ก่อนทุกครั้ง — กินเวลา 2–3 วัน

---

**คุณคือ Data Engineer คนแรกของทีม** ภารกิจคือสร้าง Data Platform ตั้งแต่ศูนย์:

```
Raw Sources          Object Storage       Data Warehouse
(CSV / API / DB) --> (RustFS / S3)    --> (ClickHouse)  --> Analyst query ได้เอง
                      เก็บ raw ไว้         transform &
                      reprocess ได้         aggregate
```

**เป้าหมายปลายทาง:**
- Analyst query ข้อมูลใน ClickHouse ได้ทันที ไม่ต้องรอ
- Raw data ยังอยู่ใน object storage เผื่อ reprocess ในอนาคต
- Pipeline รันซ้ำได้ (idempotent) ไม่มี duplicate

Pattern นี้คือ **ELT** (Extract → Load to lake → Transform in warehouse) ซึ่งเป็นแนวทางมาตรฐานในงาน Data Engineering ปัจจุบัน

---

## Stack & Rationale

เลือก tool แต่ละตัวด้วยเหตุผล ไม่ใช่แค่เพราะฟังดูดี

| Layer | Tool | หมวด |
|-------|------|------|
| Object Storage | RustFS (S3-compatible) | Data Lake |
| Data Warehouse | ClickHouse | OLAP |
| Lakehouse | Delta Lake + DuckDB | Lakehouse |
| Relational DB | SQLite | Database |
| Package manager | uv | Tooling |

### RustFS — Data Lake

RustFS ใช้ S3 API เหมือน AWS S3 ทุกประการ ซึ่งหมายความว่า boto3 code ที่เขียนในคอร์สนี้ **ใช้กับ AWS S3 จริงได้เลยโดยไม่ต้องแก้โค้ด** แค่เปลี่ยน endpoint URL

เหตุผลที่เลือก object storage สำหรับ raw data:
- **Schema-on-read** — เก็บไฟล์ได้ทุกรูปแบบ (CSV, JSON, Parquet) โดยไม่ต้องรู้ schema ล่วงหน้า
- **Immutable raw layer** — raw data อยู่ใน lake เสมอ ถ้า transform logic ผิดพลาดสามารถ reprocess ใหม่ได้
- **ราคา** — object storage ถูกกว่า database มาก เหมาะกับเก็บข้อมูลที่ยังไม่รู้ว่าจะใช้ยังไง

### ClickHouse — Data Warehouse

ClickHouse เป็น **column-oriented database** ออกแบบมาสำหรับ analytical queries (OLAP) โดยเฉพาะ ต่างจาก PostgreSQL ที่ออกแบบมาสำหรับ transactional workload (OLTP)

| | PostgreSQL | ClickHouse |
|-|-----------|------------|
| เหมาะกับ | INSERT/UPDATE/DELETE ถี่ ๆ | SELECT + GROUP BY ข้อมูลเยอะ |
| เก็บข้อมูล | Row-oriented | Column-oriented |
| Aggregate 100M แถว | ช้า | เร็วมาก |

จุดเด่นอีกข้อ: `s3()` table function ช่วยให้ ClickHouse **query ไฟล์ใน RustFS ได้โดยตรง** โดยไม่ต้องโหลดเข้า database ก่อน — นี่คือหัวใจของ module 05 (lake → warehouse)

### Delta Lake — Lakehouse

Delta Lake เพิ่ม **ACID transactions** ให้กับ Parquet files ธรรมดา

- **ไม่ต้องกลัว partial write** — ถ้า pipeline fail กลางคัน ข้อมูลจะ rollback อัตโนมัติ
- **Time travel** — ดูข้อมูล ณ version ก่อนหน้าได้ด้วย `version_as_of`
- **Pattern เหมือน production** — Databricks, Apache Spark, และ Azure Synapse ใช้ Delta Lake เป็น default storage format

### SQLite — Database module

ใช้ SQLite เพราะ built-in ใน Python ไม่ต้องติดตั้งอะไรเพิ่ม เหมาะที่สุดสำหรับสอน **schema-on-write concept** ให้ชัดเจน ก่อนไปจับ tool ที่ซับซ้อนกว่า

### uv — Package manager

`uv` เร็วกว่า `pip` มาก และแก้ปัญหา "มันรันได้บนเครื่องฉันนะ" ได้ด้วย lock file `uv run script.py` รัน script ได้เลยโดยไม่ต้อง activate virtual environment ก่อน

### ELT ไม่ใช่ ETL

คอร์สนี้สอน **ELT** (Extract → Load → Transform) แทน ETL แบบเก่า

```
ETL (แบบเก่า):  Extract → Transform → Load warehouse
ELT (แบบใหม่):  Extract → Load lake → Transform ใน warehouse
```

ทำไม ELT ดีกว่าในบริบทนี้:
- **Raw data ยังอยู่** — ถ้า business logic เปลี่ยน reprocess ได้ทันที ไม่ต้องดึงจาก source ใหม่
- **Transform ที่ warehouse** — compute อยู่ที่ ClickHouse แล้ว ใช้ SQL ตรง ๆ ไม่ต้องมี transformation layer พิเศษ
- **Pattern มาตรฐาน** — dbt, Fivetran, Airbyte และ modern data stack ส่วนใหญ่ทำแบบนี้

---

## Curriculum

| Module | Topics |
|--------|--------|
| `00_bash_basics/` | Command line for data engineers: navigation, file management, viewing/searching files, pipes & redirects, environment & shell scripts, plus a mini incident-debugging exercise |
| `01_python_basics/` | Variables, data types, operators, I/O, control flow, functions, data structures, error handling, string manipulation, modules |
| `02_working_with_data/` | Data manipulation with pandas — Series, DataFrame, read/write, selecting, statistics, cleaning, merge/join — taught as a single notebook, plus a practice project and an EDA workshop |
| `03_data_sources/` | Where data comes from and its formats: files (text/csv/json/xml/parquet/avro), REST APIs, databases |
| `04_data_storage/` | Set up the destinations: Database (SQLite), Data Lake (RustFS/S3), Data Warehouse (ClickHouse), Data Lakehouse (Delta Lake) |
| `05_data_ingestion/` | Move source data into a destination: → database (schema-on-write), → data lake (schema-on-read), → lakehouse (Delta MERGE upsert), → warehouse via lake (ClickHouse s3() function) |

## Prerequisites

Install [uv](https://docs.astral.sh/uv/) (manages Python and dependencies):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux
```

## Setup

```bash
uv sync                         # create .venv and install dependencies
cp .env.example .env            # connection details for storage backends (defaults work)
docker compose up -d            # start ClickHouse and RustFS
```

Stop the services with `docker compose down` (add `-v` to also wipe the data volumes).

## Running Examples

```bash
# Run any Python script
uv run 03_data_sources/01_files/work_with_csv.py
uv run 04_data_storage/02_data_lake/rustfs_example.py
uv run 04_data_storage/03_data_warehouse/clickhouse_example.py
uv run 05_data_ingestion/01_to_database/load_to_database.py

# Open the pandas notebooks
uv run jupyter notebook 02_working_with_data/01_pandas/01_pandas.ipynb
uv run jupyter notebook 02_working_with_data/02_assignment/workshop_eda.ipynb
```

The `00_bash_basics/` module needs no Python — work through it directly in a terminal.

## Exercises & Solutions

Each module from 03 to 05 includes a hands-on exercise at `exercise/exercise.py`. These contain `TODO` items and assertions for students to implement.

The completed solutions to all exercises are on the **`teacher-guide`** branch:

```bash
git checkout teacher-guide
```

## External Services

The storage modules in `04_data_storage/` connect to backends. SQLite and Delta Lake need no setup; the rest are started by `docker compose up -d`:

| Service | Used in | Endpoint |
|---------|---------|----------|
| SQLite | `04_data_storage/01_database/`, `05_data_ingestion/01_to_database/` | Built-in, no setup |
| RustFS (S3) | `04_data_storage/02_data_lake/`, `05_data_ingestion/02_to_data_lake/` | S3 `:9000`, console `:9001` |
| ClickHouse | `04_data_storage/03_data_warehouse/`, `05_data_ingestion/04_datalake_to_warehouse/` | HTTP `:8123` |
| Delta Lake | `04_data_storage/04_data_lakehouse/`, `05_data_ingestion/03_to_lakehouse/` | No service — writes to `/tmp/delta/` |

**RustFS authentication:** the Python examples read credentials from `credentials.json` placed next to the script. Download this file from the RustFS console at <http://localhost:9001> (login `minioadmin` / `minioadmin`) under **Access Keys → Create → Download**.

**ClickHouse** uses the HTTP interface on port 8123 via `clickhouse-connect`. The password is set by `CLICKHOUSE_PASSWORD` in `.env` (default: `clickhouse`).

## Datasets

### Shared formats dataset (modules 01–03)

| File | Description |
|------|-------------|
| `datasets/sales.csv` | Q1 2024 sales data (54 rows): date, product, category, quantity, unit_price, revenue, region |
| `datasets/products.json` | 13-product catalog with nested structure |
| `datasets/products.xml` | Same catalog in XML format |
| `datasets/sample.txt` | Plain text report for file-handling exercises |

### E-commerce raw datasets (modules 04–05)

Six related CSV files in `datasets/raw/` with intentional data quality issues for cleaning practice. See `datasets/er_diagram.md` for the full schema and relationships.

| File | Rows | Description |
|------|------|-------------|
| `datasets/raw/products_raw.csv` | 33 | Product catalog |
| `datasets/raw/users_raw.csv` | ~80 | Customer accounts |
| `datasets/raw/addresses_raw.csv` | ~90 | Shipping addresses |
| `datasets/raw/orders_raw.csv` | ~108 | Customer orders |
| `datasets/raw/order_items_raw.csv` | ~198 | Line items per order |
| `datasets/raw/transports_raw.csv` | ~100 | Shipment records |

Regenerate with: `uv run datasets/generate_raw_data.py`
