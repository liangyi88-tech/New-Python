import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------
# Page configuration
# -----------------------------------------------------------
st.set_page_config(
    page_title="Downstream Client Tracker",
    page_icon="🔗",
    layout="wide",
)

# -----------------------------------------------------------
# Mock Data Generator (Simulating Annual Report Extraction)
# -----------------------------------------------------------
def load_client_data() -> pd.DataFrame:
    """
    Simulates a database of top clients extracted from annual and quarterly 
    reports of our target manufacturers.
    """
    data = [
        {
            "Manufacturer": "Greif",
            "Client Name": "Unilever APAC",
            "Sector": "FMCG",
            "Report Source": "2023 Annual Report",
            "Volume Trend": "Increasing 📈",
            "Est. Volume (Units)": 150000,
            "Extraction Notes": "Report notes a 15% increase in rigid packaging orders for Q4 to support new personal care line.",
        },
        {
            "Manufacturer": "Greif",
            "Client Name": "Bayer CropScience",
            "Sector": "Agriculture",
            "Report Source": "Q1 2024 Earnings Call",
            "Volume Trend": "Stable ➖",
            "Est. Volume (Units)": 85000,
            "Extraction Notes": "Contract renewed for 2024; purchase volume expected to remain flat year-over-year.",
        },
        {
            "Manufacturer": "SCGM Berhad",
            "Client Name": "Nestle Malaysia",
            "Sector": "Food & Beverage",
            "Report Source": "2023 Annual Report",
            "Volume Trend": "Increasing 📈",
            "Est. Volume (Units)": 220000,
            "Extraction Notes": "F&B expansion driving 20% higher thermoform packaging demand in the domestic market.",
        },
        {
            "Manufacturer": "SCGM Berhad",
            "Client Name": "Local Fresh Produce Co.",
            "Sector": "Agriculture",
            "Report Source": "Q3 2023 Filing",
            "Volume Trend": "Decreasing 📉",
            "Est. Volume (Units)": 30000,
            "Extraction Notes": "Client reduced orders due to poor crop yields; down 10% from previous quarter.",
        },
        {
            "Manufacturer": "Daibochi",
            "Client Name": "Mondelez International",
            "Sector": "Food & Beverage",
            "Report Source": "2023 Annual Report",
            "Volume Trend": "Increasing 📈",
            "Est. Volume (Units)": 310000,
            "Extraction Notes": "Secured new contract for sustainable flexible packaging lines across Southeast Asia.",
        },
        {
            "Manufacturer": "Dynapack Asia",
            "Client Name": "P&G Singapore",
            "Sector": "FMCG",
            "Report Source": "Investor Presentation 2024",
            "Volume Trend": "Increasing 📈",
            "Est. Volume (Units)": 180000,
            "Extraction Notes": "Highlighted as a key growth account; increasing rigid plastic bottle volumes by 12%.",
        },
        {
            "Manufacturer": "Vinda Singapore",
            "Client Name": "NTUC FairPrice",
            "Sector": "Retail",
            "Report Source": "2023 Annual Report",
            "Volume Trend": "Stable ➖",
            "Est. Volume (Units)": 500000,
            "Extraction Notes": "Consistent tissue and hygiene product supply; baseline volumes maintained.",
        }
    ]
    
    return pd.DataFrame(data)

# -----------------------------------------------------------
# App Layout and Logic
# -----------------------------------------------------------
def main():
    st.title("🔗 Downstream Client Volume Tracker")
    st.markdown("""
    Track the top clients of your target manufacturers (extracted from Annual/Quarterly reports). 
    Use this to identify if your prospects are experiencing downstream growth, which translates into an immediate need for your packaging solutions.
    """)
    
    df = load_client_data()
    
    # --- Filters ---
    st.sidebar.header("Filter Clients")
    selected_mfg = st.sidebar.multiselect(
        "Target Manufacturer:", 
        options=df["Manufacturer"].unique(),
        default=df["Manufacturer"].unique()
    )
    
    selected_trend = st.sidebar.multiselect(
        "Volume Trend:",
        options=df["Volume Trend"].unique(),
        default=df["Volume Trend"].unique()
    )
    
    filtered_df = df[(df["Manufacturer"].isin(selected_mfg)) & (df["Volume Trend"].isin(selected_trend))]
    
    # --- Top Level Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients Tracked", len(filtered_df))
    increasing_count = len(filtered_df[filtered_df["Volume Trend"] == "Increasing 📈"])
    col2.metric("Clients w/ Increasing Volume", increasing_count)
    col3.metric("Total Est. Volume (Units)", f"{filtered_df['Est. Volume (Units)'].sum():,}")
    
    st.divider()
    
    # --- Charts ---
    st.subheader("Client Volume Distribution")
    if not filtered_df.empty:
        fig = px.pie(filtered_df, names="Volume Trend", values="Est. Volume (Units)", color="Volume Trend",
                     color_discrete_map={"Increasing 📈": "#10b981", "Stable ➖": "#f59e0b", "Decreasing 📉": "#ef4444"})
        st.plotly_chart(fig, use_container_width=True)
    
    # --- Data Table ---
    st.subheader("Client Extraction Report")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()