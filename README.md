# Data Engineer Essential

Structured learning path covering Python fundamentals through data engineering with real-world storage systems.

## Curriculum

| Module | Topics |
|--------|--------|
| `01_python_basics/` | Variables, data types, operators, I/O, control flow, functions, data structures, error handling |
| `02_working_with_data/` | File handling (txt/csv/json), data analysis process, Pandas + EDA workshop |
| `03_data_ingestion/` | Files, APIs, databases |
| `04_data_storage/` | Database, Data Lake (RustFS), Data Warehouse (ClickHouse), Data Lakehouse |

## Setup

Uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync                         # create .venv and install dependencies
cp .env.example .env            # fill in connection details
```

## Running Examples

```bash
# Run any Python script
uv run 01_python_basics/01_variables.py

# Open EDA workshop notebook
uv run jupyter notebook 02_working_with_data/03_pandas/workshop_eda.ipynb
```

## Dataset

`datasets/sales.csv` — Q1 2024 sales data (54 rows) used throughout workshops.
