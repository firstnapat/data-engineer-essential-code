# basic try / except — a zero-item order slips into a calculation
print("--- Basic Try / Except ---")
try:
    avg_price = 35000 / 0       # zero items -> division by zero
except ZeroDivisionError:
    print("Cannot divide by zero items!")

# catching multiple exception types — parse a raw quantity field
print("\n--- Catching Multiple Exceptions ---")
def parse_quantity(value):
    try:
        return int(value)
    except ValueError:
        print(f"  ValueError: '{value}' is not a valid quantity")
        return None
    except TypeError:
        print(f"  TypeError: cannot convert {type(value).__name__} to int")
        return None

parse_quantity("3")
parse_quantity("three")
parse_quantity(None)

# accessing the exception object (as e) — missing field in a record
print("\n--- Except with Exception Info ---")
try:
    product = {"sku": "P001", "name": "Laptop Pro"}
    print(product["price"])
except KeyError as e:
    print(f"Missing field: {e} (type: {type(e).__name__})")

# else and finally — load a data file safely
print("\n--- else and finally ---")
def load_orders(filename):
    try:
        f = open(filename)
        content = f.read()
        f.close()
    except FileNotFoundError:
        print(f"  '{filename}' not found")
        return None
    else:
        print(f"  Loaded {len(content)} chars")
        return content
    finally:
        print("  finally: always runs (close connections here)")

load_orders("orders_missing.csv")

# raising exceptions — validate an order quantity
print("\n--- Raising Exceptions ---")
def validate_quantity(qty):
    if not isinstance(qty, int):
        raise TypeError(f"Quantity must be int, got {type(qty).__name__}")
    if qty <= 0:
        raise ValueError(f"Quantity {qty} must be positive")
    return True

try:
    validate_quantity(-2)
except ValueError as e:
    print(f"ValueError: {e}")

try:
    validate_quantity("3")
except TypeError as e:
    print(f"TypeError: {e}")

# custom exception class — a domain-specific validation error
print("\n--- Custom Exception ---")
class ProductValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        super().__init__(f"Field '{field}': {message}")

try:
    raise ProductValidationError("unit_price", "must be greater than 0")
except ProductValidationError as e:
    print(f"ProductValidationError — field='{e.field}', msg='{e}'")
