import streamlit as st
import sqlite3
from app.database import get_feed
from app.topics import TOPIC_HUBS

st.set_page_config(page_title="Academic Feed", page_icon="🎓", layout="wide")

st.title("🎓 Peripheral Academic Watch")
st.markdown(
    "Artificial Intelligence curation of the latest major scientific findings.")

# 1. The Sidebar Filter
# We use the "Hubs" to make a nice two-step selection
selected_hub = st.sidebar.radio("Select Field Group", list(TOPIC_HUBS.keys()))
selected_topic = st.sidebar.selectbox(
    "Select Specific Topic", TOPIC_HUBS[selected_hub])

st.divider()
st.subheader(f"Latest in {selected_topic}")

try:
    # 2. Get Data for the selected topic
    papers = get_feed(selected_topic)

    if not papers:
        st.info(
            f"No major breakthroughs detected in {selected_topic} yet. Check back tomorrow!")

    # 3. Display Papers
    for paper in papers:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {paper['title']}")
                st.caption(
                    f"📅 {paper['published_date']} | Score: **{paper['score']}/10**")

                # Color code the score
                if paper['score'] >= 8:
                    st.success(f"🌟 **MAJOR FINDING:** {paper['summary']}")
                else:
                    st.info(f"**Summary:** {paper['summary']}")

            with col2:
                st.markdown(f"[**Read Full Paper**]({paper['url']})")
                if paper['is_major']:
                    st.write("🔥 Highly Innovative")

            st.divider()

except sqlite3.OperationalError:
    st.error("⚠️ Database not found. Please run the scout script.")
