# helper: run a function and report the error type if it raises
def safe_run(label, fn):
    try:
        result = fn()
        print(f"  {label}: OK -> {result}")
    except Exception as e:
        print(f"  {label}: {type(e).__name__}: {e}")

# NameError — using a variable that was never defined
print("--- NameError: variable used before assignment ---")
safe_run("undefined var", lambda: undefined_variable)  # noqa: F821

# TypeError — operation on the wrong type
print("\n--- TypeError ---")
safe_run("str + int",   lambda: "5" + 5)
safe_run("len(int)",    lambda: len(42))
safe_run("None + int",  lambda: None + 1)

# ValueError — right type, wrong value
print("\n--- ValueError ---")
safe_run("int('abc')", lambda: int("abc"))
safe_run("int('')",    lambda: int(""))

# IndexError — list index out of range
print("\n--- IndexError ---")
lst = [1, 2, 3]
safe_run("lst[10]",  lambda: lst[10])
safe_run("lst[-10]", lambda: lst[-10])

# KeyError — dict key does not exist
print("\n--- KeyError ---")
d = {"a": 1}
safe_run("d['missing']", lambda: d["missing"])

# AttributeError — attribute/method does not exist
print("\n--- AttributeError ---")
safe_run("str.nonexistent", lambda: "hello".nonexistent_method())
safe_run("int.upper()",     lambda: (42).upper())

# ZeroDivisionError — division by zero
print("\n--- ZeroDivisionError ---")
safe_run("10 / 0",  lambda: 10 / 0)
safe_run("10 // 0", lambda: 10 // 0)

# RecursionError — recursion too deep
print("\n--- RecursionError ---")
def infinite(n): return infinite(n + 1)
try:
    infinite(0)
except RecursionError:
    print("  RecursionError: maximum recursion depth exceeded")

# FileNotFoundError — opening a file that does not exist
print("\n--- FileNotFoundError ---")
try:
    open("does_not_exist.txt")
except FileNotFoundError as e:
    print(f"  FileNotFoundError: {e}")
