import streamlit as st
import pandas as pd
import json
import os
import time 
from volume_agent import run_live_search_agent
from datetime import datetime
import plotly.express as px

# Page config
st.set_page_config(
    page_title="VolumeSignal | Manufacturing Client Acquisition",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom styling
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .score-high {
        background-color: #10b981;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    .score-medium {
        background-color: #f59e0b;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    .score-low {
        background-color: #ef4444;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Fallback data
fallback_companies = [
    {
        "name": "Greif",
        "country": "Malaysia",
        "city": "Shah Alam",
        "recentJobs": 16,
        "productionShare": 0.69,
        "logisticsShare": 0.18,
        "recencyDays": 5,
        "source": "Public jobs / careers signals",
        "summary": "Strong operations and plant hiring suggests packaging and industrial throughput expansion in Malaysia.",
    },
    {
        "name": "SCGM Berhad",
        "country": "Malaysia",
        "city": "Kulai",
        "recentJobs": 12,
        "productionShare": 0.74,
        "logisticsShare": 0.11,
        "recencyDays": 7,
        "source": "Public jobs / careers signals",
        "summary": "Manufacturing and shift-based openings indicate active production demand with local packaging relevance.",
    },
    {
        "name": "Daibochi",
        "country": "Malaysia",
        "city": "Melaka",
        "recentJobs": 11,
        "productionShare": 0.72,
        "logisticsShare": 0.14,
        "recencyDays": 8,
        "source": "Public jobs / careers signals",
        "summary": "Hiring mix points to capacity support across flexible packaging and plant execution roles.",
    },
    {
        "name": "Dynapack Asia",
        "country": "Singapore",
        "city": "Singapore",
        "recentJobs": 9,
        "productionShare": 0.62,
        "logisticsShare": 0.2,
        "recencyDays": 6,
        "source": "Public jobs / careers signals",
        "summary": "Regional packaging footprint and fresh hiring activity suggest near-term operating momentum.",
    },
    {
        "name": "Kimball Electronics",
        "country": "Malaysia",
        "city": "Penang",
        "recentJobs": 18,
        "productionShare": 0.66,
        "logisticsShare": 0.17,
        "recencyDays": 4,
        "source": "Public jobs / careers signals",
        "summary": "Electronics manufacturing ramp indicators can correlate with stronger industrial packaging requirements.",
    },
    {
        "name": "V.S. Industry",
        "country": "Malaysia",
        "city": "Senai",
        "recentJobs": 14,
        "productionShare": 0.71,
        "logisticsShare": 0.15,
        "recencyDays": 9,
        "source": "Public jobs / careers signals",
        "summary": "High proportion of production and plant roles suggests throughput support and supplier opportunity.",
    },
    {
        "name": "Vinda Singapore",
        "country": "Singapore",
        "city": "Singapore",
        "recentJobs": 7,
        "productionShare": 0.48,
        "logisticsShare": 0.28,
        "recencyDays": 10,
        "source": "Public jobs / careers signals",
        "summary": "Consumer goods hiring is moderate but distribution support roles may imply increased packaging movement.",
    },
    {
        "name": "Briggs Packaging",
        "country": "Malaysia",
        "city": "Johor Bahru",
        "recentJobs": 8,
        "productionShare": 0.64,
        "logisticsShare": 0.19,
        "recencyDays": 11,
        "source": "Public jobs / careers signals",
        "summary": "Consistent operational hiring makes this a relevant target for packaging supply conversations.",
    },
]

def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))

def score_company(company):
    """Score a company based on hiring signals"""
    hiring_score = clamp(company["recentJobs"] / 20, 0, 1) * 45
    production_score = company["productionShare"] * 30
    logistics_score = company["logisticsShare"] * 10
    recency_score = clamp((30 - company["recencyDays"]) / 30, 0, 1) * 10
    region_score = 5 if company["country"] in ["Singapore", "Malaysia"] else 0
    
    total = round(hiring_score + production_score + logistics_score + recency_score + region_score)
    
    return {
        **company,
        "score": total,
        "outlook": "High" if total >= 75 else "Medium" if total >= 55 else "Low"
    }

def load_companies():
    """Load companies from leads.json or use fallback"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "client-acquisition-site", "leads.json")
        with open(json_path, "r") as f:
            companies = json.load(f)
            if isinstance(companies, list) and len(companies) > 0:
                return sorted([score_company(c) for c in companies], key=lambda x: x["score"], reverse=True)
    except Exception as e:
        st.warning(f"Could not load leads.json: {e}. Using fallback data.")
    
    return sorted([score_company(c) for c in fallback_companies], key=lambda x: x["score"], reverse=True)

# Load data
companies = load_companies()

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

client_df = load_client_data()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["VolumeSignal Leads", "Client Volume Tracker", "Market Intelligence"])

st.sidebar.divider()

if page == "VolumeSignal Leads":
    # Header
    st.title("📊 VolumeSignal")
    st.markdown("**Manufacturing Client Acquisition Dashboard**")
    st.markdown("Identify manufacturers in Singapore and Malaysia likely increasing production volume using hiring signals.")

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    search_query = st.sidebar.text_input("Search by company name, country, or city:", "").lower()
    region_filter = st.sidebar.selectbox("Region:", ["All", "Singapore", "Malaysia"])

    # Filter data
    filtered = companies
    if search_query:
        filtered = [
            c for c in filtered
            if search_query in c["name"].lower()
            or search_query in c["country"].lower()
            or search_query in c["city"].lower()
        ]

    if region_filter != "All":
        filtered = [c for c in filtered if c["country"] == region_filter]

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    top_company = filtered[0] if filtered else None
    avg_score = round(sum(c["score"] for c in filtered) / len(filtered)) if filtered else 0

    with col1:
        st.metric("Total Companies", len(filtered))

    with col2:
        st.metric("Average Score", avg_score)

    with col3:
        if top_company:
            st.metric("Top Company", top_company["name"])
        else:
            st.metric("Top Company", "—")

    with col4:
        if top_company:
            st.metric("Recent Jobs", top_company["recentJobs"])
        else:
            st.metric("Recent Jobs", "—")

    # Display as table
    st.subheader("📋 Lead Dashboard")

    if filtered:
        # Prepare dataframe
        df_display = pd.DataFrame([
            {
                "Company": c["name"],
                "Country": c["country"],
                "City": c["city"],
                "Recent Jobs": c["recentJobs"],
                "Production Share": f"{round(c['productionShare'] * 100)}%",
                "Score": c["score"],
                "Outlook": c["outlook"]
            }
            for c in filtered
        ])
        
        st.dataframe(df_display, use_container_width=True)
        
        # Display detailed cards
        st.subheader("📌 Company Details")
        
        for company in filtered:
            with st.expander(f"**{company['name']}** (Score: {company['score']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Country", company["country"])
                    st.metric("City", company["city"])
                
                with col2:
                    st.metric("Recent Jobs", company["recentJobs"])
                    st.metric("Production Share", f"{round(company['productionShare'] * 100)}%")
                
                with col3:
                    st.metric("Logistics Share", f"{round(company['logisticsShare'] * 100)}%")
                    st.metric("Freshness (days)", company["recencyDays"])
                
                st.write(f"**Summary:** {company['summary']}")
                st.write(f"**Source:** {company['source']}")
                st.write(f"**Outlook:** {company['outlook']} probability of manufacturing volume increase")

    else:
        st.info("No companies match the current filters.")

elif page == "Client Volume Tracker":
    st.title("🔗 Client Volume Tracker")
    st.markdown("""
    Track the top clients of your target manufacturers (extracted from Annual/Quarterly reports). 
    Use this to identify if your prospects are experiencing downstream growth, which translates into an immediate need for your packaging solutions.
    """)
    
    # --- Filters ---
    st.sidebar.header("🔍 Filters")
    selected_mfg = st.sidebar.multiselect(
        "Target Manufacturer:", 
        options=client_df["Manufacturer"].unique(),
        default=client_df["Manufacturer"].unique()
    )
    
    selected_trend = st.sidebar.multiselect(
        "Volume Trend:",
        options=client_df["Volume Trend"].unique(),
        default=client_df["Volume Trend"].unique()
    )
    
    filtered_client_df = client_df[
        (client_df["Manufacturer"].isin(selected_mfg)) & 
        (client_df["Volume Trend"].isin(selected_trend))
    ]
    
    # --- Top Level Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients Tracked", len(filtered_client_df))
    increasing_count = len(filtered_client_df[filtered_client_df["Volume Trend"] == "Increasing 📈"])
    col2.metric("Clients w/ Increasing Volume", increasing_count)
    col3.metric("Total Est. Volume (Units)", f"{filtered_client_df['Est. Volume (Units)'].sum():,}")
    
    st.divider()
    
    # --- Charts ---
    st.subheader("Client Volume Distribution")
    if not filtered_client_df.empty:
        fig = px.pie(
            filtered_client_df, 
            names="Volume Trend", 
            values="Est. Volume (Units)", 
            color="Volume Trend",
            color_discrete_map={
                "Increasing 📈": "#10b981", 
                "Stable ➖": "#f59e0b", 
                "Decreasing 📉": "#ef4444"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data matches the current filters.")
    
    # --- Data Table ---
    st.subheader("Client Extraction Report")
    st.dataframe(filtered_client_df, use_container_width=True, hide_index=True)

# Data refresh info
# Data refresh info
elif page == "Market Intelligence":
    st.title("📰 Market Intelligence Feed")
    st.markdown("Latest live AI signals on packaging materials, sales volumes, and production growth.")
    st.divider()

    # Your CRM target list
    tracked_companies = [
        "Kimball Electronics", "Greif", "V.S. Industry", 
        "SCGM Berhad", "Daibochi", "Dynapack Asia", 
        "Briggs Packaging", "Vinda Singapore"
    ]

    st.info("Click below to dispatch your AI agent to search the live web for recent signals.")

    # The Live Fetch Button
    if st.button("🤖 Fetch Live Web Signals"):
        
        with st.spinner("Agents are scouring the live web for your clients (this may take a minute)..."):
            
            # Loop through your companies and run the AI
            for company in tracked_companies:
                analysis_json, sources = run_live_search_agent(company)
                
                # Build the Streamlit UI Cards using the JSON data
                if "error" not in analysis_json:
                    with st.container(border=True):
                        # The dynamic headline
                        st.subheader(analysis_json.get('feed_headline', f"Live Update: {company}"))
                        
                        # Make the scraped sources clickable links
        if st.button("🤖 Fetch Live Web Signals"):
                
                with st.spinner("Agents are scouring the live web... (Pausing between searches to avoid rate limits)"):
                    
                    for index, company in enumerate(tracked_companies):
                        # 1. Run the AI Agent
                        analysis_json, sources = run_live_search_agent(company)
                        
                        # 2. Display the result
                        if "error" not in analysis_json:
                            with st.container(border=True):
                                st.subheader(analysis_json.get('feed_headline', company))
                                # ... rest of your display code ...
                        else:
                            # UPDATED: Show the actual error so you can debug!
                            st.error(f"Error for {company}: {analysis_json['error']}")
                        
                        # 3. PAUSE to respect the 5 RPM limit (except after the last item)
                        if index < len(tracked_companies) - 1:
                            time.sleep(12)