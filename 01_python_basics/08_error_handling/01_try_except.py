# basic try / except
print("--- Basic Try / Except ---")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# catching multiple exception types
print("\n--- Catching Multiple Exceptions ---")
def parse_number(value):
    try:
        return int(value)
    except ValueError:
        print(f"  ValueError: '{value}' is not a valid integer")
        return None
    except TypeError:
        print(f"  TypeError: cannot convert {type(value).__name__} to int")
        return None

parse_number("123")
parse_number("abc")
parse_number(None)

# accessing the exception object (as e)
print("\n--- Except with Exception Info ---")
try:
    data = {"key": "value"}
    print(data["missing_key"])
except KeyError as e:
    print(f"Key not found: {e} (type: {type(e).__name__})")

# else and finally clauses
print("\n--- else and finally ---")
def safe_open(filename):
    try:
        f = open(filename)
        content = f.read()
        f.close()
    except FileNotFoundError:
        print(f"  '{filename}' not found")
        return None
    else:
        print(f"  Read {len(content)} chars")
        return content
    finally:
        print("  finally: always runs")

safe_open("nonexistent.txt")

# raising exceptions
print("\n--- Raising Exceptions ---")
def validate_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Age must be int, got {type(age).__name__}")
    if not 0 <= age <= 150:
        raise ValueError(f"Age {age} out of valid range (0-150)")
    return True

try:
    validate_age(-5)
except ValueError as e:
    print(f"ValueError: {e}")

try:
    validate_age("25")
except TypeError as e:
    print(f"TypeError: {e}")

# custom exception class
print("\n--- Custom Exception ---")
class DataValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        super().__init__(f"Field '{field}': {message}")

try:
    raise DataValidationError("email", "invalid format")
except DataValidationError as e:
    print(f"DataValidationError — field='{e.field}', msg='{e}'")
