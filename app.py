import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Business Analytics Dashboard",
                   page_icon="📊", layout="wide")

st.title("📊 Interactive Business Analytics Dashboard")
st.write("Revenue, Users and Customer Churn Analysis")

# Generate sample dataset
np.random.seed(42)
n = 500

df = pd.DataFrame({
    "Date": pd.date_range("2025-01-01", periods=n, freq="D"),
    "Region": np.random.choice(["North", "South", "East", "West"], n),
    "Category": np.random.choice(["Electronics", "Fashion", "Food", "Services"], n),
    "Revenue": np.random.randint(500, 10000, n),
    "Users": np.random.randint(1, 5, n),
    "Churned": np.random.choice([0, 1], n, p=[0.8, 0.2]),
    "Ticket_Size": np.random.randint(100, 2000, n)
})

# Filters
st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region", df["Region"].unique(),
    default=list(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category", df["Category"].unique(),
    default=list(df["Category"].unique())
)

dates = st.sidebar.date_input(
    "Select Date Range",
    value=(df["Date"].min().date(), df["Date"].max().date())
)

filtered = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

if len(dates) == 2:
    filtered = filtered[
        (filtered["Date"].dt.date >= dates[0]) &
        (filtered["Date"].dt.date <= dates[1])
    ]

if filtered.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# KPI Cards
revenue = filtered["Revenue"].sum()
active_users = filtered.loc[filtered["Churned"] == 0, "Users"].sum()
churn = filtered["Churned"].mean() * 100
ticket = filtered["Ticket_Size"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"₹{revenue:,.0f}")
c2.metric("Active Users", f"{active_users:,}")
c3.metric("Churn Rate", f"{churn:.2f}%")
c4.metric("Avg Ticket Size", f"₹{ticket:,.2f}")

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Revenue by Region")
    fig = px.bar(filtered, x="Region", y="Revenue",
                 color="Region", title="Regional Revenue")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Revenue by Category")
    fig2 = px.pie(filtered, names="Category", values="Revenue",
                  title="Category Revenue Distribution")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Revenue Trend")
monthly = filtered.copy()
monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)
trend = monthly.groupby("Month", as_index=False)["Revenue"].sum()

fig3 = px.line(trend, x="Month", y="Revenue",
               markers=True, title="Monthly Revenue Trend")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Dashboard Dataset")
st.dataframe(filtered, use_container_width=True)

st.success("Interactive Dashboard Loaded Successfully!")
