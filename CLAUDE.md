# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Structured learning codebase for a Data Engineer Essentials course. Each module is self-contained and runnable. All examples use `datasets/sales.csv` (54-row Q1 2024 sales data) or `datasets/products.json` as the shared dataset.

## Setup

Dependencies are managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`).

```bash
uv sync                         # create .venv and install dependencies
cp .env.example .env            # fill in connection details for storage backends
```

## Running Code

```bash
# Run any script directly (uv resolves the project environment)
uv run 01_python_basics/01_variables/01_variables.py
uv run 03_data_sources/01_files/work_with_xml.py
uv run 05_data_ingestion/01_to_database/load_to_database.py

# pandas notebook (module 02 is notebook-based)
uv run jupyter notebook 02_working_with_data/01_pandas/01_pandas.ipynb
```

## Module Structure

```
01_python_basics/              # Python fundamentals, runnable scripts
  01_variables/                # variable assignment and naming
  02_data_types/               # int, float, str, bool
  03_operators/                # arithmetic, comparison, logical
  04_input_output/             # print, input, formatting
  05_control_flow/             # if/else, for, while, list comprehension
  06_functions/                # definition, parameters, return values
  07_data_structures/          # list, tuple, dict, set
  08_error_handling/           # try/except, common errors
  09_string_manipulation/      # case, split/join, replace, search, formatting
  10_modules/                  # creating/importing your own module (sales_utils.py)

02_working_with_data/         # data manipulation with pandas
  00_setup/                    # 00_setup.py — verify env, jupyter + pandas conventions
  01_pandas/                   # 01_pandas.ipynb — single notebook, 9 sections (intro,
                               #   Series, DataFrame, read/write, select, stats,
                               #   manipulation, cleaning, merge/join/concat)
  02_assignment/               # pandas_practice_project.ipynb + workshop_eda.ipynb
                               #   (both run on datasets/new-raw/ QuickMart data)

03_data_sources/               # WHERE data comes from — each script: read → inspect → clean
  01_files/                    # work_with_{text,csv,json,xml,parquet,avro}.py (one per format)
  02_apis/                     # work_with_api.py — a REST API as a source (Open-Meteo)
  03_databases/                # work_with_db.py — query an existing DB as a source

04_data_storage/               # set up the DESTINATIONS first (schema + backends)
  01_database/                 # storage_db.py — star schema in SQLite (schema-on-write)
  02_data_lake/                # rustfs_example.py — S3-compatible via boto3
  03_data_warehouse/           # clickhouse_example.py — ClickHouse via clickhouse-driver
  04_data_lakehouse/           # lakehouse_example.py — Delta Lake via deltalake + DuckDB

05_data_ingestion/             # MOVE source data into a storage target (runnable, no Docker)
  01_to_database/              # load_to_database.py — extract→validate→create schema→load (SQLite)
  02_to_data_lake/             # load_to_lake.py — land partitioned parquet (schema-on-read)
  03_to_lakehouse/             # load_to_lakehouse.py — Delta initial load + idempotent MERGE upsert

datasets/
  sales.csv                    # 54 rows: date, product, category, quantity, unit_price, revenue, region
  products.json                # 13-product catalog with nested structure
  products.xml                 # same 13-product catalog in XML (for work_with_xml.py)
  sample.txt                   # plain text report (for work_with_text.py)
```

## Architecture Patterns

**Course flow:** `03_data_sources` (know your sources + formats) → `04_data_storage` (set up the destinations and their schema) → `05_data_ingestion` (move source data into a destination). Storage comes *before* ingestion on purpose: you set up the lake/warehouse/lakehouse/schema, then ingest into it.

**Schema timing:** a warehouse/database is **schema-on-write** — create the schema first, then load (see `05_data_ingestion/01_to_database`). A data lake is **schema-on-read** — land raw files now, apply structure at read time (see `05_data_ingestion/02_to_data_lake`).

**Data-source scripts** (`03_data_sources/`) each follow **read → inspect → clean** with `read()`, `inspect()`, `clean()` functions — no writing/loading (that's module 05). `01_files/` has one `work_with_<format>.py` per format (text, csv, json, xml, parquet, avro). Requires `pyarrow` (parquet), `fastavro` (avro), and `lxml` (xml via `pandas.read_xml`).

**Ingestion pipelines** (`05_data_ingestion/`) follow extract → validate → (create schema) → load, one subfolder per destination. All three run without Docker (SQLite, local filesystem, on-disk Delta).

**Storage scripts** (`04_data_storage/`) require external services (ClickHouse, RustFS/MinIO, or just local disk for Delta). Backends that need Docker are called out in the module docstring with the `docker run` command.

**Module 02 is notebook-based:** pandas is taught in a single executable notebook (`01_pandas/01_pandas.ipynb`). Since notebooks have no `__file__`, it resolves `datasets/` by searching upward (`.`, `..`, `../..`) so it runs whether Jupyter is launched from the repo root or the notebook's folder.

**Datasets path convention:** plain `.py` scripts use `os.path.join(os.path.dirname(__file__), "../../datasets")` to resolve `datasets/` relative to the script location.

## External Services

| Service | Used in | Docker |
|---------|---------|--------|
| ClickHouse | `04_data_storage/03_data_warehouse/` | `docker run -p 9000:9000 -p 8123:8123 clickhouse/clickhouse-server` |
| RustFS / MinIO | `04_data_storage/02_data_lake/` | `docker run -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ':9001'` |
| Delta Lake | `04_data_storage/04_data_lakehouse/` | No service — writes to `/tmp/delta/` |
| SQLite | `03_data_sources/03_databases/`, `04_data_storage/01_database/`, `05_data_ingestion/01_to_database/` | Built-in, no setup |
