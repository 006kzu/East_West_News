import os
from google import genai
from dotenv import load_dotenv

# 1. LOAD ENV VARS
load_dotenv()

# 2. DEFINE CLIENT (Global Scope)
# This line must be all the way to the left!
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 3. DEFINE FUNCTION


def analyze_article(article):
    """
    Analyzes a news article using the new Google Gen AI SDK.
    """

    prompt = f"""
    You are an expert Foreign Intelligence Analyst.

    Analyze the following news snippet from {article['source']}:

    Original Title: {article['title']}
    Original Content: {article['summary']}

    Please provide:
    1. A clear English translation of the headline.
    2. A 2-sentence summary of the core message.
    3. An "Analyst Note" on any cultural context, bias, or hidden meaning.

    Format the output clearly.
    """

    try:
        # Since 'client' is defined globally above, the function can "see" it.
        # In app/analysis.py
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Error analyzing article: {e}"
