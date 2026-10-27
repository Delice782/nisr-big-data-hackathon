import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Agricultural Financial Inclusion Dashboard",
    page_icon="🌾",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

# Replace with your actual dataframe loading logic
dashboard_df = pd.read_csv("dashboard_data.csv")

# ==========================================================
# DERIVED METRICS
# ==========================================================

dashboard_df["Loan_to_Bank_Ratio"] = (
    dashboard_df["HH_Loan_Percentage"]
    / dashboard_df["HH_Bank_Percentage"]
)

dashboard_df["Financial_Inclusion_Gap"] = (
    dashboard_df["HH_Loan_Percentage"]
    - dashboard_df["HH_Bank_Percentage"]
)

# ==========================================================
# TITLE
# ==========================================================

st.title("🌾 Agricultural Financial Inclusion Dashboard")
st.caption("Agricultural Household Survey 2024")

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.markdown("## Executive Summary")

avg_hh_bank = dashboard_df["HH_Bank_Percentage"].mean()
avg_hh_loan = dashboard_df["HH_Loan_Percentage"].mean()
avg_farmer_bank = dashboard_df["Farmer_Bank_Percentage"].mean()
avg_farmer_loan = dashboard_df["Farmer_Loan_Percentage"].mean()

st.info(
    f"""
    Agricultural households demonstrate significant demand for financial services.

    • Average Agricultural Household Bank Access: **{avg_hh_bank:.1f}%**

    • Average Agricultural Household Loan Demand: **{avg_hh_loan:.1f}%**

    • Average Farmer Bank Access: **{avg_farmer_bank:.1f}%**

    • Average Farmer Loan Demand: **{avg_farmer_loan:.1f}%**

    Loan demand exceeds banking participation in most provinces, indicating opportunities to strengthen access to affordable agricultural finance.
    """
)

# ==========================================================
# KPI SECTION
# ==========================================================

st.markdown("## Key Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Agricultural HH Bank Access",
    f"{avg_hh_bank:.1f}%"
)

col2.metric(
    "Agricultural HH Loan Demand",
    f"{avg_hh_loan:.1f}%"
)

col3.metric(
    "Farmer Bank Access",
    f"{avg_farmer_bank:.1f}%"
)

col4.metric(
    "Farmers Requesting Loans",
    f"{avg_farmer_loan:.1f}%"
)

# ==========================================================
# BANK ACCOUNTS VS LOANS
# ==========================================================

st.markdown("---")
st.markdown("## Banking Access vs Loan Demand")

comparison_df = dashboard_df.melt(
    id_vars="Province",
    value_vars=[
        "HH_Bank_Percentage",
        "HH_Loan_Percentage"
    ],
    var_name="Metric",
    value_name="Percentage"
)

comparison_df["Metric"] = comparison_df["Metric"].replace({
    "HH_Bank_Percentage": "Bank Account Percentage",
    "HH_Loan_Percentage": "Loan Percentage"
})

fig1 = px.bar(
    comparison_df,
    x="Province",
    y="Percentage",
    color="Metric",
    barmode="group",
    title="Agricultural Households: Bank Accounts vs Loan Requests"
)

col1, col2 = st.columns([3,1])

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Summary")
    st.write(
        """
        This chart compares financial inclusion with demand for credit.

        Provinces where loan demand significantly exceeds banking access may face barriers to financial services.
        """
    )

# ==========================================================
# FINANCIAL INCLUSION GAP
# ==========================================================

st.markdown("---")
st.markdown("## Financial Inclusion Gap")

fig2 = px.bar(
    dashboard_df,
    x="Province",
    y="Financial_Inclusion_Gap",
    color="Financial_Inclusion_Gap",
    title="Loan Demand Minus Bank Account Access",
    labels={
        "Financial_Inclusion_Gap":
        "Financial Inclusion Gap (%)"
    }
)

col1, col2 = st.columns([3,1])

with col1:
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("### Insight")

    largest_gap = dashboard_df.loc[
        dashboard_df["Financial_Inclusion_Gap"].idxmax()
    ]

    st.warning(
        f"""
        {largest_gap['Province']} exhibits the largest gap between
        banking access and demand for loans.

        This suggests high demand for financial services that may not
        be fully met by current banking inclusion.
        """
    )

# ==========================================================
# LOAN TO BANK RATIO
# ==========================================================

st.markdown("---")
st.markdown("## Loan-to-Bank Ratio")

fig3 = px.bar(
    dashboard_df,
    x="Province",
    y="Loan_to_Bank_Ratio",
    color="Loan_to_Bank_Ratio",
    title="Loan Demand Relative to Banking Access",
    labels={
        "Loan_to_Bank_Ratio": "Loan Bank Ratio"
    }
)

col1, col2 = st.columns([3,1])

with col1:
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("### Interpretation")

    st.write(
        """
        Values above 1 indicate that loan demand exceeds the level of banking participation.

        Higher values may signal opportunities to expand agricultural financing products and outreach.
        """
    )

# ==========================================================
# PROVINCIAL SCORECARD
# ==========================================================

st.markdown("---")
st.markdown("## Provincial Scorecard")

dashboard_df["Financial_Score"] = (
    dashboard_df["HH_Bank_Percentage"] * 0.5
    +
    dashboard_df["Farmer_Bank_Percentage"] * 0.5
)

scorecard = dashboard_df[[
    "Province",
    "HH_Bank_Percentage",
    "HH_Loan_Percentage",
    "Loan_to_Bank_Ratio",
    "Financial_Inclusion_Gap",
    "Financial_Score"
]]

st.dataframe(
    scorecard.sort_values(
        by="Financial_Score",
        ascending=False
    ),
    use_container_width=True
)


# KEY FINDINGS


st.markdown("---")
st.markdown("## Key Findings")

highest_bank = dashboard_df.loc[
    dashboard_df["HH_Bank_Percentage"].idxmax()
]

highest_loan = dashboard_df.loc[
    dashboard_df["HH_Loan_Percentage"].idxmax()
]

largest_gap = dashboard_df.loc[
    dashboard_df["Financial_Inclusion_Gap"].idxmax()
]

st.success(
    f"Highest banking access: {highest_bank['Province']} "
    f"({highest_bank['HH_Bank_Percentage']:.1f}%)"
)

st.info(
    f"Highest loan demand: {highest_loan['Province']} "
    f"({highest_loan['HH_Loan_Percentage']:.1f}%)"
)

st.warning(
    f"Largest financial inclusion gap: "
    f"{largest_gap['Province']} "
    f"({largest_gap['Financial_Inclusion_Gap']:.1f} percentage points)"
)


# RECOMMENDATIONS


st.markdown("---")
st.markdown("## Recommendations")

with st.expander("🏦 Strengthen Financial Inclusion"):
    st.write("""
    • Expand rural banking agents and mobile banking services.

    • Simplify account opening procedures for smallholder farmers.

    • Improve financial literacy and savings awareness programmes.

    • Promote digital financial services through cooperatives.
    """)

with st.expander("💰 Improve Access to Agricultural Credit"):
    st.write("""
    • Develop farmer-friendly loan products aligned with seasonal crop cycles.

    • Increase cooperative-based lending programmes.

    • Establish agricultural credit guarantee facilities.

    • Expand low-interest lending targeted at productive investments.
    """)

with st.expander("🌱 Reduce Poverty Among Agricultural Households"):
    st.write("""
    • Encourage savings and investment groups.

    • Promote crop insurance and risk mitigation products.

    • Improve market access and value-chain participation.

    • Support diversification into higher-value agricultural activities.

    • Expand agricultural extension and productivity programmes.
    """)

# FOOTER


st.markdown("---")
st.caption(
    "Agricultural Household Financial Inclusion Dashboard | AHS 2024"
)
