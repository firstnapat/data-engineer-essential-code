print("--- Creating Tuples ---")
point = (3, 4)
single = (42,)        # trailing comma required for single-element
rgb = (255, 128, 0)
print(f"point={point}, type={type(point)}")
print(f"single-element: {single}, type={type(single)}")

print("\n--- Accessing ---")
coords = (10, 20, 30)
print(f"coords[0]={coords[0]}, coords[-1]={coords[-1]}, slice={coords[1:]}")

print("\n--- Tuple Unpacking ---")
x, y = (3, 4)
print(f"x={x}, y={y}")

first, *middle, last = (1, 2, 3, 4, 5)
print(f"first={first}, middle={middle}, last={last}")

a, b = 10, 20
a, b = b, a    # swap via tuple
print(f"After swap: a={a}, b={b}")

print("\n--- Immutable ---")
t = (1, 2, 3)
try:
    t[0] = 99
except TypeError as e:
    print(f"Cannot modify tuple: {e}")

print("\n--- Tuples as Dict Keys (lists cannot be) ---")
locations = {(13.75, 100.52): "Bangkok", (18.79, 98.98): "Chiang Mai"}
print(f"Bangkok coords: {(13.75, 100.52)} -> {locations[(13.75, 100.52)]}")

print("\n--- namedtuple ---")
from collections import namedtuple

Person = namedtuple("Person", ["name", "age", "city"])
alice = Person("Alice", 25, "Bangkok")
print(f"alice:      {alice}")
print(f"alice.name: {alice.name}, alice.age: {alice.age}")
