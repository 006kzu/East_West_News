import streamlit as st
import datetime
import re
from app.database import get_dashboard_stats, get_latest_news_preview, get_latest_academic_preview

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Peripheral News",
    page_icon="🧬",
    layout="wide"
)

# 2. HELPER: Clean AI Headlines


def parse_headline(summary_text):
    """Extracts the English headline if the AI formatted it that way."""
    if not summary_text:
        return "No Summary Available"
    # Look for "**Headline:**" pattern often used by the AI
    match = re.search(r"\**Headline:?\**\s*(.*?)\n",
                      summary_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return summary_text[:80] + "..."  # Fallback to first 80 chars


# 3. HEADER
with st.container(border=True):
    c_brand, c_spacer, c_date = st.columns([3, 3, 2])

    with c_brand:
        st.title("PERIPHERAL NEWS")
        st.caption("Global Bio-Engineering Intelligence")

    with c_date:
        # User picks a date (Defaults to Today)
        selected_date = st.date_input(
            "Date", datetime.date.today(), label_visibility="collapsed")
        date_str = selected_date.strftime("%Y-%m-%d")

# 4. FETCH REAL DATA
try:
    stats = get_dashboard_stats(date_str)
    latest_news = get_latest_news_preview()
    latest_paper = get_latest_academic_preview()
except Exception as e:
    # Handle case where DB isn't ready
    stats = {"global_total": 0, "global_today": 0,
             "academic_total": 0, "academic_today": 0}
    latest_news = None
    latest_paper = None
    # st.error(f"Database Connection Error: {e}") # Uncomment to debug

# 5. METRICS
st.write("")
c1, c2, c3 = st.columns(3)

# Metric 1: Global News
c1.metric(
    "Global Updates",
    f"{stats['global_total']}",
    f"+{stats['global_today']} today"
)

# Metric 2: Academic Papers
c2.metric(
    "New Papers",
    f"{stats['academic_total']}",
    f"+{stats['academic_today']} today"
)

# Metric 3: Urgent Alerts (Logic Placeholder)
# You could count articles with specific keywords like "Emergency" or "Sanction"
urgent_alerts = 0
with c3:
    st.metric("Urgent Alerts", f"{urgent_alerts}")
    if urgent_alerts > 0:
        st.markdown(f":red[**Action Required**]")
    else:
        st.markdown(f":green[All Clear]")

st.divider()

# 6. MAIN FEED PREVIEWS
col_left, col_right = st.columns(2)

# --- LEFT COLUMN: GLOBAL NEWS ---
with col_left:
    st.markdown("### 🌍 Global News")
    with st.container(border=True):
        if latest_news:
            # Parse the AI summary to get a clean headline
            display_title = parse_headline(latest_news['summary'])

            st.markdown(f"**{display_title}**")
            st.caption(
                f"{latest_news['source']} • {latest_news['added_date']}")
            st.markdown(f"[Read Original Source]({latest_news['link']})")
        else:
            st.info("System Offline. Run `python run_news.py` to ingest data.")

        st.button("View Global Feed",
                  use_container_width=True, key="btn_global")

# --- RIGHT COLUMN: ACADEMIC FEED ---
with col_right:
    st.markdown("### 🎓 Academic Feed")
    with st.container(border=True):
        if latest_paper:
            st.markdown(f"**{latest_paper['title']}**")
            st.caption(
                f"{latest_paper['field']} • {latest_paper['published_date']}")

            # Show score if available
            score = latest_paper['score']
            if score >= 8:
                st.markdown(f":star: **Major Finding ({score}/10)**")
            else:
                st.markdown(f"Impact Score: {score}/10")

        else:
            st.info("No papers found. Run `python run_academic.py`.")

        # This button could link to your pages/02_🎓_Academic_Feed.py
        if st.button("View Academic Feed", use_container_width=True, key="btn_academic"):
            st.switch_page("pages/02_🎓_Academic_Feed.py")
