# Data Engineer Essential

Structured learning path covering Python fundamentals through data engineering with real-world storage systems. Each module is self-contained and runnable, using a shared sales dataset throughout.

## Curriculum

| Module | Topics |
|--------|--------|
| `01_python_basics/` | Variables, data types, operators, I/O, control flow, functions, data structures, error handling |
| `02_working_with_data/` | File handling (txt/csv/json), data analysis process, Pandas + EDA workshop |
| `03_data_ingestion/` | Files, APIs, databases (extract → validate → transform → load) |
| `04_data_storage/` | Database, Data Lake (RustFS), Data Warehouse (ClickHouse), Data Lakehouse (Delta Lake) |

## Prerequisites

Install [uv](https://docs.astral.sh/uv/) (manages Python and dependencies):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux
```

## Setup

```bash
uv sync                         # create .venv and install dependencies
cp .env.example .env            # fill in connection details for storage backends
```

## Running Examples

```bash
# Run any Python script
uv run 01_python_basics/01_variables/01_variables.py
uv run 02_working_with_data/02_data_analysis_process/04_eda.py

# Open the EDA workshop notebook
uv run jupyter notebook 02_working_with_data/03_pandas/workshop_eda.ipynb
```

## External Services

The storage modules in `04_data_storage/` connect to backends. Database and Delta Lake examples need no setup; the others run via Docker:

| Service | Used in | Docker |
|---------|---------|--------|
| SQLite | `04_data_storage/01_database/` | Built-in, no setup |
| RustFS / MinIO | `04_data_storage/02_data_lake/` | `docker run -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ':9001'` |
| ClickHouse | `04_data_storage/03_data_warehouse/` | `docker run -p 9000:9000 -p 8123:8123 clickhouse/clickhouse-server` |
| Delta Lake | `04_data_storage/04_data_lakehouse/` | No service — writes to `/tmp/delta/` |

## Datasets

| File | Description |
|------|-------------|
| `datasets/sales.csv` | Q1 2024 sales data (54 rows): date, product, category, quantity, unit_price, revenue, region |
| `datasets/products.json` | 13-product catalog with nested structure |
| `datasets/sample.txt` | Plain text for file-handling exercises |
