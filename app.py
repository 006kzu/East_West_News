import streamlit as st
import datetime

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Peripheral News",
    page_icon="🧬",
    layout="wide"
)

# 2. HEADER
# This container will now automatically use the #D5C7AC (Tan) background
# from your palette because of the theme settings.
with st.container(border=True):
    c_brand, c_spacer, c_date = st.columns([3, 3, 2])

    with c_brand:
        st.title("PERIPHERAL NEWS")
        st.caption("Global Bio-Engineering Intelligence")

    with c_date:
        st.date_input("Date", datetime.date.today(),
                      label_visibility="collapsed")

# 3. METRICS
st.write("")
c1, c2, c3 = st.columns(3)

# Mock data for demonstration
urgent_alerts = 2

c1.metric("Global Updates", "12", "+2")
c2.metric("New Papers", "8", "+5")

with c3:
    # This renders the number standardly
    st.metric("Urgent Alerts", f"{urgent_alerts}")

    # This adds the dynamic colored text underneath the metric
    if urgent_alerts > 0:
        st.markdown(f":red[**Action Required**]")
    else:
        st.markdown(f":green[All Clear]")
st.divider()

# 4. MAIN FEED
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🌍 Global News")
    with st.container(border=True):
        st.markdown("**China Announces $5B Bio-Fund**")
        st.caption("Xinhua Policy • 2025-12-21")
        st.button("View Global Feed",
                  use_container_width=True, key="btn_global")

with col_right:
    st.markdown("### 🎓 Academic Feed")
    with st.container(border=True):
        st.markdown("**Stability of Polymer Coatings**")
        st.caption("Nature Bio • 2025-12-21")
        st.button("View Academic Feed",
                  use_container_width=True, key="btn_academic")
