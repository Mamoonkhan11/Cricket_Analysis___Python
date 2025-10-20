# Main file to load and run Steamlit and all other files

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Cricket Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS 
def load_css(file_path="assets/styles.css"):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Overview",
    "Player Insights",
    "Team Insights",
    "Match Predictor",
    "Report Exporter"
])

# Page routing 
if page == "Overview":
    import pages.Overview as overview
    overview.run()
elif page == "Player Insights":
    import pages.Player_Insights as player
    player.run()
elif page == "Team Insights":
    import pages.Team_Insights as team
    team.run()
elif page == "Match Predictor":
    import pages.Match_Predictor as predictor
    predictor.run()
elif page == "Report Exporter":
    import pages.Report_Exporter as report
    report.run()

# Footer 
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
