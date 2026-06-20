name = "Alice"
age = 25
height = 1.65
is_student = True
nothing = None

print("--- Basic Variables ---")
print(f"Name: {name}, Age: {age}, Height: {height}")
print(f"Is student: {is_student}, Nothing: {nothing}")
print(f"type(name): {type(name)}, type(age): {type(age)}")

print("\n--- Multiple Assignment ---")
x, y, z = 10, 20, 30
print(f"x={x}, y={y}, z={z}")

x, y = y, x  # swap without temp variable
print(f"After swap: x={x}, y={y}")

a = b = c = 0
print(f"a={a}, b={b}, c={c}")

print("\n--- Naming Conventions ---")
user_name = "snake_case"  # preferred in Python
MAX_CONNECTIONS = 100  # constants in UPPER_SNAKE_CASE
_internal = "prefix _ = internal"
print(user_name, MAX_CONNECTIONS, _internal)
