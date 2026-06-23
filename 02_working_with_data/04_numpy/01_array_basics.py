import numpy as np

# creating arrays
print("=== Creating Arrays ===")
a = np.array([1, 2, 3, 4, 5])
print(f"from list:  {a}")
print(f"arange:     {np.arange(0, 10, 2)}")        # start, stop, step
print(f"zeros:      {np.zeros(4)}")
print(f"ones:       {np.ones(3, dtype=int)}")
print(f"linspace:   {np.linspace(0, 1, 5)}")        # 5 evenly spaced points
print(f"full:       {np.full(3, 7)}")

# dtype — arrays are homogeneous
print("\n=== Data Types ===")
print(f"a.dtype:               {a.dtype}")
print(f"float array dtype:     {np.array([1.0, 2.0]).dtype}")
print(f"cast to float:         {a.astype(float)}")

# shape and reshape
print("\n=== Shape & Reshape ===")
m = np.arange(1, 13).reshape(3, 4)
print(m)
print(f"shape: {m.shape}, ndim: {m.ndim}, size: {m.size}")
print(f"transpose:\n{m.T}")
print(f"flatten: {m.flatten()}")

# indexing and slicing
print("\n=== Indexing & Slicing ===")
print(f"a[0]={a[0]}, a[-1]={a[-1]}, a[1:4]={a[1:4]}")
print(f"m[0, 2] (row 0, col 2): {m[0, 2]}")
print(f"m[:, 1] (column 1):     {m[:, 1]}")
print(f"m[1, :] (row 1):        {m[1, :]}")

# boolean masking — filter by condition
print("\n=== Boolean Masking ===")
data = np.array([12, 45, 7, 88, 23, 60])
print(f"data:          {data}")
print(f"data > 30:     {data > 30}")
print(f"data[data>30]: {data[data > 30]}")
print(f"count > 30:    {(data > 30).sum()}")
