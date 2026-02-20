import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("enriched_data.csv")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

st.title("NordTech Dashboard")

cats = st.sidebar.multiselect("Category", df["Product_Category"].unique(), default=df["Product_Category"].unique())
df = df[df["Product_Category"].isin(cats)]

st.metric("Revenue", f"{df['gross_revenue_eur'].sum():,.0f} EUR")
st.metric("Refund", f"{df['refund_amount'].sum():,.0f} EUR")

weekly = df.groupby(df["order_date"].dt.to_period("W")).sum(numeric_only=True).reset_index()
weekly["order_date"]=weekly["order_date"].astype(str)

fig = px.line(weekly, x="order_date", y="gross_revenue_eur", title="Revenue over time")
st.plotly_chart(fig)

st.dataframe(df)
