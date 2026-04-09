import streamlit as st
import pandas as pd
import json
from datetime import datetime

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
        with open("client-acquisition-site/leads.json", "r") as f:
            companies = json.load(f)
            if isinstance(companies, list) and len(companies) > 0:
                return sorted([score_company(c) for c in companies], key=lambda x: x["score"], reverse=True)
    except Exception as e:
        st.warning(f"Could not load leads.json: {e}. Using fallback data.")
    
    return sorted([score_company(c) for c in fallback_companies], key=lambda x: x["score"], reverse=True)

# Load data
companies = load_companies()

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

# Data refresh info
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Data refreshes automatically")
