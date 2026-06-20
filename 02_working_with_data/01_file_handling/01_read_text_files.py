import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
FILEPATH = os.path.join(DATASETS, "sample.txt")

print("--- Read Entire File ---")
with open(FILEPATH, "r", encoding="utf-8") as f:
    content = f.read()
print(content)
print(f"Total characters: {len(content)}")

print("--- Read Line by Line ---")
with open(FILEPATH, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(f"  Line {i:2}: {line.rstrip()}")

print("\n--- readlines() -> list ---")
with open(FILEPATH, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
print(f"First line:  {lines[0].strip()}")
non_empty = [l.strip() for l in lines if l.strip()]
print(f"Non-empty lines: {len(non_empty)}")

print("\n--- Write to File ---")
output = "/tmp/output.txt"
with open(output, "w", encoding="utf-8") as f:
    f.write("Line 1\n")
    f.writelines(["Line 2\n", "Line 3\n"])
print(f"Written to {output}")

print("\n--- Append to File ---")
with open(output, "a", encoding="utf-8") as f:
    f.write("Line 4 (appended)\n")

with open(output) as f:
    print(f.read())
