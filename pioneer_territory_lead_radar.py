import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------------------------------------
# Page configuration
# -----------------------------------------------------------
st.set_page_config(
    page_title="Pioneer Territory Lead Radar",
    page_icon="📦",
    layout="wide",
)


# -----------------------------------------------------------
# Mock data generator
# -----------------------------------------------------------
def load_mock_data() -> pd.DataFrame:
    """Create a mock dataset of expansion signals for Jurong/Pioneer leads."""
    data = [
        {
            "Date Detected": "2026-04-09",
            "Company Name": "BASF Singapore",
            "Signal Type": "Job Posting",
            "Signal Headline": "Hiring 3x Chemical Process Technicians for Jurong Island operations",
            "AI Intent Score": 9,
            "AI Summary": "Multiple process technician hires usually indicate a need to support higher production throughput, which can increase drum consumption.",
        },
        {
            "Date Detected": "2026-04-08",
            "Company Name": "Evonik",
            "Signal Type": "News Article",
            "Signal Headline": "Evonik highlights specialty chemicals output expansion in Singapore",
            "AI Intent Score": 8,
            "AI Summary": "Public statements about output expansion suggest upcoming increases in raw material handling and finished product packaging demand.",
        },
        {
            "Date Detected": "2026-04-08",
            "Company Name": "Lubrizol",
            "Signal Type": "Job Posting",
            "Signal Headline": "Opening for Production Planner in Pioneer manufacturing cluster",
            "AI Intent Score": 7,
            "AI Summary": "A production planning hire often points to broader scheduling complexity and possible growth in order volume requiring more industrial packaging.",
        },
        {
            "Date Detected": "2026-04-07",
            "Company Name": "Shell Chemicals",
            "Signal Type": "Gov Permit",
            "Signal Headline": "Permit filing linked to process equipment modification at Bukom/Jurong network",
            "AI Intent Score": 9,
            "AI Summary": "Process modification permits can signal line upgrades or capacity improvements that may translate into higher packaging throughput.",
        },
        {
            "Date Detected": "2026-04-07",
            "Company Name": "Mitsui Chemicals Asia Pacific",
            "Signal Type": "Job Posting",
            "Signal Headline": "Recruiting Logistics Executive for Jurong Island supply chain",
            "AI Intent Score": 6,
            "AI Summary": "A logistics role alone is a moderate indicator, but it can suggest increased outbound movement tied to packaging usage.",
        },
        {
            "Date Detected": "2026-04-06",
            "Company Name": "Lanxess",
            "Signal Type": "News Article",
            "Signal Headline": "Lanxess announces reliability improvements and output optimization program",
            "AI Intent Score": 7,
            "AI Summary": "Optimization efforts can raise effective plant output, increasing the likelihood of incremental drum demand.",
        },
        {
            "Date Detected": "2026-04-06",
            "Company Name": "ExxonMobil Chemical",
            "Signal Type": "Job Posting",
            "Signal Headline": "Hiring Shift Supervisor for chemical blending operations",
            "AI Intent Score": 8,
            "AI Summary": "Shift leadership hiring often accompanies volume growth or operational scaling that requires additional packaging support.",
        },
        {
            "Date Detected": "2026-04-05",
            "Company Name": "Afton Chemical",
            "Signal Type": "Job Posting",
            "Signal Headline": "Plant hiring campaign for operators and maintenance technicians",
            "AI Intent Score": 10,
            "AI Summary": "Simultaneous hiring across operators and maintenance is a strong leading indicator of sustained production ramp-up and packaging need.",
        },
        {
            "Date Detected": "2026-04-05",
            "Company Name": "Chevron Oronite",
            "Signal Type": "Gov Permit",
            "Signal Headline": "Environmental filing references storage and handling upgrades in Pioneer",
            "AI Intent Score": 8,
            "AI Summary": "Storage and handling upgrades often support larger raw material or finished goods flows, which can drive demand for drums.",
        },
        {
            "Date Detected": "2026-04-04",
            "Company Name": "Arkema",
            "Signal Type": "News Article",
            "Signal Headline": "Arkema signals stronger regional demand from Southeast Asia customers",
            "AI Intent Score": 7,
            "AI Summary": "Rising regional demand can cascade into higher local production planning and more packaging consumption.",
        },
        {
            "Date Detected": "2026-04-04",
            "Company Name": "Croda Singapore",
            "Signal Type": "Job Posting",
            "Signal Headline": "Hiring warehouse and dispatch coordinator for Pioneer site",
            "AI Intent Score": 6,
            "AI Summary": "Warehouse and dispatch hiring is a useful secondary signal that product flow may be increasing.",
        },
        {
            "Date Detected": "2026-04-03",
            "Company Name": "Asahi Kasei",
            "Signal Type": "Gov Permit",
            "Signal Headline": "Utility upgrade submission linked to Jurong Island production asset",
            "AI Intent Score": 8,
            "AI Summary": "Utility upgrades are commonly associated with equipment additions or production support for higher output levels.",
        },
        {
            "Date Detected": "2026-04-03",
            "Company Name": "Brenntag Singapore",
            "Signal Type": "Job Posting",
            "Signal Headline": "Seeking operations executive for chemical distribution terminal",
            "AI Intent Score": 7,
            "AI Summary": "Operational headcount growth at a distribution terminal can indicate increased packaging turnover and refill activity.",
        },
        {
            "Date Detected": "2026-04-02",
            "Company Name": "Clariant",
            "Signal Type": "News Article",
            "Signal Headline": "Clariant references Singapore site as strategic supply point for Asia",
            "AI Intent Score": 8,
            "AI Summary": "Strategic supply hub positioning suggests higher throughput probability and stronger packaging requirements over time.",
        },
        {
            "Date Detected": "2026-04-01",
            "Company Name": "Celanese",
            "Signal Type": "Job Posting",
            "Signal Headline": "Hiring EHS and process support engineers for Jurong operations",
            "AI Intent Score": 7,
            "AI Summary": "Support engineering hires imply active investment in plant readiness, which may precede capacity expansion and packaging demand.",
        },
    ]

    df = pd.DataFrame(data)
    df["Date Detected"] = pd.to_datetime(df["Date Detected"])
    return df.sort_values("Date Detected", ascending=False).reset_index(drop=True)


# -----------------------------------------------------------
# Styling helpers
# -----------------------------------------------------------
def apply_theme() -> None:
    """Apply a lean corporate theme using blues and grays."""
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f7fa;
        }
        .stMetric {
            background-color: #ffffff;
            border: 1px solid #d9e2ec;
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(16, 24, 40, 0.08);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3 {
            color: #16324f;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------
# App layout and logic
# -----------------------------------------------------------
def main() -> None:
    apply_theme()
    df = load_mock_data()

    st.title("Pioneer Territory Lead Radar")
    st.caption("Leading indicator dashboard for chemical manufacturers in the Jurong / Pioneer region of Singapore.")

    # ---------------- Sidebar ----------------
    with st.sidebar:
        st.title("Pioneer Territory Lead Radar")
        st.markdown(
            """
            **About**

            This dashboard helps an Area Sales Manager track early signs that
            chemical manufacturers may be expanding production and may soon need
            more industrial packaging such as steel and plastic drums.
            """
        )

        company_options = sorted(df["Company Name"].unique())
        signal_options = sorted(df["Signal Type"].unique())

        selected_companies = st.multiselect(
            "Filter by Company Name",
            options=company_options,
            default=company_options,
        )

        selected_signal_types = st.multiselect(
            "Filter by Signal Type",
            options=signal_options,
            default=signal_options,
        )

        min_intent_score = st.slider(
            "Minimum Intent Score",
            min_value=1,
            max_value=10,
            value=6,
        )

    # ---------------- Filtering ----------------
    filtered_df = df[
        (df["Company Name"].isin(selected_companies))
        & (df["Signal Type"].isin(selected_signal_types))
        & (df["AI Intent Score"] >= min_intent_score)
    ].copy()

    # ---------------- KPI calculations ----------------
    total_signals = len(filtered_df)
    high_intent_leads = len(filtered_df[filtered_df["AI Intent Score"] >= 8])

    if not filtered_df.empty:
        top_company = (
            filtered_df.groupby("Company Name")["AI Intent Score"]
            .mean()
            .sort_values(ascending=False)
            .index[0]
        )
    else:
        top_company = "No matching leads"

    # ---------------- KPIs ----------------
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    kpi_col1.metric("Total Signals This Week", total_signals)
    kpi_col2.metric("High Intent Leads (Score 8+)", high_intent_leads)
    kpi_col3.metric("Top Expanding Company", top_company)

    st.markdown("---")

    # ---------------- Visualization ----------------
    st.subheader("Average Intent Score by Company")

    if not filtered_df.empty:
        chart_df = (
            filtered_df.groupby("Company Name", as_index=False)["AI Intent Score"]
            .mean()
            .sort_values("AI Intent Score", ascending=False)
        )

        fig = px.bar(
            chart_df,
            x="Company Name",
            y="AI Intent Score",
            color="AI Intent Score",
            color_continuous_scale=["#9fb3c8", "#486581", "#243b53"],
            text_auto=".1f",
        )
        fig.update_layout(
            height=420,
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(color="#243b53"),
            coloraxis_showscale=False,
            xaxis_title="Company",
            yaxis_title="Average Intent Score",
            margin=dict(l=20, r=20, t=30, b=80),
        )
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Avg Intent Score: %{y:.1f}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data matches the current filters.")

    st.markdown("---")

    # ---------------- Lead engine table ----------------
    st.subheader("Lead Engine")

    display_df = filtered_df[
        [
            "Date Detected",
            "Company Name",
            "Signal Type",
            "Signal Headline",
            "AI Intent Score",
        ]
    ].copy()

    if not display_df.empty:
        display_df["Date Detected"] = display_df["Date Detected"].dt.strftime("%Y-%m-%d")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Lead Details")
        for _, row in filtered_df.iterrows():
            label = f'{row["Date Detected"].strftime("%Y-%m-%d")} | {row["Company Name"]} | Score {row["AI Intent Score"]}'
            with st.expander(label):
                st.write(f"**Signal Type:** {row['Signal Type']}")
                st.write(f"**Headline:** {row['Signal Headline']}")
                st.write(f"**AI Summary:** {row['AI Summary']}")
    else:
        st.warning("No leads match the current filters. Adjust the sidebar filters to see more results.")


if __name__ == "__main__":
    main()
