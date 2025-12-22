import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from app.database import get_feed
from app.topics import TOPIC_HUBS

st.set_page_config(page_title="Academic Feed", page_icon="🎓", layout="wide")

# --- HELPER: MINIATURE RING CHART (PURE ALTAIR) ---


def make_impact_ring(score):
    # 1. The Data for the Ring
    source = pd.DataFrame({
        "Category": ["Impact", "Rest"],
        "Value": [score, 10-score]
    })

    base = alt.Chart(source).encode(
        theta=alt.Theta("Value", stack=True)
    )

    # 2. Layer 1: The Ring (Arc)
    pie = base.mark_arc(innerRadius=15, outerRadius=20).encode(
        color=alt.Color("Category",
                        scale=alt.Scale(domain=["Impact", "Rest"],
                                        range=["#008080", "#E5E4E2"]),
                        legend=None),
        order=alt.Order("Category", sort="descending")
    )

    # 3. Layer 2: The Score (Number in Center)
    # We render this on top of the 'base' so it stays centered
    text_score = base.mark_text(radius=0, size=12, color="#004225", fontStyle="bold").encode(
        text=alt.value(f"{score}")
    )

    # 4. Layer 3: The Label (Subtitle)
    # We create a new independent chart layer just for the "Impact Score" text
    # This avoids parsing the text multiple times for each slice of the pie
    label_df = pd.DataFrame({"label": ["Impact Score"]})
    text_label = alt.Chart(label_df).mark_text(
        align='center',
        dy=32,           # Shift text down (pixels) to sit below the ring
        size=8,
        color="#888",
        lineHeight=10    # Tighter line spacing if we split text (optional)
    ).encode(
        text='label'
    )

    # Combine all layers
    # We increase the height (e.g. 75) to ensure the bottom label isn't cut off
    return (pie + text_score + text_label).properties(width=50, height=75)


# --- SIDEBAR ---
with st.sidebar:
    st.page_link("app.py", label="Back to Dashboard", icon="🏠")
    st.divider()
    st.title("Filters")
    selected_hub = st.radio("Field Group", list(TOPIC_HUBS.keys()))
    selected_topic = st.selectbox("Topic", TOPIC_HUBS[selected_hub])

# --- MAIN PAGE ---
st.title(f"🎓 {selected_topic}")
st.caption("Curated High-Impact Research (Score 7+)")
st.divider()

try:
    papers = get_feed(selected_topic)

    if not papers:
        st.info(f"No high-impact papers found for {selected_topic} yet.")

    for paper in papers:
        with st.container(border=True):
            # Tighter Column Ratio for small chart
            col_text, col_chart = st.columns([0.9, 0.1])

            with col_text:
                st.subheader(paper['title'])

                # CONDITIONAL LABEL LOGIC
                if paper['score'] >= 8:
                    label = "  |  🏆 **Major Breakthrough**"
                else:
                    label = ""

                st.caption(f"📅 {paper['published_date']}{label}")
                st.markdown(paper['summary'])
                st.markdown(f"🔗 [Read Full Paper]({paper['url']})")

            with col_chart:
                # The label is now baked into the chart image itself
                ring = make_impact_ring(paper['score'])

                # We use use_container_width=True to let it center in the column
                # The column is narrow (0.1), so it effectively centers it.
                st.altair_chart(ring, use_container_width=True)

except sqlite3.OperationalError:
    st.error("⚠️ Database not found.")
