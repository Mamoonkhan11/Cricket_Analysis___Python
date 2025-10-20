# Season and Stats Overview File

import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data
from utils.visualization import plot_team_wins

def run():
    st.title("📊 Season Overview")

    # Load all data
    try:
        matches, balls, players, teams = load_all_data()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return

    # Check data is not empty
    if matches.empty:
        st.warning("No match data available.")
        return
    if players.empty:
        st.warning("No player data available.")

    # Team Wins Visualization
    st.header("🏆 Team Wins")
    try:
        st.plotly_chart(plot_team_wins(matches))
    except Exception as e:
        st.warning(f"Failed to generate team wins chart: {e}")

    # General Stats
    st.header("General Stats")
    st.write("Total Matches:", matches.shape[0])
    st.write("Total Players:", players.shape[0])
    st.write("Total Teams:", teams.shape[0] if not teams.empty else "N/A")
