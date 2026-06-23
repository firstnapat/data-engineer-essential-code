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
uv run 02_working_with_data/02_data_analysis_process/04_eda.py

# EDA workshop notebook
uv run jupyter notebook 02_working_with_data/03_pandas/workshop_eda.ipynb
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

02_working_with_data/
  01_file_handling/            # read txt/csv/json with stdlib (no pandas)
  02_data_analysis_process/    # 4-step EDA methodology as scripts
  03_pandas/                   # pandas basics, Series, merge/join + workshop_eda.ipynb
  04_numpy/                    # arrays, vectorization, broadcasting, aggregations
  05_visualization/            # matplotlib + seaborn charts (saved to /tmp/viz/)

03_data_ingestion/
  01_files/                    # ingest_csv.py, ingest_json.py (extract→validate→transform→load)
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
  sample.txt                   # plain text for file handling exercises
```

## Architecture Patterns

**Ingestion scripts** (`03_data_ingestion/`) follow the extract → validate → transform → load pattern. Functions are separated by responsibility and raise exceptions on validation failures.

**Storage scripts** (`04_data_storage/`) require external services (ClickHouse, RustFS/MinIO, or just local disk for Delta). Storage backends that need Docker are called out in the module docstring with the `docker run` command.

**File handling** (`02_working_with_data/01_file_handling/`) intentionally uses stdlib (`csv`, `json`) — no pandas — to teach the fundamentals before introducing the abstraction.

**Datasets path convention:** scripts use `os.path.join(os.path.dirname(__file__), "../../datasets")` to resolve `datasets/` relative to the script location.

## External Services

| Service | Used in | Docker |
|---------|---------|--------|
| ClickHouse | `04_data_storage/03_data_warehouse/` | `docker run -p 9000:9000 -p 8123:8123 clickhouse/clickhouse-server` |
| RustFS / MinIO | `04_data_storage/02_data_lake/` | `docker run -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ':9001'` |
| Delta Lake | `04_data_storage/04_data_lakehouse/` | No service — writes to `/tmp/delta/` |
| SQLite | `03_data_ingestion/03_database/`, `04_data_storage/01_database/` | Built-in, no setup |
