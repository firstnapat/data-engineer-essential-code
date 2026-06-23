import numpy as np
import os
import csv

# vectorization — element-wise math without Python loops
print("=== Vectorization ===")
quantity = np.array([3, 15, 2, 4, 10])
unit_price = np.array([35000, 650, 8500, 15000, 2800])
revenue = quantity * unit_price          # element-wise, no loop
print(f"quantity:   {quantity}")
print(f"unit_price: {unit_price}")
print(f"revenue:    {revenue}")

# broadcasting — operate across mismatched shapes
print("\n=== Broadcasting ===")
prices = np.array([100, 200, 300])
print(f"prices + 10:      {prices + 10}")          # scalar broadcast
print(f"prices * 1.07:    {(prices * 1.07).round(2)}")
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"matrix + [10,20,30]:\n{matrix + np.array([10, 20, 30])}")

# aggregations — with axis
print("\n=== Aggregations ===")
print(f"sum:  {revenue.sum()}")
print(f"mean: {revenue.mean():.2f}")
print(f"std:  {revenue.std():.2f}")
print(f"min/max: {revenue.min()} / {revenue.max()}")
print(f"matrix sum axis=0 (columns): {matrix.sum(axis=0)}")
print(f"matrix sum axis=1 (rows):    {matrix.sum(axis=1)}")

# math ufuncs (universal functions)
print("\n=== Math Functions ===")
x = np.array([1, 4, 9, 16])
print(f"sqrt:  {np.sqrt(x)}")
print(f"log:   {np.log(x).round(3)}")
print(f"cumsum:{np.cumsum(x)}")
print(f"clip(2, 10): {np.clip(x, 2, 10)}")

# practical: load sales revenue into a numpy array and analyze
print("\n=== Practical: Revenue Stats from sales.csv ===")
csv_path = os.path.join(os.path.dirname(__file__), "../../datasets/sales.csv")
with open(csv_path) as f:
    rows = list(csv.DictReader(f))
rev = np.array([float(r["revenue"]) for r in rows])
print(f"transactions: {rev.size}")
print(f"total:        {rev.sum():,.0f}")
print(f"average:      {rev.mean():,.2f}")
print(f"median:       {np.median(rev):,.2f}")
print(f"90th pct:     {np.percentile(rev, 90):,.2f}")
print(f"above avg:    {(rev > rev.mean()).sum()} transactions")
