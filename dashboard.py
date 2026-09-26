import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = load_data()


# ============================================================
# TITLE
# ============================================================

st.title("📊 Sales Analytics Dashboard")

st.markdown(
    "Interactive visualization of sales, profit, products, "
    "categories, and regions."
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)


# Apply filters
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = filtered_df["Order_ID"].nunique()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"₹{total_profit:,.0f}"
)

col3.metric(
    "📦 Total Quantity",
    f"{total_quantity:,}"
)

col4.metric(
    "🧾 Total Orders",
    f"{total_orders:,}"
)


st.divider()


# ============================================================
# MONTHLY SALES TREND
# ============================================================

monthly_sales = (
    filtered_df
    .assign(
        Month=filtered_df["Date"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("Month", as_index=False)["Sales"]
    .sum()
)


fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="📅 Monthly Sales Trend"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales (₹)"
)

st.plotly_chart(
    fig_monthly,
    width="stretch"
)


# ============================================================
# CATEGORY AND REGION CHARTS
# ============================================================

col1, col2 = st.columns(2)


# -----------------------------
# Category Sales
# -----------------------------
with col1:
    category_sales = filtered_df.groupby("Category")["Sales"].sum()
    category_sales = category_sales.reset_index()
    category_sales = category_sales.sort_values(
        by="Sales",
        ascending=False
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="🛍️ Sales by Category"
    )

    fig_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales (₹)"
    )

    st.plotly_chart(fig_category, width="stretch")

# -----------------------------
# Regional Sales
# -----------------------------
with col2:
    regional_sales = filtered_df.groupby("Region")["Sales"].sum()
    regional_sales = regional_sales.reset_index()
    regional_sales = regional_sales.sort_values(
        by="Sales",
        ascending=False
    )

    fig_region = px.bar(
        regional_sales,
        x="Region",
        y="Sales",
        title="🌎 Sales by Region"
    )

    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Sales (₹)"
    )

    st.plotly_chart(fig_region, width="stretch")


# ============================================================
# PRODUCT SALES
# ============================================================
product_sales = filtered_df.groupby("Product")["Sales"].sum()
product_sales = product_sales.reset_index()
product_sales = product_sales.sort_values(
    by="Sales",
    ascending=False
)

fig_product = px.bar(
    product_sales,
    x="Product",
    y="Sales",
    title="🏆 Sales by Product"
)

fig_product.update_layout(
    xaxis_title="Product",
    yaxis_title="Sales (₹)"
)

st.plotly_chart(fig_product, width="stretch")

# ============================================================
# SALES VS PROFIT
# ============================================================

fig_profit = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    size="Quantity",
    hover_data=["Product", "Region"],
    title="💹 Sales vs Profit"
)

fig_profit.update_layout(
    xaxis_title="Sales (₹)",
    yaxis_title="Profit (₹)"
)

st.plotly_chart(
    fig_profit,
    width="stretch"
)


# ============================================================
# DATA TABLE
# ============================================================

with st.expander("📋 View Sales Data"):

    st.dataframe(
        filtered_df,
        width="stretch"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CodeAlpha Data Visualization Project | "
    "Built with Python, Pandas, Plotly and Streamlit"
)