import streamlit as st
from app.database import get_global_news

# 1. Page Config
st.set_page_config(
    page_title="Peripheral News",
    page_icon="🌍",
    layout="wide"
)

# 2. Sidebar (Info Only)
with st.sidebar:
    st.title("🌍 Peripheral News")
    st.markdown("Automated intelligence on the things that matter.")
    st.divider()
    st.info("💡 **Tip:** Go to the 'Academic Feed' page in the sidebar to see scientific papers.")

# 3. Main Dashboard
st.title("🗺️ Global Intelligence Brief")
st.markdown(
    "Daily analysis of foreign media (Russia/China) translated and summarized for Western context.")
st.divider()

# 4. Fetch Data from DB (Instant Load!)
news_items = get_global_news(limit=20)

if not news_items:
    st.warning(
        "⚠️ Database is empty. Please run `python run_news.py` in your terminal first.")
else:
    # 5. Display News Cards
    for item in news_items:
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                # Icon based on Source
                icon = "🐻" if "Kommersant" in item['source'] else "🐉"
                st.subheader(f"{icon} {item['source']}: {item['title']}")
                st.caption(
                    f"📅 Added: {item['added_date']} | 🔗 [Original Source]({item['link']})")

                # The Analysis
                st.markdown(item['summary'])

            with col2:
                # Placeholder for future metadata tags
                st.empty()

            st.divider()
