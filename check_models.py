import os
from google import genai
from dotenv import load_dotenv

# 1. Load env vars
load_dotenv()

# 2. Setup Client (New Way)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Checking available models...")

try:
    # 3. List models using the new client method
    # The new SDK returns a pager, so we iterate through it
    for model in client.models.list():
        # We only care about models we can use for generating text
        print(f"- {model.name}")

except Exception as e:
    print(f"❌ Error: {e}")
