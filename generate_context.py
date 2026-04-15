import json
import os
from google import genai
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Use Flash to bypass the quota error!
model_id = "gemini-2.5-flash"

print("Asking Gemini to generate market context...")

# 3. Give it strict instructions to output ONLY code
prompt = """
Generate a JSON list of 3 major chemical or manufacturing companies in Singapore/Malaysia that would be good leads for industrial packaging (drums).
Include the exact keys: "company", "location", "last_score" (a number from 1 to 100), and "notes".
Output ONLY valid JSON, without any markdown formatting or explanations.
"""

response = client.models.generate_content(
    model=model_id,
    contents=prompt,
)

# 4. Clean up the AI's text and save it as a file
try:
    # Sometimes AI adds ```json at the start, this cleans it up
    clean_text = response.text.strip().replace('```json', '').replace('```', '')
    
    # Verify it is valid JSON
    data = json.loads(clean_text)
    
    # Create the actual file on your hard drive
    with open("leads.json", "w") as file:
        json.dump(data, file, indent=4)
        
    print("\nSUCCESS! 'leads.json' has been created in your folder.")
    print("Check your VS Code file explorer on the left.")

except Exception as e:
    print(f"Failed to create file. Error: {e}")
    print("Raw output was:", response.text)