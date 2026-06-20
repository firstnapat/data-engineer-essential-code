print("--- Single Return ---")
def square(n):
    return n ** 2

print(f"square(5) = {square(5)}")

print("\n--- Multiple Return Values (tuple unpacking) ---")
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(f"min={low}, max={high}")

def get_stats(numbers):
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "average": sum(numbers) / len(numbers),
    }

for key, val in get_stats([10, 20, 30, 40, 50]).items():
    print(f"  {key}: {val}")

print("\n--- Early Return ---")
def safe_divide(a, b):
    if b == 0:
        return None
    return a / b

print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")
print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")

print("\n--- Generator (yield) ---")
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(f"Fibonacci: {list(fibonacci(10))}")

print("\n--- Function Returning Function (closure) ---")
def make_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)
print(f"double(5)={double(5)}, triple(5)={triple(5)}")
