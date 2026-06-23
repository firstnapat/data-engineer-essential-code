"""00 — Setup: Jupyter and pandas

Module 02 teaches data manipulation with pandas. This script just confirms your
environment is ready and shows the conventions used throughout the module.

Run this file:   uv run 02_working_with_data/00_setup/00_setup.py
Launch Jupyter:  uv run jupyter notebook
"""
import sys

print("=== Environment Check ===")
print(f"Python: {sys.version.split()[0]}")

import pandas as pd      # conventional alias: pd
import numpy as np       # conventional alias: np

print(f"pandas: {pd.__version__}")
print(f"numpy:  {np.__version__}")

# the two core pandas objects
print("\n=== Hello, pandas ===")
s = pd.Series([35000, 650, 8500], name="unit_price")
print(s)

df = pd.DataFrame({"product": ["Laptop Pro", "Wireless Mouse"], "price": [35000, 650]})
print(df)

# display options — useful inside Jupyter notebooks
print("\n=== Display options (handy in Jupyter) ===")
pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)
print("Set max_columns=20 and width=120.")

print("\nReady! Next: 01_pandas/01_introduction.py")
print("Tip: open the workshop notebook with  uv run jupyter notebook")
