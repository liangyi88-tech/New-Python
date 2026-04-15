import streamlit as st
from datetime import datetime, timedelta

# 1. Page Setup
st.set_page_config(page_title="Market News", page_icon="📰", layout="wide")

st.title("📰 Market Intelligence Feed")
st.markdown("Latest signals on packaging materials, sales volumes, and production growth.")
st.divider()

# 2. Keyword Filter (The UI)
st.sidebar.header("Filter Signals")
keywords = ["Packaging", "Growth", "Volume", "Sales", "Production", "Expansion"]
selected_keywords = st.sidebar.multiselect("Select Keywords to track:", keywords, default=["Growth", "Volume"])

# 3. Simulated Data Engine (Later, your Gemini Agent will feed this!)
# We use mock data here to test the layout immediately.
news_data = [
    {
        "title": "Greif Announces Major Q3 Production Volume Increase in APAC",
        "source": "Company Announcement",
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "tags": ["Growth", "Volume", "Packaging"],
        "summary": "Greif's recent quarterly report indicates a 15% surge in industrial packaging volume across Singapore and Malaysia due to chemical sector demands."
    },
    {
        "title": "SCGM Berhad expands chemical-safe packaging lines",
        "source": "LinkedIn Post (Industry Analyst)",
        "date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "tags": ["Expansion", "Production", "Packaging"],
        "summary": "Noticed high hiring activity for floor operators at the Johor plant. Looks like a new production line is going live next month."
    },
    {
        "title": "Petrochemical Export Sales Hit Record High in SG",
        "source": "Business Times News",
        "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "tags": ["Sales", "Growth"],
        "summary": "A massive surge in export sales means downstream suppliers (drums, IBCs) will likely see increased order books for the rest of the year."
    }
]

# 4. Filter Logic
filtered_news = [
    item for item in news_data 
    if any(tag in selected_keywords for tag in item["tags"])
]

# 5. Display the Feed
if not filtered_news:
    st.info("No recent news matches your selected keywords.")
else:
    for item in filtered_news:
        # Create a visual "Card" for each news item
        with st.container():
            st.subheader(item["title"])
            st.caption(f"**Source:** {item['source']}  |  **Date:** {item['date']}")
            
            # Show tags as little colored blocks
            tag_string = " ".join([f"`{tag}`" for tag in item["tags"]])
            st.markdown(tag_string)
            
            st.write(item["summary"])
            
            # Add a functional button for the future
            if st.button(f"Analyze Lead Potential", key=item["title"]):
                st.success("Agent dispatched! (This will trigger Gemini to update your lead score soon.)")
            
            st.divider()