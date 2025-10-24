import streamlit as st
from streamlit_option_menu import option_menu
import pages.Overview as overview
import pages.Player_Insights as player
import pages.Team_Insights as team
import pages.Match_Predictor as predictor
import pages.Report_Exporter as report

st.set_page_config(
    page_title="Cricket Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
/* Hide default menu and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Top Navigation bar */
.navbar {
    display: flex;
    justify-content: center;
    background-color: #1F2937;
    padding: 10px 0;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
.navbar button {
    margin: 0 15px;
    background-color: #3B82F6;
    border: none;
    padding: 8px 20px;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}
.navbar button:hover {
    background-color: #2563EB;
}
.navbar .selected {
    background-color: #2563EB;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; font-size:36px; font-weight:bold; color:#3B82F6; margin-bottom:20px;">
    🔮 Cricket Analytics Dashboard
</div>
""", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,  
    options=["Overview", "Player Insights", "Team Insights", "Match Predictor", "Report Exporter"],
    icons=["house", "person-lines-fill", "people-fill", "magic", "file-earmark-spreadsheet"],
    menu_icon="cast",
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1F2937"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#2563EB"},
        "nav-link-selected": {"background-color": "#3B82F6"},
    }
)

if selected == "Overview":
    overview.run()
elif selected == "Player Insights":
    player.run()
elif selected == "Team Insights":
    team.run()
elif selected == "Match Predictor":
    predictor.run()
elif selected == "Report Exporter":
    report.run()

st.markdown("""
<div style='text-align:center; padding:10px; color:gray; font-size:12px; margin-top:20px;'>
    © 2025 Cricket Analytics Dashboard | Designed with ❤️
</div>
""", unsafe_allow_html=True)