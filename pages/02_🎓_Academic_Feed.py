import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from app.database import get_feed
from app.topics import TOPIC_HUBS

st.set_page_config(page_title="Academic Feed", page_icon="🎓", layout="wide")

# --- HELPER: MINIATURE RING CHART ---


def make_impact_ring(score):
    source = pd.DataFrame({
        "Category": ["Impact", "Rest"],
        "Value": [score, 10-score]
    })

    base = alt.Chart(source).encode(theta=alt.Theta("Value", stack=True))

    pie = base.mark_arc(innerRadius=15, outerRadius=20).encode(
        color=alt.Color("Category", scale=alt.Scale(
            domain=["Impact", "Rest"], range=["#008080", "#E5E4E2"]), legend=None),
        order=alt.Order("Category", sort="descending")
    )

    text_score = base.mark_text(radius=0, size=12, color="#004225", fontStyle="bold").encode(
        text=alt.value(f"{score}")
    )

    # Label is now part of the chart
    label_df = pd.DataFrame({"label": ["Impact Score"]})
    text_label = alt.Chart(label_df).mark_text(
        align='center', dy=32, size=8, color="#888").encode(text='label')

    return (pie + text_score + text_label).properties(width=50, height=75)


# --- 1. HEADER & NAVIGATION ---
st.title("🎓 Academic Intelligence Feed")
st.caption("Curated High-Impact Research (Score 7+)")

# Create the top-level "Pills" navigation
# We add "All" to the start of the keys from TOPIC_HUBS
categories = ["All"] + list(TOPIC_HUBS.keys())

selected_category = st.pills(
    "Filter by Category",
    categories,
    default="All",
    selection_mode="single"
)

st.divider()

# --- 2. DATA FETCHING LOGIC ---
try:
    # CASE A: User selected "All"
    if selected_category == "All":
        st.subheader("🌍 Latest Breakthroughs (All Fields)")
        papers = get_feed(target="All")

    # CASE B: User selected a specific Category (e.g. Engineering)
    else:
        # Get the list of sub-topics (e.g. ['Biomedical Engineering', ...])
        available_topics = TOPIC_HUBS[selected_category]

        # Show a secondary filter for specific drilling
        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader(f"📂 {selected_category} Stream")
        with c2:
            # We use format_func to clean up the display labels
            def clean_label(option):
                if option == "View All":
                    return option
                # Remove "Engineering" from the display label only
                return option.replace(" Engineering", "")

            selected_specific = st.selectbox(
                "Filter by Topic",
                ["View All"] + available_topics,
                format_func=clean_label  # <--- THIS IS THE MAGIC FIX
            )

        # The rest of the logic remains exactly the same...
        if selected_specific == "View All":
            papers = get_feed(target=available_topics)
        else:
            # The variable 'selected_specific' still contains "Biomedical Engineering"
            # so the database query works perfectly.
            papers = get_feed(target=selected_specific)

    # --- 3. RENDER CARDS ---
    if not papers:
        st.info("No high-impact papers found matching these criteria.")

    for paper in papers:
        with st.container(border=True):
            col_text, col_chart = st.columns([0.9, 0.1])

            with col_text:
                st.subheader(paper['title'])

                # Metadata Line
                if paper['score'] >= 8:
                    badge = "🏆 **Major Breakthrough**"
                else:
                    badge = ""

                st.markdown(
                    f"**{paper['field']}** • 📅 {paper['published_date']}  |  {badge}")
                st.markdown(paper['summary'])
                st.markdown(f"🔗 [Read Full Paper]({paper['url']})")

            with col_chart:
                ring = make_impact_ring(paper['score'])
                st.altair_chart(ring, width='stretch')

except sqlite3.OperationalError:
    st.error("⚠️ Database connection failed. Ensure 'peripheral_news.db' exists.")
