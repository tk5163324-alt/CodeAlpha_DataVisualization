import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
DATA_FILE = Path("data/sales_data.csv")
OUTPUT_DIR = Path("outputs")

OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_FILE)

df["Date"] = pd.to_datetime(df["Date"])

print("\n===== SALES DATASET =====")
print(df.head())

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATES =====")
print(df.duplicated().sum())

# -----------------------------
# Basic statistics
# -----------------------------
print("\n===== SUMMARY STATISTICS =====")
print(df[["Sales", "Quantity", "Profit"]].describe())

print("\n===== TOTAL SALES =====")
print(f"₹{df['Sales'].sum():,.2f}")

print("\n===== TOTAL PROFIT =====")
print(f"₹{df['Profit'].sum():,.2f}")

print("\n===== TOTAL QUANTITY =====")
print(df["Quantity"].sum())

# -----------------------------
# Monthly sales
# -----------------------------
df["Month"] = df["Date"].dt.to_period("M").astype(str)

monthly_sales = df.groupby("Month")["Sales"].sum()

print("\n===== MONTHLY SALES =====")
print(monthly_sales)

# -----------------------------
# Category analysis
# -----------------------------
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

print("\n===== SALES BY CATEGORY =====")
print(category_sales)

# -----------------------------
# Regional analysis
# -----------------------------
regional_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

print("\n===== SALES BY REGION =====")
print(regional_sales)

# -----------------------------
# Product analysis
# -----------------------------
product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)

print("\n===== SALES BY PRODUCT =====")
print(product_sales)

# -----------------------------
# Visualizations
# -----------------------------

# 1. Monthly Sales
plt.figure(figsize=(10, 6))
monthly_sales.plot(marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_sales.png")
plt.close()

# 2. Category Sales
plt.figure(figsize=(9, 6))
category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "category_sales.png")
plt.close()

# 3. Regional Sales
plt.figure(figsize=(8, 6))
regional_sales.plot(kind="bar")
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales (₹)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "regional_sales.png")
plt.close()

# 4. Profit Analysis
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="Sales",
    y="Profit",
    hue="Category",
    s=100
)
plt.title("Sales vs Profit")
plt.xlabel("Sales (₹)")
plt.ylabel("Profit (₹)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "profit_analysis.png")
plt.close()

# 5. Product Sales
plt.figure(figsize=(10, 6))
product_sales.plot(kind="bar")
plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "product_sales.png")
plt.close()

# -----------------------------
# Key insights
# -----------------------------
print("\n===== KEY INSIGHTS =====")

print(
    f"Highest sales category: "
    f"{category_sales.idxmax()} "
    f"(₹{category_sales.max():,.2f})"
)

print(
    f"Highest sales region: "
    f"{regional_sales.idxmax()} "
    f"(₹{regional_sales.max():,.2f})"
)

print(
    f"Highest selling product: "
    f"{product_sales.idxmax()} "
    f"(₹{product_sales.max():,.2f})"
)

print(
    f"Highest monthly sales: "
    f"{monthly_sales.idxmax()} "
    f"(₹{monthly_sales.max():,.2f})"
)

print("\nVisualization files created successfully in outputs/")