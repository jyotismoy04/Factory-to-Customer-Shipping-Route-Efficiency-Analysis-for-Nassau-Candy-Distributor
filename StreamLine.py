
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Shipping Efficiency Analytics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(r"D:\excel\Nassau.xlsx")


@st.cache_data
def load_data(path):
    df = pd.read_excel(path)

    # Convert dates
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce"
    )

    # Create Lead Time
    df["Lead Time"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    return df


# Load the data using our function
df = load_data(DATA_FILE)


st.title("Shipping Efficiency & Lead-Time Analytics")

st.caption(
    "Interactive Streamlit dashboard built from the Nassau.xlsx dataset"
)

# ---------------- Sidebar filters ----------------
st.sidebar.header("Dashboard Filters")

date_min = df["Order Date"].min().date()
date_max = df["Order Date"].max().date()
selected_dates = st.sidebar.date_input(
    "Order Date Range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date, end_date = date_min, date_max

regions = sorted(df["Region"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

states = sorted(df["State/Province"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect("State / Province", states, default=[])

ship_modes = sorted(df["Ship Mode"].dropna().unique().tolist())
selected_modes = st.sidebar.multiselect("Ship Mode", ship_modes, default=ship_modes)
valid_lead = df["Lead Time"].dropna()
lead_min = int(valid_lead.min())
lead_max = int(valid_lead.max())
lead_range = st.sidebar.slider(
    "Lead-Time Threshold (days)",
    min_value=lead_min,
    max_value=lead_max,
    value=(lead_min, lead_max),
)

# Apply filters
filtered = df[
    (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
    & (df["Region"].isin(selected_regions))
    & (df["Ship Mode"].isin(selected_modes))
    & (df["Lead Time"].between(lead_range[0], lead_range[1], inclusive="both"))
].copy()

if selected_states:
    filtered = filtered[filtered["State/Province"].isin(selected_states)].copy()

# ---------------- KPI row ----------------
orders = filtered["Order ID"].nunique()
records = len(filtered)
avg_lead = filtered["Lead Time"].mean() if records else 0
sales = filtered["Sales"].sum() if records else 0
profit = filtered["Gross Profit"].sum() if records else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Unique Orders", f"{orders:,}")
c2.metric("Records", f"{records:,}")
c3.metric("Avg Lead Time", f"{avg_lead:,.1f} days")
c4.metric("Sales", f"${sales:,.2f}")
c5.metric("Gross Profit", f"${profit:,.2f}")

if records == 0:
    st.warning("No records match the selected filters. Please widen the filters.")
    st.stop()

st.divider()

# ---------------- Route Efficiency ----------------
st.subheader("1. Route Efficiency Overview")
left, right = st.columns(2)

route = (
    filtered.groupby("State/Province", as_index=False)
    .agg(Avg_Lead_Time=("Lead Time", "mean"), Orders=("Order ID", "nunique"))
    .sort_values("Avg_Lead_Time")
)

with left:
    fig = px.bar(
        route,
        x="Avg_Lead_Time",
        y="State/Province",
        orientation="h",
        title="Average Lead Time by State / Province",
        labels={"Avg_Lead_Time": "Average Lead Time (days)", "State/Province": ""},
    )
    fig.update_layout(height=520, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with right:
    leaderboard = route.copy()
    leaderboard["Rank"] = range(1, len(leaderboard) + 1)
    leaderboard["Performance"] = leaderboard["Avg_Lead_Time"].round(2)
    st.markdown("**Route Performance Leaderboard**")
    st.dataframe(
        leaderboard[["Rank", "State/Province", "Performance", "Orders"]]
        .rename(columns={"Performance": "Avg Lead Time (days)"}),
        use_container_width=True,
        height=470,
        hide_index=True,
    )

# ---------------- Geographic + regional ----------------
st.subheader("2. Geographic Shipping Map & Regional Bottlenecks")
left, right = st.columns(2)

us = filtered[filtered["Country/Region"].eq("United States")].copy()
state_map = (
    us.groupby("State/Province", as_index=False)
    .agg(Avg_Lead_Time=("Lead Time", "mean"), Orders=("Order ID", "nunique"))
)

with left:
    if not state_map.empty:
        fig_map = px.choropleth(
            state_map,
            locations="State/Province",
            locationmode="USA-states",
            color="Avg_Lead_Time",
            scope="usa",
            color_continuous_scale="Viridis",
            hover_data={"Avg_Lead_Time": ":.1f", "Orders": True},
            labels={"Avg_Lead_Time": "Avg Lead Time (days)"},
            title="US Shipping Efficiency Heatmap",
        )
        fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No United States records match the current filters.")

with right:
    regional = (
        filtered.groupby("Region", as_index=False)
        .agg(Avg_Lead_Time=("Lead Time", "mean"), Records=("Order ID", "size"))
        .sort_values("Avg_Lead_Time", ascending=False)
    )
    fig_region = px.bar(
        regional,
        x="Region",
        y="Avg_Lead_Time",
        text="Avg_Lead_Time",
        title="Regional Bottleneck Visualization",
        labels={"Avg_Lead_Time": "Average Lead Time (days)"},
    )
    fig_region.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_region.update_layout(height=500, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig_region, use_container_width=True)

# ---------------- Ship mode ----------------
st.subheader("3. Ship Mode Comparison")
mode = (
    filtered.groupby("Ship Mode", as_index=False)
    .agg(Avg_Lead_Time=("Lead Time", "mean"), Orders=("Order ID", "nunique"))
    .sort_values("Avg_Lead_Time")
)
fig_mode = px.bar(
    mode,
    x="Ship Mode",
    y="Avg_Lead_Time",
    text="Avg_Lead_Time",
    title="Lead Time Comparison by Shipping Method",
    labels={"Avg_Lead_Time": "Average Lead Time (days)"},
)
fig_mode.update_traces(texttemplate="%{text:.1f}", textposition="outside")
st.plotly_chart(fig_mode, use_container_width=True)

# ---------------- State insights ----------------
st.subheader("4. State-Level Performance Insights")
state_detail = (
    filtered.groupby(["Region", "State/Province"], as_index=False)
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Median_Lead_Time=("Lead Time", "median"),
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
    )
    .sort_values("Avg_Lead_Time", ascending=False)
)
st.dataframe(
    state_detail.round({"Avg_Lead_Time": 2, "Median_Lead_Time": 2, "Sales": 2, "Gross_Profit": 2}),
    use_container_width=True,
    hide_index=True,
)

# ---------------- Order-level timeline ----------------
st.subheader("5. Order-Level Shipment Timeline")
order_cols = [
    "Order ID", "Order Date", "Ship Date", "Lead Time",
    "Ship Mode", "Region", "State/Province", "Sales", "Gross Profit"
]
order_view = filtered[order_cols].sort_values("Lead Time", ascending=False).copy()

search = st.text_input("Search Order ID (optional)")
if search:
    order_view = order_view[order_view["Order ID"].astype(str).str.contains(search, case=False, na=False)]

st.dataframe(
    order_view.head(1000),
    use_container_width=True,
    height=420,
    hide_index=True,
)

# ---------------- Data quality ----------------
with st.expander("⚠️ Data Quality Note"):
    st.write(
        f"The calculated Lead Time ranges from {lead_min:,} to {lead_max:,} days in the source data. "
        "These values are unusually large for conventional shipment operations. "
        "Validate the business meaning and correctness of Order Date and Ship Date before using "
        "the results for real-world operational or policy decisions."
    )

st.caption("Built with Python, Streamlit, Pandas and Plotly • Source: Nassau.xlsx")
