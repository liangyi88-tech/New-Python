import os
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
    # This replaces your old mock function with a live connection to Google Search.
    search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    print(f"--- VolumeSignal Live Agent starting with {model_id} ---")
    print(f"Agent is querying the live internet for {company_name}... (this may take a few seconds)")

    # 3. Create a dynamic prompt for the Agent
    prompt = f"""
    Search the live web for recent news, earnings calls, or expansion signals regarding '{company_name}' in Southeast Asia or globally. 
    Based on the real-time data you find, analyze if they are currently a high-priority lead for our industrial drum sales team.
    """

    # 4. Run the Agent with the Search Tool attached
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[search_tool], # <-- This single line gives the AI internet access!
                temperature=0.2      # Keep it low so the AI sticks strictly to facts
            )
        )

        # 5. Transparency: Show exactly where the AI scraped the info from!
        sources = []
        candidate = response.candidates[0]
        if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
            for chunk in candidate.grounding_metadata.grounding_chunks:
                if hasattr(chunk, 'web') and chunk.web:
                    sources.append({"title": chunk.web.title, "uri": chunk.web.uri})
                    
        return response.text, sources
        
    except Exception as e:
        return f"Agent Error: {str(e)}", []

# If you run this file directly in the terminal, it will test the function:
if __name__ == "__main__":
    analysis, sources_found = run_live_search_agent("Greif packaging")
    
    print("\n--- FINAL SALES INTELLIGENCE (LIVE DATA) ---")
    print(analysis)
    
    if sources_found:
        print("\n--- SOURCES SCRAPED ---")
        for s in sources_found:
            print(f"- {s['title']}\n  Link: {s['uri']}")