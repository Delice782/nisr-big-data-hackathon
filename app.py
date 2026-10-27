import pandas as pd
import plotly.express as px
import streamlit as st

# page setup
st.set_page_config(
    page_title="Agricultural Finance Priority Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# colours used across the dashboard
NAVY = "#1F3A5F"
TEAL = "#2A7F8E"
TIER_COLORS = {"High": "#B23A48", "Medium": "#E0A030", "Low": "#3E8E7E"}

# light styling so it looks clean in both light and dark themes
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 1250px;}
    [data-testid="stMetric"] {
        background: rgba(128,128,128,0.08);
        border: 1px solid rgba(128,128,128,0.25);
        border-left: 4px solid #2A7F8E;
        padding: 14px 16px;
        border-radius: 6px;
    }
    [data-testid="stSidebar"] {border-right: 1px solid rgba(128,128,128,0.25);}
    #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

REQUIRED = [
    "Province",
    "HH_Bank_Percentage",
    "HH_Loan_Percentage",
    "Farmer_Bank_Percentage",
    "Farmer_Loan_Percentage",
]


# load data once and reuse it
@st.cache_data
def load_data():
    return pd.read_csv("dashboard_data.csv")


# scale a column to 0-1 so different metrics can be combined
def minmax(s):
    rng = s.max() - s.min()
    return (s - s.min()) / rng if rng else s * 0


# shared chart styling
def style(fig):
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=50, b=10),
        legend_title_text="",
        font=dict(size=13),
    )
    return fig


df = load_data()

missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    st.error(f"dashboard_data.csv is missing columns: {missing}")
    st.stop()

# derived metrics (a bank rate of 0 would divide by zero, so treat it as missing)
bank_safe = df["HH_Bank_Percentage"].replace(0, float("nan"))
df["Loan_to_Bank_Ratio"] = df["HH_Loan_Percentage"] / bank_safe
df["Financial_Inclusion_Gap"] = df["HH_Loan_Percentage"] - df["HH_Bank_Percentage"]
df["Financial_Score"] = 0.5 * df["HH_Bank_Percentage"] + 0.5 * df["Farmer_Bank_Percentage"]

# sidebar: title, navigation, then filters
st.sidebar.title("Agricultural Finance")
st.sidebar.caption("NISR Agricultural Household Survey 2024")

section = st.sidebar.radio(
    "Navigate",
    ["Overview", "Gap Analysis", "Priority Ranking", "Action Plan", "Method and Data"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")
all_prov = sorted(df["Province"].unique())
chosen = st.sidebar.multiselect("Provinces", all_prov, default=all_prov)

with st.sidebar.expander("Priority index weights"):
    st.caption("Change what matters most and the ranking updates.")
    w_gap = st.slider("Inclusion gap", 0, 100, 40)
    w_ratio = st.slider("Loan-to-bank ratio", 0, 100, 30)
    w_low = st.slider("Low bank access", 0, 100, 30)

with st.sidebar.expander("Alert settings"):
    alert_gap = st.slider("Flag gap above (points)", 0, 50, 10)

if not chosen:
    st.warning("Select at least one province in the sidebar.")
    st.stop()

# priority index is scored on all provinces so scores stay comparable when filtering
total_w = max(w_gap + w_ratio + w_low, 1)
df["Priority_Index"] = 100 * (
    w_gap * minmax(df["Financial_Inclusion_Gap"])
    + w_ratio * minmax(df["Loan_to_Bank_Ratio"].fillna(0))
    + w_low * minmax(100 - df["HH_Bank_Percentage"])
) / total_w


def tier(score):
    if score >= 66:
        return "High"
    if score >= 33:
        return "Medium"
    return "Low"


df["Priority_Tier"] = df["Priority_Index"].apply(tier)

# classify each province by its situation, using the median as the dividing line
bank_med = df["HH_Bank_Percentage"].median()
loan_med = df["HH_Loan_Percentage"].median()


def profile(r):
    low_bank = r["HH_Bank_Percentage"] < bank_med
    high_loan = r["HH_Loan_Percentage"] >= loan_med
    if low_bank and high_loan:
        return (
            "Unmet credit demand",
            "Farmers want credit but few are banked. Prioritise agent banking, "
            "mobile lending and cooperative or SACCO-linked loans with seasonal repayment.",
        )
    if low_bank:
        return (
            "Low access, low demand",
            "Both access and demand are low. Start with account opening drives, "
            "financial literacy and trust-building before pushing loan products.",
        )
    if high_loan:
        return (
            "Active borrowers",
            "Demand is high and access is better. Focus on loan product fit, "
            "affordable rates and crop insurance to reduce repayment risk.",
        )
    return (
        "Relatively well served",
        "Access is comparatively strong. Maintain services and target "
        "smallholders still left out.",
    )


df[["Profile", "Suggested_Action"]] = df.apply(lambda r: pd.Series(profile(r)), axis=1)

view = df[df["Province"].isin(chosen)].copy()

# page header
st.title("Agricultural Finance Priority Dashboard")
st.markdown(
    "Agriculture is central to Rwandan livelihoods, yet access to formal finance is uneven. "
    "This tool shows where farmers want credit but are not yet banked, so government, banks "
    "and partners can target limited resources where they matter most. It supports the "
    "financial inclusion and agricultural transformation priorities of NST2 and Vision 2050."
)

# smart alert
flagged = view[view["Financial_Inclusion_Gap"] > alert_gap].sort_values(
    "Financial_Inclusion_Gap", ascending=False
)
if len(flagged):
    names = ", ".join(
        f"{r.Province} (+{r.Financial_Inclusion_Gap:.1f})" for r in flagged.itertuples()
    )
    st.error(f"Alert: loan demand exceeds bank access by more than {alert_gap} points in: {names}")
else:
    st.success(f"No selected province exceeds the {alert_gap}-point alert threshold.")

st.markdown("---")

# overview
if section == "Overview":
    st.header("Overview")
    n_gap = int((view["Financial_Inclusion_Gap"] > 0).sum())
    st.info(
        f"In {n_gap} of {len(view)} selected provinces, household loan demand is higher "
        f"than bank account access. Average across provinces: bank access "
        f"{view['HH_Bank_Percentage'].mean():.1f}%, loan demand "
        f"{view['HH_Loan_Percentage'].mean():.1f}%."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Household bank access", f"{view['HH_Bank_Percentage'].mean():.1f}%")
    c2.metric("Household loan demand", f"{view['HH_Loan_Percentage'].mean():.1f}%")
    c3.metric("Farmer bank access", f"{view['Farmer_Bank_Percentage'].mean():.1f}%")
    c4.metric("Farmer loan demand", f"{view['Farmer_Loan_Percentage'].mean():.1f}%")
    st.caption("Simple averages across the selected provinces.")

    group = st.radio("Compare for", ["Households", "Farmers"], horizontal=True)
    prefix = "HH" if group == "Households" else "Farmer"
    long = view.melt(
        id_vars="Province",
        value_vars=[f"{prefix}_Bank_Percentage", f"{prefix}_Loan_Percentage"],
        var_name="Metric",
        value_name="Percentage",
    )
    long["Metric"] = long["Metric"].map(
        {f"{prefix}_Bank_Percentage": "Has bank account", f"{prefix}_Loan_Percentage": "Wants a loan"}
    )
    fig = px.bar(
        long, x="Province", y="Percentage", color="Metric", barmode="group",
        title=f"{group}: bank access vs loan demand (%)", text_auto=".1f",
        color_discrete_sequence=[NAVY, TEAL],
    )
    st.plotly_chart(style(fig), width="stretch")

# gap analysis
elif section == "Gap Analysis":
    st.header("Gap Analysis")
    fig = px.bar(
        view.sort_values("Financial_Inclusion_Gap"),
        x="Financial_Inclusion_Gap", y="Province", orientation="h",
        color="Financial_Inclusion_Gap", color_continuous_scale="RdYlGn_r",
        title="Inclusion gap: loan demand minus bank access (percentage points)",
        labels={"Financial_Inclusion_Gap": "Gap (points)"},
    )
    st.plotly_chart(style(fig), width="stretch")

    fig = px.scatter(
        view, x="HH_Bank_Percentage", y="HH_Loan_Percentage", text="Province",
        size="Priority_Index", color="Priority_Tier", color_discrete_map=TIER_COLORS,
        title="Where demand outruns access (bubble size = priority index)",
        labels={"HH_Bank_Percentage": "Bank access (%)", "HH_Loan_Percentage": "Loan demand (%)"},
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(style(fig), width="stretch")
    st.caption("Provinces above the diagonal have more loan demand than bank access.")

    # poverty link, shown only if the data has a poverty column
    pov_cols = [c for c in df.columns if "poverty" in c.lower()]
    if pov_cols:
        pov = st.selectbox("Poverty indicator", pov_cols)
        fig = px.scatter(
            view, x=pov, y="HH_Bank_Percentage", text="Province",
            title="Poverty vs bank access",
            labels={"HH_Bank_Percentage": "Bank access (%)"},
            color_discrete_sequence=[NAVY],
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(style(fig), width="stretch")

# priority ranking
elif section == "Priority Ranking":
    st.header("Priority Ranking")
    st.write(
        "The index (0 to 100) combines the inclusion gap, the loan-to-bank ratio and low bank access. "
        "Adjust the weights in the sidebar."
    )
    ranked = view.sort_values("Priority_Index", ascending=False)
    fig = px.bar(
        ranked, x="Priority_Index", y="Province", orientation="h", color="Priority_Tier",
        color_discrete_map=TIER_COLORS, title="Provinces ranked by need for intervention",
    )
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(style(fig), width="stretch")

    table = ranked[[
        "Province", "Priority_Index", "Priority_Tier", "HH_Bank_Percentage",
        "HH_Loan_Percentage", "Financial_Inclusion_Gap", "Loan_to_Bank_Ratio", "Financial_Score",
    ]].round(2)
    st.dataframe(table, width="stretch", hide_index=True)
    st.download_button(
        "Download ranking (CSV)", table.to_csv(index=False).encode("utf-8"),
        file_name="province_priority_ranking.csv", mime="text/csv",
    )

# action plan
elif section == "Action Plan":
    st.header("Action Plan")
    st.write("Suggested focus for each province, based on its own numbers.")
    for r in view.sort_values("Priority_Index", ascending=False).itertuples():
        with st.expander(f"{r.Province}  |  {r.Priority_Tier} priority ({r.Priority_Index:.0f}/100)  |  {r.Profile}"):
            st.write(
                f"Bank access {r.HH_Bank_Percentage:.1f}%, loan demand {r.HH_Loan_Percentage:.1f}%, "
                f"gap {r.Financial_Inclusion_Gap:+.1f} points."
            )
            st.write(r.Suggested_Action)

    st.subheader("Who can use this")
    st.write(
        "- **Government (MINAGRI, MINECOFIN, local districts):** target credit guarantees and extension support.\n"
        "- **Banks, SACCOs and microfinance:** decide where to open agents and design seasonal loan products.\n"
        "- **Development partners and NGOs:** direct financial literacy and group-savings programmes.\n"
        "- **Farmer cooperatives:** show evidence of local demand when negotiating with lenders."
    )

# method and data
else:
    st.header("Method and Data")
    st.markdown(
        """
**Data:** NISR Agricultural Household Survey 2024, summarised by province.

**Metrics**
- Inclusion gap = loan percentage minus bank account percentage
- Loan-to-bank ratio = loan percentage divided by bank account percentage
- Priority index = weighted sum of the min-max scaled gap, ratio and (100 minus bank access), shown as 0 to 100
- Tiers: High (66 and above), Medium (33 to 65), Low (below 33)
- Profiles split provinces at the median bank access and median loan demand

**Limitations**
- Loan percentage measures requested or demanded loans, not loans approved or used.
- Scores are relative: with few provinces, the index ranks them against each other and is not an absolute measure.
- Province-level averages hide differences between districts and between large and small farms.
- Averages across provinces are unweighted, not national estimates.

**Next steps:** district-level analysis, loan approval data, and weighting by household counts.
"""
    )
    with st.expander("View raw data"):
        st.dataframe(df, width="stretch")
