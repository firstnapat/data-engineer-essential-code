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

## Running Examples

```bash
# Run any Python script
uv run 01_python_basics/01_variables/01_variables.py
uv run 02_working_with_data/02_data_analysis_process/04_eda.py

# Open the EDA workshop notebook
uv run jupyter notebook 02_working_with_data/03_pandas/workshop_eda.ipynb
```

The `00_bash_basics/` module needs no Python — work through it directly in a terminal (`cd 00_bash_basics` and follow its `README.md`).

## External Services

The storage modules in `04_data_storage/` connect to backends. SQLite and Delta Lake examples need no setup; the rest are provided by `docker compose up -d` (see `docker-compose.yml`):

| Service | Used in | Endpoint (host) |
|---------|---------|-----------------|
| SQLite | `04_data_storage/01_database/` | Built-in, no setup |
| RustFS (S3) | `04_data_storage/02_data_lake/` | S3 `:9000`, console `:9001` |
| ClickHouse | `04_data_storage/03_data_warehouse/` | native `:9009`, HTTP `:8123` |
| PostgreSQL | ingestion / database examples | `:5432` |
| Delta Lake | `04_data_storage/04_data_lakehouse/` | No service — writes to `/tmp/delta/` |

> RustFS and ClickHouse both default to port 9000. To run them side by side, RustFS keeps `:9000` (the S3 endpoint) and ClickHouse's native protocol is mapped to host `:9009` (`CLICKHOUSE_PORT` in `.env`). The RustFS console is at <http://localhost:9001> (login `minioadmin` / `minioadmin`).

## Datasets

| File | Description |
|------|-------------|
| `datasets/sales.csv` | Q1 2024 sales data (54 rows): date, product, category, quantity, unit_price, revenue, region |
| `datasets/products.json` | 13-product catalog with nested structure |
| `datasets/sample.txt` | Plain text for file-handling exercises |
