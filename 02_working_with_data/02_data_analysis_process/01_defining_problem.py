"""
Step 1: Defining the Problem or Question
=========================================
Before writing any code, answer these questions:

  1. What business question are we trying to answer?
  2. What does "success" look like for this analysis?
  3. What data do we need, and do we have it?
  4. Who will consume the results?

Example: TechData Store Q1 2024 Sales Analysis
-----------------------------------------------
  Business Question : Which product categories and regions drive the most revenue?
  Success Criteria  : A ranked breakdown by category and region + time trend
  Data Available    : sales.csv (54 transactions, Jan–Mar 2024)
  Consumers         : Sales manager, monthly review meeting
"""

# Translate the problem into concrete analysis tasks
analysis_plan = {
    "question": "Which categories and regions drive the most revenue in Q1 2024?",
    "tasks": [
        "Calculate total revenue by category",
        "Calculate total revenue by region",
        "Identify top-selling products",
        "Spot monthly revenue trend (Jan vs Feb vs Mar)",
    ],
    "output": "Summary table + 3 charts",
    "dataset": "datasets/sales.csv",
}

for key, value in analysis_plan.items():
    if isinstance(value, list):
        print(f"{key}:")
        for item in value:
            print(f"  - {item}")
    else:
        print(f"{key}: {value}")
