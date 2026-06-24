# Data Engineer Essential

Structured learning path covering Python fundamentals through data engineering with real-world storage systems. Each module is self-contained and runnable, using a shared e-commerce dataset throughout.

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
