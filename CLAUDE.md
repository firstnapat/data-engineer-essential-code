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
uv run 03_data_ingestion/01_files/ingest_xml.py

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
                               #   (EDA workshop runs on datasets/products.json)

03_data_ingestion/
  01_files/                    # ingest handlers per format: text, csv, json, xml,
                               #   parquet, avro (extract→validate→transform→load)
  02_apis/                     # ingest_api.py (Open-Meteo weather, no auth required)
  03_database/                 # ingest_db.py (SQLite demo, SQLAlchemy pattern)

04_data_storage/
  01_database/                 # storage_db.py — star schema in SQLite
  02_data_lake/                # rustfs_example.py — S3-compatible via boto3
  03_data_warehouse/           # clickhouse_example.py — ClickHouse via clickhouse-driver
  04_data_lakehouse/           # lakehouse_example.py — Delta Lake via deltalake + DuckDB

datasets/
  sales.csv                    # 54 rows: date, product, category, quantity, unit_price, revenue, region
  products.json                # 13-product catalog with nested structure
  products.xml                 # same 13-product catalog in XML (for ingest_xml.py)
  sample.txt                   # plain text report (for ingest_text.py)
```

## Architecture Patterns

**Ingestion scripts** (`03_data_ingestion/`) follow the extract → validate → transform → load pattern. Functions are separated by responsibility and raise exceptions on validation failures.

**Storage scripts** (`04_data_storage/`) require external services (ClickHouse, RustFS/MinIO, or just local disk for Delta). Storage backends that need Docker are called out in the module docstring with the `docker run` command.

**File ingestion** (`03_data_ingestion/01_files/`) has one handler per format (text, csv, json, xml, parquet, avro). Each defines functions to read/parse the format into a pandas DataFrame; parquet/avro also demonstrate writing. Requires `pyarrow` (parquet), `fastavro` (avro), and `lxml` (xml via `pandas.read_xml`).

**Module 02 is notebook-based:** pandas is taught in a single executable notebook (`01_pandas/01_pandas.ipynb`). Since notebooks have no `__file__`, it resolves `datasets/` by searching upward (`.`, `..`, `../..`) so it runs whether Jupyter is launched from the repo root or the notebook's folder.

**Datasets path convention:** plain `.py` scripts use `os.path.join(os.path.dirname(__file__), "../../datasets")` to resolve `datasets/` relative to the script location.

## External Services

| Service | Used in | Docker |
|---------|---------|--------|
| ClickHouse | `04_data_storage/03_data_warehouse/` | `docker run -p 9000:9000 -p 8123:8123 clickhouse/clickhouse-server` |
| RustFS / MinIO | `04_data_storage/02_data_lake/` | `docker run -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ':9001'` |
| Delta Lake | `04_data_storage/04_data_lakehouse/` | No service — writes to `/tmp/delta/` |
| SQLite | `03_data_ingestion/03_database/`, `04_data_storage/01_database/` | Built-in, no setup |
