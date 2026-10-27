# NISR Big Data Hackathon | AgriTitans

**Track 2: Financial Inclusion and Poverty Reduction**

**Agricultural Finance Priority Dashboard: where farmers want credit but can't reach a bank**

Live dashboard: https://nisr-big-data-hackathon-ldhv7hqtp5e9vygehio2t2.streamlit.app/

## The problem

Farming is how most Rwandan households earn a living, and it runs on cash at specific moments: seed and fertiliser before the season, labour at harvest, a buffer when rain fails. A household that cannot save safely or borrow fairly carries all of that risk alone.

Rwanda's NST2 and Vision 2050 both prioritise agricultural transformation and wider financial inclusion, but a national target does not tell a ministry, a SACCO or an NGO **which province to start with**. This project answers that question with NISR data.

## The idea

For every province, we put two numbers from the 2024 Agricultural Household Survey side by side:

- **Access**: share of agricultural households with a bank account
- **Demand**: share of agricultural households requesting a loan

Where demand is higher than access, farmers are ready to borrow but the banking system is not reaching them. That gap is visible in the data, and it is something a policy or a product can close. The dashboard ranks provinces by that need and says what kind of response each one calls for.

## What the dashboard does

The app has five sections, selectable from the sidebar:

| Section | What it shows |
|---|---|
| **Overview** | Four headline averages (household and farmer bank access, household and farmer loan demand), a one-line finding, and a grouped bar chart of access vs demand by province. A toggle switches between households and farmers. |
| **Gap Analysis** | Inclusion gap per province (horizontal bars), a scatter of access vs demand with bubble size set by Priority Index, and a poverty vs bank access chart that appears when a poverty column is present in the data. |
| **Priority Ranking** | Provinces ranked by Priority Index, coloured by tier, with a full table and a **CSV download** for planning documents. |
| **Action Plan** | One expandable card per province: its numbers, its profile and a suggested focus. Also lists how government, lenders, NGOs and cooperatives can use the tool. |
| **Method and Data** | Formulas, tier cut-offs, limitations and raw data. |

Above every section, a **smart alert** banner names each selected province whose gap exceeds a threshold the user sets (default 10 points).

## How the numbers are built

**Inclusion gap** = loan demand − bank access (percentage points). Positive means more households want credit than hold an account.

**Loan-to-bank ratio** = loan demand ÷ bank access. The same signal in relative terms, so a small gap in a very low-access province is not hidden. A bank rate of 0 is treated as missing to avoid dividing by zero.

**Priority Index (0 to 100)** = weighted mix of three min-max scaled components:

| Component | Default weight |
|---|---|
| Inclusion gap | 40 |
| Loan-to-bank ratio | 30 |
| Low bank access (100 − bank %) | 30 |

The weights are sliders in the sidebar and the ranking recalculates immediately. A ministry worried about the widest gap and a microfinance lender looking for the strongest relative demand will not rank provinces the same way, so the tool lets them choose. Scores are always computed on all provinces, so filtering the view does not change a province's score.

**Tiers:** High (66 and above), Medium (33 to 65), Low (below 33).

**Province profiles** split at the median bank access and median loan demand across provinces:

| Profile | Condition | Suggested focus |
|---|---|---|
| Unmet credit demand | Low access, high demand | Agent banking, mobile lending, SACCO-linked loans with seasonal repayment |
| Low access, low demand | Low access, low demand | Account-opening drives, financial literacy, trust-building before loan products |
| Active borrowers | Higher access, high demand | Loan product fit, affordable rates, crop insurance |
| Relatively well served | Higher access, lower demand | Maintain services, reach remaining smallholders |

We chose a transparent index over a model on purpose. With a handful of provinces, a complex model would look impressive and mean little. An index that anyone can inspect, reweight and export is more useful to the people who would act on it.

## Who it is for

- **MINAGRI, MINECOFIN and districts**: decide where credit guarantees, extension support or agent networks go first.
- **Banks, SACCOs and MFIs**: see where demand already exists before opening branches or agents.
- **NGOs and development partners**: direct financial literacy and savings-group programmes.
- **Farmer cooperatives**: bring evidence of local demand to lender negotiations.

## Data

- **Source:** NISR Agricultural Household Survey 2024, summarised by province.
- **Input file:** `dashboard_data.csv`, with these required columns: `Province`, `HH_Bank_Percentage`, `HH_Loan_Percentage`, `Farmer_Bank_Percentage`, `Farmer_Loan_Percentage`. The app stops with a clear error if any are missing.
- **Optional:** any column whose name contains "poverty" automatically unlocks the poverty vs bank access chart.

## Run it locally

```bash
git clone https://github.com/<your-username>/nisr-big-data-hackathon.git
cd nisr-big-data-hackathon
pip install streamlit pandas plotly
streamlit run app.py
```

Keep `dashboard_data.csv` in the same folder as `app.py`.

## Limitations

- The loan figure is households **requesting** credit, not loans approved or used. High demand can reflect hardship as well as appetite to invest.
- Province averages hide large differences between districts and between small and large farms.
- Averages across provinces are not weighted by population, so they are not national estimates.
- The Priority Index is relative: it says which provinces rank higher, not how severe the problem is in absolute terms.
- The tool describes patterns. It does not prove that expanding access would reduce poverty.

## Next steps

1. Repeat the analysis at district level, where decisions are made.
2. Add loan approval and repayment data to separate unmet demand from distress borrowing.
3. Link poverty and social protection data to test whether the least-banked areas are also the poorest.
4. Weight results by household counts for national estimates.

## Team

**AgriTitans**, NISR Big Data Hackathon, Track 2.
