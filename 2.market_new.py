import streamlit as st
# 1. Import your newly upgraded AI engine!
from volume_agent import run_live_search_agent 

st.title("📰 Market Intelligence Feed")
st.write("Latest signals on packaging materials, sales volumes, and production growth in SG/MY.")

# Your CRM target list (Keeping it to 3 for a quick test so you don't wait too long)
tracked_companies = ["Greif", "SCGM Berhad", "Kimball Electronics"]

# 2. Add a trigger button. 
# We use a button because live web searching takes 5-10 seconds per company. 
# You don't want Streamlit to freeze every time you navigate pages!
if st.button("Fetch Live Web Signals"):
    
    with st.spinner("Agents are scouring the live web for your clients..."):
        
        # 3. Loop through your companies and run the AI
        for company in tracked_companies:
            analysis_json, sources = run_live_search_agent(company)
            
            # 4. Build the Streamlit UI Cards using the JSON data
            if "error" not in analysis_json:
                with st.container():
                    # The dynamic headline
                    st.subheader(analysis_json.get('feed_headline', f"Live Update: {company}"))
                    
                    # Make the scraped sources clickable links!
                    if sources:
                        source_links = " | ".join([f"[{s['title']}]({s['uri']})" for s in sources[:2]])
                        st.caption(f"🤖 AI Live Search | Sources: {source_links}")
                    else:
                        st.caption("🤖 AI Live Search")
                    
                    # Tags
                    tags = analysis_json.get('tags', [])
                    st.write(" • ".join(tags))
                    
                    # The Summary and the Impact
                    st.write(analysis_json.get('summary', ''))
                    st.success(f"**Packaging Impact:** {analysis_json.get('packaging_impact', '')}")
                    
                    # The action button
                    st.button(f"Analyze Lead Potential", key=f"btn_{company}")
                    
                    st.markdown("---")
            else:
                st.error(f"Could not fetch data for {company}. Check terminal for errors.")