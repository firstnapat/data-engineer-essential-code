# helper: run a function and report the error type if it raises
def safe_run(label, fn):
    try:
        result = fn()
        print(f"  {label}: OK -> {result}")
    except Exception as e:
        print(f"  {label}: {type(e).__name__}: {e}")

# NameError — referencing a column/variable that was never defined
print("--- NameError: variable used before assignment ---")
safe_run("unit_prince typo", lambda: unit_prince)  # noqa: F821  (misspelled 'unit_price')

# TypeError — operation on the wrong type (raw CSV fields are strings!)
print("\n--- TypeError ---")
safe_run("'3' + 35000",  lambda: "3" + 35000)      # quantity str + price int
safe_run("len(50)",      lambda: len(50))
safe_run("None + 1",     lambda: None + 1)         # a missing field

# ValueError — right type, wrong value
print("\n--- ValueError ---")
safe_run("int('three')", lambda: int("three"))     # bad quantity cell
safe_run("int('')",      lambda: int(""))          # empty cell

# IndexError — list index out of range
print("\n--- IndexError ---")
order_line = ["P001", 3, 35000]
safe_run("order_line[5]",  lambda: order_line[5])
safe_run("order_line[-9]", lambda: order_line[-9])

# KeyError — dict key / record field does not exist
print("\n--- KeyError ---")
product = {"sku": "P001"}
safe_run("product['price']", lambda: product["price"])

# AttributeError — attribute/method does not exist
print("\n--- AttributeError ---")
safe_run("'P001'.to_upper()", lambda: "P001".to_upper())   # it's .upper()
safe_run("(50).upper()",      lambda: (50).upper())

# ZeroDivisionError — averaging revenue over zero orders
print("\n--- ZeroDivisionError ---")
safe_run("105000 / 0",  lambda: 105000 / 0)
safe_run("105000 // 0", lambda: 105000 // 0)

# RecursionError — recursion too deep
print("\n--- RecursionError ---")
def keep_paging(page): return keep_paging(page + 1)   # forgot the stop condition
try:
    keep_paging(0)
except RecursionError:
    print("  RecursionError: maximum recursion depth exceeded")

# FileNotFoundError — opening a dataset that does not exist
print("\n--- FileNotFoundError ---")
try:
    open("orders_2099.csv")
except FileNotFoundError as e:
    print(f"  FileNotFoundError: {e}")
