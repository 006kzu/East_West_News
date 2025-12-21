import streamlit as st
import time
from app.ingestion import fetch_latest_news
from app.analysis import analyze_article

# 1. Page Config (Tab title, icon)
st.set_page_config(page_title="Peripheral News", page_icon="🌍")

# 2. Header Section
st.title("🌍 Peripheral News")
st.markdown("""
**Objective:** Bridge the information gap by translating and analyzing news from **China** and **Russia** for Western readers.
""")

# 3. The "Run" Button
if st.button("🔄 Fetch & Analyze Latest News"):

    # Create a placeholder for status updates
    status_text = st.empty()
    progress_bar = st.progress(0)

    # Step 1: Ingestion
    status_text.text("📡 Contacting foreign RSS feeds...")
    # Get 3 articles total for the demo
    raw_articles = fetch_latest_news(limit=3)

    if not raw_articles:
        st.error("No articles found. Please check your connection.")
    else:
        st.success(
            f"Found {len(raw_articles)} articles. Beginning analysis...")
        time.sleep(1)  # Visual pause

        # Step 2: Analysis Loop
        for i, article in enumerate(raw_articles):
            # Update status
            status_text.text(
                f"🧠 Analyzing article {i+1}/{len(raw_articles)}: {article['title'][:30]}...")
            progress_bar.progress((i) / len(raw_articles))

            # Run the specific analysis
            # We use a spinner so the user knows it's working
            with st.spinner(f"Reading {article['source']}..."):
                analysis = analyze_article(article)

            # Step 3: Display Results nicely
            with st.expander(f"{article['source']}: {article['title']}", expanded=True):
                st.markdown(analysis)
                st.markdown(f"[🔗 Read Original Source]({article['link']})")

            # Rate Limit Protection (Vital for Free Tier!)
            time.sleep(4)

        progress_bar.progress(100)
        status_text.text("✅ Briefing Complete.")
