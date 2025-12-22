import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from app.database import get_feed
from app.topics import TOPIC_HUBS

st.set_page_config(page_title="Academic Feed", page_icon="🎓", layout="wide")

# --- CSS FOR ALIGNMENT ---
st.markdown("""
<style>
    /* Center the chart in its column */
    [data-testid="stAltairChart"] {
        display: flex;
        justify-content: center;
        /* Push it down slightly to visually center it against the text */
        margin-top: 10px; 
    }
    
    /* Make the Impact Score label tiny and gray */
    .impact-label {
        text-align: center;
        font-size: 10px;
        color: #888;
        line-height: 1;
        margin-top: -5px; /* Pull it closer to the ring */
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER: MINIATURE RING CHART ---


def make_impact_ring(score):
    # Data: Score vs Rest
    source = pd.DataFrame({
        "Category": ["Impact", "Rest"],
        "Value": [score, 10-score]
    })

    base = alt.Chart(source).encode(
        theta=alt.Theta("Value", stack=True)
    )

    # The Ring (Smaller Radius)
    pie = base.mark_arc(innerRadius=15, outerRadius=20).encode(
        color=alt.Color("Category",
                        scale=alt.Scale(domain=["Impact", "Rest"],
                                        range=["#008080", "#E5E4E2"]),
                        legend=None),
        order=alt.Order("Category", sort="descending")
    )

    # The Text (Smaller Font)
    text = base.mark_text(radius=0, size=12, color="#004225", fontStyle="bold", align="center", baseline="middle").encode(
        text=alt.value(f"{score}")
    )

    # Combine (Smaller Canvas)
    return (pie + text).properties(width=50, height=50)


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
                ring = make_impact_ring(paper['score'])
                st.altair_chart(ring, use_container_width=True)
                # Tighter HTML label
                st.markdown(
                    "<div class='impact-label'>Impact<br>Score</div>", unsafe_allow_html=True)

except sqlite3.OperationalError:
    st.error("⚠️ Database not found.")
