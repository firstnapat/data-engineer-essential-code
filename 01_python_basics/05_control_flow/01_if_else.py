print("--- If / Elif / Else ---")
score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score} -> Grade: {grade}")

print("\n--- Ternary (one-liner) ---")
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Age {age} is: {status}")

print("\n--- Nested If ---")
temperature = 28
humidity = 80

if temperature > 30:
    weather = "Hot and Humid" if humidity > 70 else "Hot and Dry"
elif temperature > 20:
    weather = "Comfortable"
else:
    weather = "Cold"

print(f"{temperature}°C, {humidity}% humidity -> {weather}")

print("\n--- and / or in conditions ---")
username, password = "admin", "secret123"
if username == "admin" and password == "secret123":
    print("Login successful!")
else:
    print("Invalid credentials.")

print("\n--- Truthy / Falsy ---")
values = [0, 1, "", "hello", None, [], [1], {}, {"a": 1}]
for val in values:
    print(f"  {str(val):15} -> {'truthy' if val else 'falsy'}")
