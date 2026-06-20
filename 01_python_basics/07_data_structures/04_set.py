print("--- Creating Sets ---")
s = {1, 2, 3, 4, 5}
with_dupes = {1, 2, 2, 3, 3, 3}    # duplicates removed automatically
from_list = set([1, 1, 2, 2, 3])
empty = set()                        # {} creates a dict, not a set!
print(f"set: {s}")
print(f"with_dupes -> {with_dupes}")
print(f"from_list  -> {from_list}")

print("\n--- Adding / Removing ---")
s = {1, 2, 3}
s.add(4);       print(f"add(4):     {s}")
s.discard(2);   print(f"discard(2): {s}  (no error if missing)")
s.remove(3);    print(f"remove(3):  {s}")

print("\n--- Set Operations ---")
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}
print(f"a:                {a}")
print(f"b:                {b}")
print(f"union      a | b: {a | b}")
print(f"intersect  a & b: {a & b}")
print(f"difference a - b: {a - b}")
print(f"symmetric  a ^ b: {a ^ b}")

print("\n--- Subset / Superset ---")
c = {1, 2, 3}
d = {1, 2, 3, 4, 5}
print(f"c.issubset(d):    {c.issubset(d)}")
print(f"d.issuperset(c):  {d.issuperset(c)}")
print(f"c.isdisjoint({{6,7}}): {c.isdisjoint({6, 7})}")

print("\n--- Common Use Case: Remove Duplicates ---")
original = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
unique_unordered = list(set(original))
unique_ordered = list(dict.fromkeys(original))   # preserves insertion order
print(f"original:          {original}")
print(f"unique (unordered):{unique_unordered}")
print(f"unique (ordered):  {unique_ordered}")

print("\n--- Fast Membership Testing ---")
valid_categories = {"Electronics", "Furniture", "Clothing", "Accessories"}
test_values = ["Laptop", "Electronics", "Chair", "Clothing"]
for val in test_values:
    status = "valid category" if val in valid_categories else "not a category"
    print(f"  '{val}': {status}")
