# pages/01_🌍_Global_Intelligence.py
import streamlit as st
import sqlite3
from app.database import get_global_news, get_news_sources

st.set_page_config(page_title="Global Intelligence",
                   page_icon="🌍", layout="wide")

# --- HEADER & NAVIGATION ---
st.title("🌍 Global Intelligence Feed")
st.caption("AI-Translated & Analyzed Geopolitical Streams")

# 1. Fetch available sources dynamically (e.g., "China_Xinhua", "Russia_Kommersant")
try:
    available_sources = get_news_sources()
except sqlite3.OperationalError:
    available_sources = []
    st.error("⚠️ Database not found. Run 'python run_news.py' first.")

# 2. Create Filters
# Add "All" to the start of the list
filter_options = ["All"] + available_sources

selected_source = st.pills(
    "Filter by Source Channel",
    filter_options,
    default="All",
    selection_mode="single"
)

st.divider()

# --- CONTENT STREAM ---
try:
    # Fetch data based on selection
    news_items = get_global_news(source_filter=selected_source)

    if not news_items:
        st.info(
            "No intelligence reports found. Run the ingestion script to gather data.")

    for item in news_items:
        with st.container(border=True):
            # Layout: Title & Metadata on top
            st.subheader(item['title'])

            # Color-coded metadata badge logic (Optional visual flair)
            if "China" in item['source']:
                flag = "🇨🇳"
            elif "Russia" in item['source']:
                flag = "🇷🇺"
            else:
                flag = "🏳️"

            st.caption(f"{flag} **{item['source']}** • 📅 {item['added_date']}")

            # The AI Analysis (Summary)
            # This contains the Translation, Summary, and Analyst Note
            st.markdown("### 🧠 Analyst Briefing")
            st.markdown(item['summary'])

            # Link to original
            st.markdown(f"🔗 [Original Source Material]({item['link']})")

except Exception as e:
    st.error(f"Error loading feed: {e}")
