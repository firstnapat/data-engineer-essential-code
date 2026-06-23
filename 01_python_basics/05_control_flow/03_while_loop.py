# basic while — sell units until stock runs out
print("--- Basic While ---")
stock = 5
while stock > 0:
    print(f"  sell 1 unit, stock left = {stock - 1}")
    stock -= 1

# while True + break — keep doubling an order until it crosses a threshold
print("\n--- While with break ---")
units = 1
while True:
    print(f"  {units}", end=" ")
    units *= 2
    if units > 50:
        break
print()

# while + continue — print only odd order IDs
print("\n--- While with continue ---")
order_id = 0
while order_id < 10:
    order_id += 1
    if order_id % 2 == 0:
        continue            # skip even IDs
    print(order_id, end=" ")
print()

# retry pattern — common when an ingestion API call fails
print("\n--- Retry Pattern (API ingestion) ---")
max_retries = 3
attempt = 0
success = False

while attempt < max_retries:
    attempt += 1
    print(f"  Fetching orders... attempt {attempt}")
    if attempt == 2:        # simulate success on the 2nd try
        success = True
        break

print("Fetched!" if success else "Gave up after max retries.")

# loop until a sentinel value — stop processing a stream at 'EOF'
print("\n--- Process Until Sentinel ---")
stream = ["100", "250", "EOF", "999"]
total_revenue = 0
for token in stream:
    if token == "EOF":
        print("End of stream.")
        break
    total_revenue += int(token)
print(f"Total revenue: {total_revenue}")
