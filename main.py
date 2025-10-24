# Main file to load and run Streamlit with modern navigation

import streamlit as st
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Cricket Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS 
def load_css(file_path="assets/styles.css"):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------------
# Modern Top Navigation Bar
# -------------------------
selected_page = option_menu(
    menu_title=None,  # no menu title
    options=["Overview", "Player Insights", "Team Insights", "Match Predictor", "Report Exporter"],
    icons=["house", "person-circle", "people", "lightning", "file-earmark-text"],  # icons
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color":"#eee"},
        "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
    }
)

# -------------------------
# Page Routing 
# -------------------------
if selected_page == "Overview":
    import pages.Overview as overview
    overview.run()
elif selected_page == "Player Insights":
    import pages.Player_Insights as player
    player.run()
elif selected_page == "Team Insights":
    import pages.Team_Insights as team
    team.run()
elif selected_page == "Match Predictor":
    import pages.Match_Predictor as predictor
    predictor.run()
elif selected_page == "Report Exporter":
    import pages.Report_Exporter as report
    report.run()

# -------------------------
# Footer
# -------------------------
st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    text-align: center;
    padding: 5px;
    font-size: 12px;
    color: gray;
}
</style>
<div class="footer">
    © 2025 Cricket Analytics Dashboard
</div>
""", unsafe_allow_html=True)