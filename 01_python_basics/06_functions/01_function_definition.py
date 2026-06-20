print("--- Basic Function ---")
def greet():
    print("Hello, World!")

greet()

print("\n--- With Docstring ---")
def calculate_area(width, height):
    """Calculate the area of a rectangle."""
    return width * height

print(f"Area: {calculate_area(5, 3)}")
print(f"Docstring: {calculate_area.__doc__}")

print("\n--- Functions Are First-Class Objects ---")
def add(a, b): return a + b
def subtract(a, b): return a - b

for op in [add, subtract]:
    print(f"  {op.__name__}(10, 3) = {op(10, 3)}")

print("\n--- Lambda Functions ---")
square = lambda x: x ** 2
double = lambda x: x * 2
print(f"square(5)={square(5)}, double(7)={double(7)}")

people = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}, {"name": "Charlie", "age": 22}]
sorted_people = sorted(people, key=lambda p: p["age"])
print(f"sorted by age: {[p['name'] for p in sorted_people]}")

print("\n--- Scope ---")
global_var = "I am global"

def show_scope():
    local_var = "I am local"
    print(f"  Inside: global_var='{global_var}', local_var='{local_var}'")

show_scope()
print(f"Outside: global_var='{global_var}'")
# local_var is not accessible here
