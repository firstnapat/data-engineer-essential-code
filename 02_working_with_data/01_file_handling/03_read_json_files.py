import json
import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
JSON_FILE = os.path.join(DATASETS, "products.json")

print("--- Load JSON ---")
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Store:         {data['store']}")
print(f"Last updated:  {data['last_updated']}")
print(f"Products:      {len(data['products'])}")

print("\n--- Access Nested Data ---")
for product in data["products"][:3]:
    print(f"  [{product['id']}] {product['name']:<22} ฿{product['unit_price']:>6,}")

print("\n--- Filter Products ---")
electronics = [p for p in data["products"] if p["category"] == "Electronics"]
print(f"Electronics ({len(electronics)} items):")
for p in electronics:
    print(f"  {p['name']:<22} ฿{p['unit_price']:>6,}  stock={p['stock']}")

print("\n--- Serialize Back to String ---")
summary = {
    "store": data["store"],
    "product_count": len(data["products"]),
    "categories": sorted(set(p["category"] for p in data["products"])),
    "total_stock_value": sum(p["unit_price"] * p["stock"] for p in data["products"]),
}
print(json.dumps(summary, indent=2, ensure_ascii=False))

print("\n--- Write JSON ---")
output = "/tmp/products_summary.json"
with open(output, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"Written to {output}")

print("\n--- Parse JSON String ---")
json_str = '{"name": "Alice", "skills": ["Python", "SQL", "Spark"]}'
parsed = json.loads(json_str)
print(f"name: {parsed['name']}, skills: {parsed['skills']}")
