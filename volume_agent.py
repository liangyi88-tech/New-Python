import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

def run_live_search_agent(company_name: str):
    # 1. Setup
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # We use gemini-2.5-pro for deep reasoning and live search capabilities
    model_id = "gemini-2.5-pro" 

    # 2. Enable Google Search (The "Agentic Internet" Tool)
    search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    print(f"--- VolumeSignal Live Agent starting with {model_id} ---")
    print(f"Agent is querying the live internet for {company_name}... (this may take a few seconds)")

    # 3. Create a dynamic prompt for the Agent to return JSON
    prompt = f"""
    Search the live web for recent news, earnings calls, or expansion signals regarding '{company_name}' in Southeast Asia or globally. 
    Based on the real-time data you find, analyze if they are currently a high-priority lead for our industrial drum and packaging sales team.
    
    You MUST respond STRICTLY in the following JSON format. Do not include markdown formatting like ```json or any extra text outside the brackets:
    {{
        "company": "{company_name}",
        "feed_headline": "A short 1-line headline summarizing the latest news",
        "tags": ["Packaging", "Growth", "Volume"], 
        "summary": "A 2-sentence summary of what you found focusing on expansion or production.",
        "packaging_impact": "Explain how this impacts their packaging volume requirements.",
        "estimated_lead_temperature": "Cold, Warm, or Hot"
    }}
    """

    # 4. Run the Agent with the Search Tool attached
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[search_tool], # <-- This gives the AI internet access
                temperature=0.2      # <-- Low temp so it sticks to facts
            )
        )

        # 5. Transparency: Show exactly where the AI scraped the info from!
        sources = []
        candidate = response.candidates[0]
        if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
            for chunk in candidate.grounding_metadata.grounding_chunks:
                if hasattr(chunk, 'web') and chunk.web:
                    sources.append({"title": chunk.web.title, "uri": chunk.web.uri})
                    
        # 6. Clean and Parse the JSON output safely
        # We strip backticks just in case the AI ignores the "no markdown" rule
        clean_text = response.text.strip().replace('```json', '').replace('```', '')
        ai_data = json.loads(clean_text)
                    
        return ai_data, sources
        
    except Exception as e:
        print(f"Agent Error for {company_name}: {str(e)}")
        # Return a fallback JSON object so the app doesn't crash
        return {"company": company_name, "error": str(e)}, []

# --- TESTING THE LOOP ---
# If you run this file directly in the terminal, it will test the function:
if __name__ == "__main__":
    
    # Your full list of tracked companies
    tracked_companies = [
        "Kimball Electronics", "Greif", "V.S. Industry", 
        "SCGM Berhad", "Daibochi", "Dynapack Asia", 
        "Briggs Packaging", "Vinda Singapore"
    ]
    
    # Let's test just the first 2 companies so you don't have to wait too long
    print("\nStarting multi-company sweep...\n")
    
    for target_company in tracked_companies[:2]: 
        analysis, sources_found = run_live_search_agent(target_company)
        
        print(f"\n--- FINAL SALES INTELLIGENCE ({target_company}) ---")
        print(json.dumps(analysis, indent=4))
        
        if sources_found:
            print("\n--- SOURCES SCRAPED ---")
            for s in sources_found:
                print(f"- {s['title']}\n   Link: {s['uri']}")
                
        print("\n" + "="*60 + "\n")