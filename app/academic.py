import requests
import datetime
import os
import time
import random
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
DEV_MODE = False  # Set to False since your API keys are working
# ---------------------

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

VIP_VENUES = [
    "Nature", "Science", "Cell", "The Lancet", "New England Journal of Medicine",
    "JAMA", "IEEE", "NeurIPS", "ICML", "CVPR", "ArXiv"
]


class QuickPaperReview(BaseModel):
    score: int = Field(description="Score 1-10 based on innovation.")
    # RENAMED BACK TO MATCH DATABASE:
    is_major: bool = Field(
        description="True if from a top-tier journal or highly cited.")
    # RENAMED BACK TO MATCH DATABASE:
    layman_summary: str = Field(
        description="A catchy, 1-sentence news-style headline.")
    category: str = Field(description="The specific sub-field.")


def fetch_with_retry(url, params, retries=5, backoff_factor=2):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json().get('data', [])
            elif response.status_code == 429:
                wait = (backoff_factor ** attempt) + random.uniform(0, 1)
                print(f"      ⚠️ Rate limited. Waiting {wait:.1f}s...")
                time.sleep(wait)
            else:
                return []
        except Exception:
            return []
    return []


def fetch_latest_papers(topic="Artificial Intelligence", limit=20):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    # Calculate current year range (e.g., "2024-2025")
    current_year = datetime.datetime.now().year
    year_range = f"{current_year-1}-{current_year}"

    params = {
        "query": topic,
        "year": year_range,           # <--- STRICT FILTER (Fixes the 2011 bug)
        "sort": "publicationDate:desc",  # <--- Keeps sorting by newest
        "fields": "title,abstract,url,publicationDate,venue,authors",
        "limit": limit
    }
    return fetch_with_retry(url, params)


def evaluate_paper(paper):
    if not paper.get('abstract'):
        return None

    venue = paper.get('venue') or "Unknown"

    # --- MOCK MODE (Matches DB Schema) ---
    if DEV_MODE:
        return {
            "score": 8,
            "is_major": True,          # Fixed key name
            # Fixed key name
            "layman_summary": f"[MOCK] {paper['title'][:50]}...",
            "category": "Dev Test"
        }
    # -------------------------------------

    prompt = f"""
    You are a science news editor. Write a clickable headline for this paper.
    
    Title: {paper['title']}
    Venue: {venue}
    Abstract: {paper['abstract']}
    """

    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': QuickPaperReview,
            }
        )
        return response.parsed.model_dump()
    except Exception as e:
        print(f"Review failed: {e}")
        return None
