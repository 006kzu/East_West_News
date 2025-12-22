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
DEV_MODE = False
# ---------------------

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

VIP_VENUES = [
    "Nature", "Science", "Cell", "The Lancet", "New England Journal of Medicine",
    "JAMA", "IEEE", "NeurIPS", "ICML", "CVPR", "ArXiv"
]


class QuickPaperReview(BaseModel):
    score: int = Field(
        description="Score 1-10 based on wider population impact.")
    is_major: bool = Field(
        description="True ONLY if the research fundamentally changes how we interact with the world.")
    layman_summary: str = Field(
        description="A catchy, 1-sentence news-style headline focusing on the real-world benefit.")
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
    current_year = datetime.datetime.now().year
    year_range = f"{current_year-1}-{current_year}"

    params = {
        "query": topic,
        "year": year_range,
        "sort": "publicationDate:desc",
        "fields": "title,abstract,url,publicationDate,venue,authors",
        "limit": limit
    }
    return fetch_with_retry(url, params)


def evaluate_paper(paper):
    if not paper.get('abstract'):
        return None

    venue = paper.get('venue') or "Unknown"

    prompt = f"""
    You are a ruthless Scientific Editor for "Peripheral News."
    Your Goal: Prioritize the reader's time by filtering out insignificant research.

    ### THE GOLDEN RULE OF SIGNIFICANCE
    To determine if a paper is worth reading, you must ask this specific question:
    "Does this impact affect the population OUTSIDE of this specific domain, or does it help experts in this domain DIRECTLY impact the outside population?"

    ### SCORING RUBRIC (1-10)
    
    **SCORES 1-5: INSIGNIFICANT (REJECT)**
    - Criteria: The impact is trapped inside the domain.
    - Examples: Incremental tweaks to algorithms, pure simulations with no real-world tether, theoretical proofs without application, or student-level reviews.
    - Action: If it doesn't pass the Golden Rule, give it a low score so it is filtered out.

    **SCORE 6: DOMAIN RELEVANT (BORDERLINE)**
    - Criteria: Solid science, but the downstream impact on humanity is vague or too distant.
    
    **SCORE 7: IMPACTFUL (PUBLISH)**
    - Criteria: Clear potential to affect the outside world.
    - Example: A new material that *could* make batteries 20% cheaper, or a drug target that *might* cure a rare disease.

    **SCORES 8-10: TRANSFORMATIVE (MAJOR INNOVATION)**
    - Criteria: A breakthrough that will undeniably change safety, health, energy, or understanding of the universe for the general public.
    - Example: Research on Earth's core (like the Nature s41586-024-08322-y paper) that enables better earthquake prediction. This saves lives.
    - Example: A fusion reactor achieving net gain. This changes energy forever.

    ### YOUR TASK
    Analyze the paper below. If it is "Insignificant," score it low (1-5). If it passes the Golden Rule, score it high (7+).
    
    Paper Data:
    - Title: {paper['title']}
    - Venue: {venue}
    - Abstract: {paper['abstract']}
    
    Output JSON.
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
