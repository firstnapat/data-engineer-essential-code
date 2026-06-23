# creating sets — duplicates removed automatically
print("--- Creating Sets ---")
skus_today = {"P001", "P002", "P002", "P006"}    # duplicates removed automatically
from_list = set(["P001", "P001", "P002"])
empty = set()                                      # {} makes a dict, not a set!
print(f"skus_today: {skus_today}")
print(f"from_list:  {from_list}")

# adding / removing — add, discard, remove
print("\n--- Adding / Removing ---")
cart = {"P001", "P002", "P006"}
cart.add("P009");      print(f"add:     {cart}")
cart.discard("P002");  print(f"discard: {cart}  (no error if missing)")
cart.remove("P006");   print(f"remove:  {cart}")

# set operations — compare what sold today vs yesterday
print("\n--- Set Operations ---")
today = {"P001", "P002", "P006", "P009"}
yesterday = {"P006", "P009", "P011", "P012"}
print(f"today:            {today}")
print(f"yesterday:        {yesterday}")
print(f"either day  | :   {today | yesterday}")
print(f"both days   & :   {today & yesterday}")
print(f"only today  - :   {today - yesterday}")
print(f"one day only ^:   {today ^ yesterday}")

# subset / superset / disjoint
print("\n--- Subset / Superset ---")
ordered = {"P001", "P002"}
catalog = {"P001", "P002", "P006", "P009"}
print(f"ordered.issubset(catalog):    {ordered.issubset(catalog)}")
print(f"catalog.issuperset(ordered):  {catalog.issuperset(ordered)}")
print(f"ordered.isdisjoint({{'P099'}}): {ordered.isdisjoint({'P099'})}")

# use case: distinct values from a column of order rows
print("\n--- Common Use Case: Remove Duplicates ---")
region_column = ["Bangkok", "Chiang Mai", "Bangkok", "Phuket", "Bangkok", "Chiang Mai"]
distinct_unordered = list(set(region_column))
distinct_ordered = list(dict.fromkeys(region_column))   # preserves first-seen order
print(f"raw column:         {region_column}")
print(f"distinct (set):     {distinct_unordered}")
print(f"distinct (ordered): {distinct_ordered}")

# use case: fast membership testing — validate a category column
print("\n--- Fast Membership Testing ---")
valid_categories = {"Electronics", "Furniture", "Clothing", "Accessories"}
incoming = ["Electronics", "Toys", "Clothing", "Gadgets"]
for value in incoming:
    status = "valid" if value in valid_categories else "REJECT"
    print(f"  {value:12} -> {status}")
