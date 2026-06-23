import os
import matplotlib

# use a non-interactive backend so the script runs without a display / GUI
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
OUTDIR = "/tmp/viz"
os.makedirs(OUTDIR, exist_ok=True)

df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])
df["month"] = df["date"].dt.strftime("%Y-%m")

# bar chart — revenue by category
print("=== Bar Chart: Revenue by Category ===")
by_cat = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
by_cat.plot(kind="bar", ax=ax, color="steelblue")
ax.set_title("Total Revenue by Category")
ax.set_ylabel("Revenue (THB)")
plt.tight_layout()
fig.savefig(f"{OUTDIR}/revenue_by_category.png")
plt.close(fig)
print(f"saved -> {OUTDIR}/revenue_by_category.png")

# line chart — monthly revenue trend
print("\n=== Line Chart: Monthly Trend ===")
monthly = df.groupby("month")["revenue"].sum()
fig, ax = plt.subplots(figsize=(8, 5))
monthly.plot(kind="line", marker="o", ax=ax, color="darkgreen")
ax.set_title("Monthly Revenue Trend")
ax.set_ylabel("Revenue (THB)")
plt.tight_layout()
fig.savefig(f"{OUTDIR}/monthly_trend.png")
plt.close(fig)
print(f"saved -> {OUTDIR}/monthly_trend.png")

# histogram — distribution of transaction revenue
print("\n=== Histogram: Revenue Distribution ===")
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df["revenue"], bins=15, color="coral", edgecolor="black")
ax.set_title("Distribution of Transaction Revenue")
ax.set_xlabel("Revenue (THB)")
plt.tight_layout()
fig.savefig(f"{OUTDIR}/revenue_distribution.png")
plt.close(fig)
print(f"saved -> {OUTDIR}/revenue_distribution.png")

# seaborn — prettier statistical plots
print("\n=== Seaborn: Boxplot by Region ===")
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x="region", y="revenue", ax=ax)
ax.set_title("Revenue Spread by Region")
plt.tight_layout()
fig.savefig(f"{OUTDIR}/revenue_by_region_box.png")
plt.close(fig)
print(f"saved -> {OUTDIR}/revenue_by_region_box.png")

# seaborn — heatmap of a pivot table
print("\n=== Seaborn: Heatmap (region x category) ===")
pivot = df.pivot_table(values="revenue", index="region", columns="category",
                       aggfunc="sum", fill_value=0)
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
ax.set_title("Revenue: Region x Category")
plt.tight_layout()
fig.savefig(f"{OUTDIR}/region_category_heatmap.png")
plt.close(fig)
print(f"saved -> {OUTDIR}/region_category_heatmap.png")

print(f"\nAll charts written to {OUTDIR}/")
