# Data Engineer Essential

Structured learning path covering Python fundamentals through data engineering with real-world storage systems. Each module is self-contained and runnable, using a shared sales dataset throughout.

## Curriculum

| Module | Topics |
|--------|--------|
| `00_bash_basics/` | Command line for data engineers: navigation, file management, viewing/searching files, pipes & redirects, environment & shell scripts, plus a mini incident-debugging exercise (scenario-driven, no Python needed) |
| `01_python_basics/` | Variables, data types, operators, I/O, control flow, functions, data structures, error handling, string manipulation, modules |
| `02_working_with_data/` | Data manipulation with pandas — Series, DataFrame, read/write, selecting, statistics, cleaning, merge/join — taught as a single notebook, plus a practice project and a products EDA workshop |
| `03_data_sources/` | Where data comes from and its formats: files (text/csv/json/xml/parquet/avro), REST APIs, databases |
| `04_data_storage/` | Set up the destinations: Database (schema), Data Lake (RustFS), Data Warehouse (ClickHouse), Data Lakehouse (Delta Lake) |
| `05_data_ingestion/` | Move source data into a destination: → database (schema-on-write), → data lake (schema-on-read), → lakehouse (Delta MERGE upsert) |

## Prerequisites

Install [uv](https://docs.astral.sh/uv/) (manages Python and dependencies):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux
```

## Setup

```bash
uv sync                         # create .venv and install dependencies
cp .env.example .env            # connection details for storage backends (defaults work)
docker compose up -d            # start Postgres, ClickHouse, and RustFS
```

Stop the services with `docker compose down` (add `-v` to also wipe the data volumes).

# Running Examples

```bash
# Run any Python script
uv run 03_data_sources/01_files/work_with_csv.py
uv run 05_data_ingestion/01_to_database/load_to_database.py

# Open the pandas notebooks
uv run jupyter notebook 02_working_with_data/01_pandas/01_pandas.ipynb
uv run jupyter notebook 02_working_with_data/02_assignment/workshop_eda.ipynb
```

The `00_bash_basics/` module needs no Python — work through it directly in a terminal (`cd 00_bash_basics` and follow its `README.md`).

## Refactoring Loop to Functional Style (Map & Reduce)

ประเด็นที่น่าสนใจและข้อดี-ข้อเสียในการเปลี่ยนจากโครงสร้างควบคุมการวนลูปแบบดั้งเดิมอย่าง `for` หรือ `while` ไปใช้ `map()`, `reduce()` ร่วมกับ `lambda` ใน Python เพื่อประมวลผลข้อมูลสไตล์ Functional Programming:

### 1. ความกระชับของโค้ด (Conciseness)
* **แบบเดิม (`for` loop):** มักต้องสร้างรายการว่างขึ้นมาก่อน แล้วค่อยใช้ `.append()` เพื่อเพิ่มข้อมูลทีละตัว
  ```python
  numbers = [1, 2, 3, 4]
  squared = []
  for x in numbers:
      squared.append(x ** 2)
  ```
* **แบบใหม่ (`map` + `lambda`):** เขียนจบได้ในบรรทัดเดียว
  ```python
  squared = list(map(lambda x: x ** 2, numbers))
  ```

### 2. แนวคิดแบบ Functional Programming
* **Declarative Style:** `map` บอกว่าเรา "ต้องการทำอะไร" (What to do) กับข้อมูลทุกตัว มากกว่าจะบอก "ขั้นตอนการทำงานทีละระดับ" (How to do) เหมือน `for`/`while`
* **Immutability:** ลดการเปลี่ยนแปลงสถานะของตัวแปรระหว่างทาง (เช่น ตัวแปรนับรอบ หรือการเปลี่ยนค่าลิสต์ตรงๆ) ทำให้คาดเดาผลลัพธ์ของโค้ดได้ง่ายขึ้น

### 3. ประสิทธิภาพ (Performance)
* ใน Python ฟังก์ชัน `map()` ถูกเขียนด้วยภาษา C ซึ่งโดยทั่วไปจะทำงานได้เร็วกว่าลูป `for` ที่รันบนตัวแปลภาษา (Interpreter) ของ Python โดยตรง (อย่างไรก็ตาม ความเร็วที่เพิ่มขึ้นนี้อาจไม่มีนัยสำคัญหากฟังก์ชันใน `map` ซับซ้อนมาก)
* **Lazy Evaluation:** `map()` ใน Python 3 จะส่งกลับเป็น iterator (ไม่ได้สร้าง list ใหม่ขึ้นมาในหน่วยความจำทันที) ทำให้ประหยัดหน่วยความจำเมื่อทำงานกับข้อมูลขนาดใหญ่ จนกว่าจะมีการเรียกใช้งานจริง

---

### การเปรียบเทียบการ Refactor โค้ด

#### 1. การเปลี่ยนจาก Loop ไปใช้ `map`
`map(function, iterable)` ใช้เมื่อต้องการ**แปลงข้อมูลทุกตัว**ใน List/Iterable ด้วยฟังก์ชันเดียวกัน (แปลง 1:1)

* **แบบเดิม (`for` loop):**
  ```python
  usd_prices = [100, 250, 50, 1200]
  thb_prices = []
  for price in usd_prices:
      thb_prices.append(price * 35)
  ```
* **แบบ Refactored (`map` + `lambda`):**
  ```python
  usd_prices = [100, 250, 50, 1200]
  thb_prices = list(map(lambda price: price * 35, usd_prices))
  ```

#### 2. การเปลี่ยนจาก Loop ไปใช้ `reduce`
`reduce(function, iterable[, initializer])` จากไลบรารี `functools` ใช้เมื่อต้องการ**ยุบรวมข้อมูลทั้ง List ให้เหลือค่าเดียว** (เช่น หาผลรวม, หาค่ามากสุด) โดยจะนำผลลัพธ์ของคู่ก่อนหน้าไปคำนวณกับตัวถัดไปเรื่อยๆ

* **แบบเดิม (`while` loop):**
  ```python
  transactions = [1200, 450, 3000, 800]
  total_revenue = 0
  i = 0
  while i < len(transactions):
      total_revenue += transactions[i]
      i += 1
  ```
* **แบบ Refactored (`reduce` + `lambda`):**
  ```python
  from functools import reduce
  transactions = [1200, 450, 3000, 800]
  total_revenue = reduce(lambda x, y: x + y, transactions)
  ```

#### 3. แบบผสมผสาน: MapReduce Pattern
คำนวณราคารวมของสินค้าทั้งหมดในตะกร้าที่รวม VAT 7% แล้ว

* **แบบเดิม (`for` loop):**
  ```python
  cart_prices = [1000, 2000, 500]
  total_with_vat = 0
  for price in cart_prices:
      price_with_vat = price * 1.07
      total_with_vat += price_with_vat
  ```
* **แบบ Refactored (`map` -> `reduce`):**
  ```python
  from functools import reduce
  cart_prices = [1000, 2000, 500]
  total_with_vat = reduce(lambda acc, price: acc + price, map(lambda price: price * 1.07, cart_prices))
  ```

---

### ข้อควรระวัง (และทางเลือกอื่นที่ดีกว่าใน Python)

แม้ว่า `map` และ `lambda` จะสั้น แต่มีข้อเสียสำคัญคือ **อ่านยากขึ้น (Readability)** หากเงื่อนไขหรือตัวฟังก์ชันมีความซับซ้อน

ในชุมชน Python (รวมถึงคำแนะนำใน PEP 8) มักจะแนะนำให้ใช้ **List Comprehension** แทน เพราะอ่านง่ายและเป็นระเบียบมากกว่า:

```python
# ใช้ List Comprehension (อ่านง่ายที่สุดและเป็น Pythonic style)
squared = [x ** 2 for x in numbers]
```

**เปรียบเทียบ:**
* `map(lambda x: x ** 2, numbers)` -> ต้องทำความเข้าใจทั้ง `map` และ syntax ของ `lambda`
* `[x ** 2 for x in numbers]` -> อ่านตรงตัวเหมือนภาษาอังกฤษทั่วไป (เอา x กำลังสอง สำหรับ x ทุกตัวใน numbers)

## Exercises & Solutions

Each module from 03 to 05 includes a hands-on exercise in an `exercise/exercise.py` directory (e.g., `03_data_sources/01_files/exercise/exercise.py`). These exercises contain `TODO` items and test assertions for students to implement and verify their code.

The completed, fully working solutions to all these exercises are available on the **`teacher-guide`** branch. You can check it out with:

```bash
git checkout teacher-guide
```

## External Services

The storage modules in `04_data_storage/` connect to backends. SQLite and Delta Lake examples need no setup; the rest are provided by `docker compose up -d` (see `docker-compose.yml`):

| Service | Used in | Endpoint (host) |
|---------|---------|-----------------|
| SQLite | `04_data_storage/01_database/` | Built-in, no setup |
| RustFS (S3) | `04_data_storage/02_data_lake/` | S3 `:9000`, console `:9001` |
| ClickHouse | `04_data_storage/03_data_warehouse/` | native `:9009`, HTTP `:8123` |
| PostgreSQL | Ingestion / database examples | `:5432` |
| Delta Lake | `04_data_storage/04_data_lakehouse/` | No service — writes to `/tmp/delta/` |

> RustFS and ClickHouse both default to port 9000. To run them side by side, RustFS keeps `:9000` (the S3 endpoint) and ClickHouse's native protocol is mapped to host `:9009` (`CLICKHOUSE_PORT` in `.env`). The RustFS console is at <http://localhost:9001> (login `minioadmin` / `minioadmin`).

## Datasets

| File | Description |
|------|-------------|
| `datasets/sales.csv` | Q1 2024 sales data (54 rows): date, product, category, quantity, unit_price, revenue, region |
| `datasets/products.json` | 13-product catalog with nested structure |
| `datasets/products.xml` | 13-product catalog in XML format |
| `datasets/sample.txt` | Plain text for file-handling exercises |
