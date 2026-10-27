import streamlit as st
import pandas as pd
import plotly.express as px

# page setup
st.set_page_config(
    page_title="Agricultural Financial Inclusion Dashboard",
    page_icon="🌾",
    layout="wide"
)

# load data
dashboard_df = pd.read_csv("dashboard_data.csv")

# derived metrics
dashboard_df["Loan_to_Bank_Ratio"] = (
    dashboard_df["HH_Loan_Percentage"] / dashboard_df["HH_Bank_Percentage"]
)
dashboard_df["Financial_Inclusion_Gap"] = (
    dashboard_df["HH_Loan_Percentage"] - dashboard_df["HH_Bank_Percentage"]
)
dashboard_df["Financial_Score"] = (
    dashboard_df["HH_Bank_Percentage"] * 0.5
    + dashboard_df["Farmer_Bank_Percentage"] * 0.5
)

# values reused in several sections
avg_hh_bank = dashboard_df["HH_Bank_Percentage"].mean()
avg_hh_loan = dashboard_df["HH_Loan_Percentage"].mean()
avg_farmer_bank = dashboard_df["Farmer_Bank_Percentage"].mean()
avg_farmer_loan = dashboard_df["Farmer_Loan_Percentage"].mean()

highest_bank = dashboard_df.loc[dashboard_df["HH_Bank_Percentage"].idxmax()]
highest_loan = dashboard_df.loc[dashboard_df["HH_Loan_Percentage"].idxmax()]
largest_gap = dashboard_df.loc[dashboard_df["Financial_Inclusion_Gap"].idxmax()]

# title
st.title("🌾 Agricultural Financial Inclusion Dashboard")
st.caption("Agricultural Household Survey 2024")

# executive summary
st.markdown("## Executive Summary")

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

# key indicators (KPI cards)
st.markdown("## Key Indicators")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Agricultural HH Bank Access", f"{avg_hh_bank:.1f}%")
c2.metric("Agricultural HH Loan Demand", f"{avg_hh_loan:.1f}%")
c3.metric("Farmer Bank Access", f"{avg_farmer_bank:.1f}%")
c4.metric("Farmers Requesting Loans", f"{avg_farmer_loan:.1f}%")

# banking access vs loan demand
st.markdown("---")
st.markdown("## Banking Access vs Loan Demand")

comparison_df = dashboard_df.melt(
    id_vars="Province",
    value_vars=["HH_Bank_Percentage", "HH_Loan_Percentage"],
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

left, right = st.columns([3, 1])
with left:
    st.plotly_chart(fig1, use_container_width=True)
with right:
    st.markdown("### Summary")
    st.write(
        """
        This chart compares financial inclusion with demand for credit.

        Provinces where loan demand significantly exceeds banking access may face barriers to financial services.
        """
    )

# financial inclusion gap
st.markdown("---")
st.markdown("## Financial Inclusion Gap")

fig2 = px.bar(
    dashboard_df,
    x="Province",
    y="Financial_Inclusion_Gap",
    color="Financial_Inclusion_Gap",
    title="Loan Demand Minus Bank Account Access",
    labels={"Financial_Inclusion_Gap": "Financial Inclusion Gap (%)"}
)

left, right = st.columns([3, 1])
with left:
    st.plotly_chart(fig2, use_container_width=True)
with right:
    st.markdown("### Insight")
    st.warning(
        f"""
        {largest_gap['Province']} exhibits the largest gap between
        banking access and demand for loans.

        This suggests high demand for financial services that may not
        be fully met by current banking inclusion.
        """
    )

# loan-to-bank ratio
st.markdown("---")
st.markdown("## Loan-to-Bank Ratio")

fig3 = px.bar(
    dashboard_df,
    x="Province",
    y="Loan_to_Bank_Ratio",
    color="Loan_to_Bank_Ratio",
    title="Loan Demand Relative to Banking Access",
    labels={"Loan_to_Bank_Ratio": "Loan Bank Ratio"}
)

left, right = st.columns([3, 1])
with left:
    st.plotly_chart(fig3, use_container_width=True)
with right:
    st.markdown("### Interpretation")
    st.write(
        """
        Values above 1 indicate that loan demand exceeds the level of banking participation.

        Higher values may signal opportunities to expand agricultural financing products and outreach.
        """
    )

# provincial scorecard
st.markdown("---")
st.markdown("## Provincial Scorecard")

scorecard = dashboard_df[[
    "Province",
    "HH_Bank_Percentage",
    "HH_Loan_Percentage",
    "Loan_to_Bank_Ratio",
    "Financial_Inclusion_Gap",
    "Financial_Score"
]]

st.dataframe(
    scorecard.sort_values(by="Financial_Score", ascending=False),
    use_container_width=True
)

# key findings
st.markdown("---")
st.markdown("## Key Findings")

st.success(
    f"Highest banking access: {highest_bank['Province']} "
    f"({highest_bank['HH_Bank_Percentage']:.1f}%)"
)
st.info(
    f"Highest loan demand: {highest_loan['Province']} "
    f"({highest_loan['HH_Loan_Percentage']:.1f}%)"
)
st.warning(
    f"Largest financial inclusion gap: {largest_gap['Province']} "
    f"({largest_gap['Financial_Inclusion_Gap']:.1f} percentage points)"
)

# recommendations
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

# footer
st.markdown("---")
st.caption("Agricultural Household Financial Inclusion Dashboard | AHS 2024")
