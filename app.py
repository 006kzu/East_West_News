import streamlit as st
import datetime
import re

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Peripheral News",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CSS INJECTION (Maintained from previous request)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* ----------------------------------------------------
       1. LAYOUT & SPACING FIXES
       ---------------------------------------------------- */
    .block-container {
        padding-top: 5rem !important; 
        padding-bottom: 2rem !important;
    }
    
    header[data-testid="stHeader"] {
        background-color: #A3AABE;
        border-bottom: 1px solid #dcdcdc;
    }

    /* ----------------------------------------------------
       2. TYPOGRAPHY
       ---------------------------------------------------- */
    h1, h2, h3 {
        color: #004225 !important; /* British Racing Green */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    a {
        color: #008080 !important; /* Teal */
        text-decoration: none;
        font-weight: bold;
    }

    /* ----------------------------------------------------
       3. COMPONENT STYLING
       ---------------------------------------------------- */
    .stTextInput > div > div, 
    .stDateInput > div > div,
    .stSelectbox > div > div {
        border-radius: 15px !important;
        border: 1px solid #008080;
    }
    
    .stButton > button {
        border-radius: 15px !important;
        border: 1px solid #004225;
        color: #004225;
        font-weight: 500;
        width: 100%;
    }
    .stButton > button:hover {
        border-color: #D99058 !important;
        color: #D99058 !important;
    }

    /* ----------------------------------------------------
       4. CARD/GRID STYLING
       ---------------------------------------------------- */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        border-radius: 15px !important;
        border: 1px solid #E5E4E2;
        background-color: #A3AABE; /* Your requested purple-grey */
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 20px !important;
        height: 100%;
    }

    .foreign-title {
        color: #333333;
        font-size: 0.8rem;
        font-style: italic;
        margin-bottom: 10px;
        display: block;
        line-height: 1.2;
    }
    
    /* ----------------------------------------------------
       5. SIDEBAR STYLING
       ---------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #A3AABE;
    }
    
    .stRadio > div {
        background-color: transparent;
    }
    .stRadio label {
        font-size: 1.1rem !important;
        padding: 10px;
        color: #333;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. MOCK DATA (Separated into Global vs Academic)
# -----------------------------------------------------------------------------


def get_global_news():
    return [
        {
            "id": 101,
            "title": "Headline: China Announces $5B Bio-Manufacturing Fund\nBody: The new policy aims to accelerate synthetic biology infrastructure...",
            "source": "Xinhua Policy Brief",
            "added_date": "2025-10-24",
            "link": "#",
            "region": "Global News"
        },
        {
            "id": 102,
            "title": "Headline: EU Regulations on AI Medical Devices Tighten\nBody: New compliance standards for generative AI in diagnostic tools...",
            "source": "Brussels Report",
            "added_date": "2025-10-23",
            "link": "#",
            "region": "Global News"
        },
        {
            "id": 103,
            "title": "Headline: Neuralink Competitor Secures Series B Funding\nBody: The Swiss-based startup focuses on non-invasive EEG interpretation...",
            "source": "Market Watch",
            "added_date": "2025-10-22",
            "link": "#",
            "region": "Global News"
        }
    ]


def get_academic_feed():
    return [
        {
            "id": 201,
            "title": "Headline: Long-term Stability of Conductive Polymer Coatings\nBody: A longitudinal study on the degradation rates of PEDOT:PSS...",
            "source": "Nature Biomedical",
            "added_date": "2025-10-24",
            "link": "#",
            "region": "Academic"
        },
        {
            "id": 202,
            "title": "Headline: Optogenetic Control of Motor Neurons in Primates\nBody: Achieving specific muscle activation using red-shifted opsins...",
            "source": "Science Robotics",
            "added_date": "2025-10-24",
            "link": "#",
            "region": "Academic"
        },
        {
            "id": 203,
            "title": "Headline: 3D Bioprinting of Vascularized Tissue Constructs\nBody: New bio-ink formulation allows for spontaneous capillary formation...",
            "source": "IEEE Engineering",
            "added_date": "2025-10-23",
            "link": "#",
            "region": "Academic"
        }
    ]

# -----------------------------------------------------------------------------
# 4. LOGIC HELPERS
# -----------------------------------------------------------------------------


def parse_ai_summary(full_text):
    match = re.search(r"\**Headline:?\**\s*(.*?)\n", full_text, re.IGNORECASE)
    if match:
        english_title = match.group(1).strip()
        body_text = full_text.replace(match.group(0), "").strip()
        body_text = body_text.replace("Body:", "").strip()
        return english_title, body_text
    return None, full_text


# -----------------------------------------------------------------------------
# 5. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("PERIPHERAL NEWS")
    st.caption("Global Bio-Engineering Intelligence")
    st.divider()

    # DATE PICKER
    selected_date = st.date_input("Date", datetime.date.today())

    st.divider()

    # NAVIGATION
    # Added "Home" as the first option
    page_selection = st.radio(
        "Navigate",
        ["Home", "Global News", "Academic Feed", "Saved Articles"],
        label_visibility="collapsed"
    )

    st.divider()
    st.info("System Status: **Online**")

# -----------------------------------------------------------------------------
# 6. RENDER FUNCTIONS
# -----------------------------------------------------------------------------


def render_grid_row(articles, section_title, link_target):
    """
    Renders a row of 3 cards with a section header.
    """
    # Section Header with "View All" button look-alike
    c_head, c_link = st.columns([4, 1])
    with c_head:
        st.subheader(section_title)
    with c_link:
        st.markdown(
            f"<div style='text-align: right; padding-top: 10px;'><a href='#'>{link_target} &rarr;</a></div>", unsafe_allow_html=True)

    # The Grid
    cols = st.columns(3)
    for i, item in enumerate(articles[:3]):  # Limit to 3 for the preview
        with cols[i]:
            english_title, body_text = parse_ai_summary(item['title'])
            display_title = english_title if english_title else "New Report"

            with st.container(border=True):
                st.markdown(
                    f"<small style='color:#333333; font-weight:bold;'>{item['source'].upper()}</small>", unsafe_allow_html=True)
                st.markdown(f"#### {display_title}")
                st.markdown(
                    f"<span class='foreign-title'>ID: {item['id']} • {item['added_date']}</span>", unsafe_allow_html=True)

                with st.expander("Summary"):
                    st.markdown(body_text)
                    st.markdown(f"[Source]({item['link']})")

# -----------------------------------------------------------------------------
# 7. MAIN CONTENT LOGIC
# -----------------------------------------------------------------------------


# FETCH DATA
global_data = get_global_news()
academic_data = get_academic_feed()

# LOGIC: HOME vs SPECIFIC PAGE
if page_selection == "Home":
    # 1. Dashboard Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Global Updates", "12", "+2")
    c2.metric("New Papers", "8", "+5")
    c3.metric("Urgent Alerts", "0")
    st.markdown("---")

    # 2. Global News Section (Preview)
    render_grid_row(global_data, "🌍 Global News", "See all Global News")

    st.markdown("<br>", unsafe_allow_html=True)  # Spacer

    # 3. Academic Feed Section (Preview)
    render_grid_row(academic_data, "🎓 Academic Feed", "See all Papers")

elif page_selection == "Global News":
    st.header("Global Intelligence Feed")
    st.markdown(
        "Monitoring policy, market movers, and geopolitical shifts in bio-tech.")
    st.markdown("---")
    # Render all Global items (using a loop for rows if we had more data)
    render_grid_row(global_data, "Today's Headlines", "Refresh")
    # Note: In a real app, you'd use a full grid function here, not just the preview row.

elif page_selection == "Academic Feed":
    st.header("Academic Literature Feed")
    st.markdown("Latest peer-reviewed publications and pre-prints.")
    st.markdown("---")
    render_grid_row(academic_data, "Latest Papers", "Refresh")

# Footer
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #666;'>© 2025 Peripheral News</div>",
            unsafe_allow_html=True)
