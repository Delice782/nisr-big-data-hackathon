# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # page setup
# st.set_page_config(
#     page_title="Agricultural Financial Inclusion Dashboard",
#     page_icon="🌾",
#     layout="wide"
# )

# # load data
# dashboard_df = pd.read_csv("dashboard_data.csv")

# # derived metrics
# dashboard_df["Loan_to_Bank_Ratio"] = (
#     dashboard_df["HH_Loan_Percentage"] / dashboard_df["HH_Bank_Percentage"]
# )
# dashboard_df["Financial_Inclusion_Gap"] = (
#     dashboard_df["HH_Loan_Percentage"] - dashboard_df["HH_Bank_Percentage"]
# )
# dashboard_df["Financial_Score"] = (
#     dashboard_df["HH_Bank_Percentage"] * 0.5
#     + dashboard_df["Farmer_Bank_Percentage"] * 0.5
# )

# # values reused in several sections
# avg_hh_bank = dashboard_df["HH_Bank_Percentage"].mean()
# avg_hh_loan = dashboard_df["HH_Loan_Percentage"].mean()
# avg_farmer_bank = dashboard_df["Farmer_Bank_Percentage"].mean()
# avg_farmer_loan = dashboard_df["Farmer_Loan_Percentage"].mean()

# highest_bank = dashboard_df.loc[dashboard_df["HH_Bank_Percentage"].idxmax()]
# highest_loan = dashboard_df.loc[dashboard_df["HH_Loan_Percentage"].idxmax()]
# largest_gap = dashboard_df.loc[dashboard_df["Financial_Inclusion_Gap"].idxmax()]

# # title
# st.title("🌾 Agricultural Financial Inclusion Dashboard")
# st.caption("Agricultural Household Survey 2024")

# # executive summary
# st.markdown("## Executive Summary")

# st.info(
#     f"""
#     Agricultural households demonstrate significant demand for financial services.

#     • Average Agricultural Household Bank Access: **{avg_hh_bank:.1f}%**

#     • Average Agricultural Household Loan Demand: **{avg_hh_loan:.1f}%**

#     • Average Farmer Bank Access: **{avg_farmer_bank:.1f}%**

#     • Average Farmer Loan Demand: **{avg_farmer_loan:.1f}%**

#     Loan demand exceeds banking participation in most provinces, indicating opportunities to strengthen access to affordable agricultural finance.
#     """
# )

# # key indicators (KPI cards)
# st.markdown("## Key Indicators")

# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Agricultural HH Bank Access", f"{avg_hh_bank:.1f}%")
# c2.metric("Agricultural HH Loan Demand", f"{avg_hh_loan:.1f}%")
# c3.metric("Farmer Bank Access", f"{avg_farmer_bank:.1f}%")
# c4.metric("Farmers Requesting Loans", f"{avg_farmer_loan:.1f}%")

# # banking access vs loan demand
# st.markdown("---")
# st.markdown("## Banking Access vs Loan Demand")

# comparison_df = dashboard_df.melt(
#     id_vars="Province",
#     value_vars=["HH_Bank_Percentage", "HH_Loan_Percentage"],
#     var_name="Metric",
#     value_name="Percentage"
# )
# comparison_df["Metric"] = comparison_df["Metric"].replace({
#     "HH_Bank_Percentage": "Bank Account Percentage",
#     "HH_Loan_Percentage": "Loan Percentage"
# })

# fig1 = px.bar(
#     comparison_df,
#     x="Province",
#     y="Percentage",
#     color="Metric",
#     barmode="group",
#     title="Agricultural Households: Bank Accounts vs Loan Requests"
# )

# left, right = st.columns([3, 1])
# with left:
#     st.plotly_chart(fig1, use_container_width=True)
# with right:
#     st.markdown("### Summary")
#     st.write(
#         """
#         This chart compares financial inclusion with demand for credit.

#         Provinces where loan demand significantly exceeds banking access may face barriers to financial services.
#         """
#     )

# # financial inclusion gap
# st.markdown("---")
# st.markdown("## Financial Inclusion Gap")

# fig2 = px.bar(
#     dashboard_df,
#     x="Province",
#     y="Financial_Inclusion_Gap",
#     color="Financial_Inclusion_Gap",
#     title="Loan Demand Minus Bank Account Access",
#     labels={"Financial_Inclusion_Gap": "Financial Inclusion Gap (%)"}
# )

# left, right = st.columns([3, 1])
# with left:
#     st.plotly_chart(fig2, use_container_width=True)
# with right:
#     st.markdown("### Insight")
#     st.warning(
#         f"""
#         {largest_gap['Province']} exhibits the largest gap between
#         banking access and demand for loans.

#         This suggests high demand for financial services that may not
#         be fully met by current banking inclusion.
#         """
#     )

# # loan-to-bank ratio
# st.markdown("---")
# st.markdown("## Loan-to-Bank Ratio")

# fig3 = px.bar(
#     dashboard_df,
#     x="Province",
#     y="Loan_to_Bank_Ratio",
#     color="Loan_to_Bank_Ratio",
#     title="Loan Demand Relative to Banking Access",
#     labels={"Loan_to_Bank_Ratio": "Loan Bank Ratio"}
# )

# left, right = st.columns([3, 1])
# with left:
#     st.plotly_chart(fig3, use_container_width=True)
# with right:
#     st.markdown("### Interpretation")
#     st.write(
#         """
#         Values above 1 indicate that loan demand exceeds the level of banking participation.

#         Higher values may signal opportunities to expand agricultural financing products and outreach.
#         """
#     )

# # provincial scorecard
# st.markdown("---")
# st.markdown("## Provincial Scorecard")

# scorecard = dashboard_df[[
#     "Province",
#     "HH_Bank_Percentage",
#     "HH_Loan_Percentage",
#     "Loan_to_Bank_Ratio",
#     "Financial_Inclusion_Gap",
#     "Financial_Score"
# ]]

# st.dataframe(
#     scorecard.sort_values(by="Financial_Score", ascending=False),
#     use_container_width=True
# )

# # key findings
# st.markdown("---")
# st.markdown("## Key Findings")

# st.success(
#     f"Highest banking access: {highest_bank['Province']} "
#     f"({highest_bank['HH_Bank_Percentage']:.1f}%)"
# )
# st.info(
#     f"Highest loan demand: {highest_loan['Province']} "
#     f"({highest_loan['HH_Loan_Percentage']:.1f}%)"
# )
# st.warning(
#     f"Largest financial inclusion gap: {largest_gap['Province']} "
#     f"({largest_gap['Financial_Inclusion_Gap']:.1f} percentage points)"
# )

# # recommendations
# st.markdown("---")
# st.markdown("## Recommendations")

# with st.expander("🏦 Strengthen Financial Inclusion"):
#     st.write("""
#     • Expand rural banking agents and mobile banking services.

#     • Simplify account opening procedures for smallholder farmers.

#     • Improve financial literacy and savings awareness programmes.

#     • Promote digital financial services through cooperatives.
#     """)

# with st.expander("💰 Improve Access to Agricultural Credit"):
#     st.write("""
#     • Develop farmer-friendly loan products aligned with seasonal crop cycles.

#     • Increase cooperative-based lending programmes.

#     • Establish agricultural credit guarantee facilities.

#     • Expand low-interest lending targeted at productive investments.
#     """)

# with st.expander("🌱 Reduce Poverty Among Agricultural Households"):
#     st.write("""
#     • Encourage savings and investment groups.

#     • Promote crop insurance and risk mitigation products.

#     • Improve market access and value-chain participation.

#     • Support diversification into higher-value agricultural activities.

#     • Expand agricultural extension and productivity programmes.
#     """)

# # footer
# st.markdown("---")
# st.caption("Agricultural Household Financial Inclusion Dashboard | AHS 2024")




import pandas as pd
import plotly.express as px
import streamlit as st

# page setup
st.set_page_config(
    page_title="Agricultural Finance Priority Dashboard",
    page_icon="🌾",
    layout="wide",
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

# sidebar controls
st.sidebar.header("Controls")
all_prov = sorted(df["Province"].unique())
chosen = st.sidebar.multiselect("Provinces", all_prov, default=all_prov)

st.sidebar.subheader("Priority index weights")
st.sidebar.caption("Change what matters most and the ranking updates.")
w_gap = st.sidebar.slider("Inclusion gap", 0, 100, 40)
w_ratio = st.sidebar.slider("Loan-to-bank ratio", 0, 100, 30)
w_low = st.sidebar.slider("Low bank access", 0, 100, 30)

st.sidebar.subheader("Smart alert")
alert_gap = st.sidebar.slider("Flag provinces with gap above (points)", 0, 50, 10)

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

# header and problem statement
st.title("🌾 Agricultural Finance Priority Dashboard")
st.caption("Source: NISR Agricultural Household Survey (AHS) 2024")

st.markdown(
    "**The problem:** agriculture is central to Rwandan livelihoods, yet access to formal finance "
    "is uneven. This tool shows where farmers want credit but are not yet banked, so government, "
    "banks and partners can target limited resources where they matter most. "
    "It supports the financial inclusion and agricultural transformation priorities of "
    "NST2 and Vision 2050."
)

# smart alerts
flagged = view[view["Financial_Inclusion_Gap"] > alert_gap].sort_values(
    "Financial_Inclusion_Gap", ascending=False
)
if len(flagged):
    names = ", ".join(
        f"{r.Province} (+{r.Financial_Inclusion_Gap:.1f})" for r in flagged.itertuples()
    )
    st.error(f"🚨 Alert: loan demand exceeds bank access by more than {alert_gap} points in: {names}")
else:
    st.success(f"✅ No selected province exceeds the {alert_gap}-point alert threshold.")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Gap analysis", "Priority ranking", "Action plan", "Method and data"]
)

# overview tab
with tab1:
    n_gap = int((view["Financial_Inclusion_Gap"] > 0).sum())
    st.info(
        f"In **{n_gap} of {len(view)}** selected provinces, household loan demand is higher "
        f"than bank account access. Average across provinces: bank access "
        f"**{view['HH_Bank_Percentage'].mean():.1f}%**, loan demand "
        f"**{view['HH_Loan_Percentage'].mean():.1f}%**."
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
    )
    st.plotly_chart(fig, width="stretch")

# gap analysis tab
with tab2:
    fig = px.bar(
        view.sort_values("Financial_Inclusion_Gap"),
        x="Financial_Inclusion_Gap", y="Province", orientation="h",
        color="Financial_Inclusion_Gap", color_continuous_scale="RdYlGn_r",
        title="Inclusion gap: loan demand minus bank access (percentage points)",
        labels={"Financial_Inclusion_Gap": "Gap (points)"},
    )
    st.plotly_chart(fig, width="stretch")

    fig = px.scatter(
        view, x="HH_Bank_Percentage", y="HH_Loan_Percentage", text="Province",
        size="Priority_Index", color="Priority_Tier",
        color_discrete_map={"High": "#d62728", "Medium": "#ff7f0e", "Low": "#2ca02c"},
        title="Where demand outruns access (bubble size = priority index)",
        labels={"HH_Bank_Percentage": "Bank access (%)", "HH_Loan_Percentage": "Loan demand (%)"},
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, width="stretch")
    st.caption("Provinces above the diagonal have more loan demand than bank access.")

    # poverty link, shown only if the data has a poverty column
    pov_cols = [c for c in df.columns if "poverty" in c.lower()]
    if pov_cols:
        pov = st.selectbox("Poverty indicator", pov_cols)
        fig = px.scatter(
            view, x=pov, y="HH_Bank_Percentage", text="Province",
            title="Poverty vs bank access",
            labels={"HH_Bank_Percentage": "Bank access (%)"},
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, width="stretch")

# priority ranking tab
with tab3:
    st.write(
        "The index (0 to 100) combines the inclusion gap, the loan-to-bank ratio and low bank access. "
        "Adjust the weights in the sidebar."
    )
    ranked = view.sort_values("Priority_Index", ascending=False)
    fig = px.bar(
        ranked, x="Priority_Index", y="Province", orientation="h", color="Priority_Tier",
        color_discrete_map={"High": "#d62728", "Medium": "#ff7f0e", "Low": "#2ca02c"},
        title="Provinces ranked by need for intervention",
    )
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, width="stretch")

    table = ranked[[
        "Province", "Priority_Index", "Priority_Tier", "HH_Bank_Percentage",
        "HH_Loan_Percentage", "Financial_Inclusion_Gap", "Loan_to_Bank_Ratio", "Financial_Score",
    ]].round(2)
    st.dataframe(table, width="stretch", hide_index=True)
    st.download_button(
        "Download ranking (CSV)", table.to_csv(index=False).encode("utf-8"),
        file_name="province_priority_ranking.csv", mime="text/csv",
    )

# action plan tab
with tab4:
    st.write("Suggested focus for each province, based on its own numbers.")
    for r in view.sort_values("Priority_Index", ascending=False).itertuples():
        icon = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}[r.Priority_Tier]
        with st.expander(f"{icon} {r.Province}: {r.Profile} (priority {r.Priority_Index:.0f}/100)"):
            st.write(
                f"Bank access {r.HH_Bank_Percentage:.1f}%, loan demand {r.HH_Loan_Percentage:.1f}%, "
                f"gap {r.Financial_Inclusion_Gap:+.1f} points."
            )
            st.write(r.Suggested_Action)

    st.markdown("#### Who can use this")
    st.write(
        "- **Government (MINAGRI, MINECOFIN, local districts):** target credit guarantees and extension support.\n"
        "- **Banks, SACCOs and microfinance:** decide where to open agents and design seasonal loan products.\n"
        "- **Development partners and NGOs:** direct financial literacy and group-savings programmes.\n"
        "- **Farmer cooperatives:** show evidence of local demand when negotiating with lenders."
    )

# method and data tab
with tab5:
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
