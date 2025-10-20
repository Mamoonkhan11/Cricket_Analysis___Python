# Team Performance

import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data
from utils.visualization import plot_team_wins

def run():
    st.title("🏏 Team Insights")

    # Load data
    try:
        matches, balls, players, teams = load_all_data()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return

    # Clean column names
    matches.columns = matches.columns.str.strip()
    teams.columns = teams.columns.str.strip()

    # Check required columns
    required_cols = ['Team_Name_Id', 'Opponent_Team_Id', 'winner']
    for col in required_cols:
        if col not in matches.columns:
            st.warning(f"Matches data missing column: {col}")
            return

    # Create mapping from Team_Id to Team_Name
    team_dict = dict(zip(teams['Team_Id'], teams['Team_Name']))

    # Map IDs to names
    matches['Team_Name_1'] = matches['Team_Name_Id'].map(team_dict)
    matches['Team_Name_2'] = matches['Opponent_Team_Id'].map(team_dict)
    matches['winner_name'] = matches['winner'].map(team_dict)

    # Check mapping
    if matches[['Team_Name_1', 'Team_Name_2', 'winner_name']].isnull().any().any():
        st.warning("Some Team_Id values in matches do not exist in teams.csv. Check your data.")

    # Team selection
    team_options = pd.concat([matches['Team_Name_1'], matches['Team_Name_2']]).dropna().unique()
    team_name = st.selectbox("Select Team", team_options)

    # Filter matches for selected team
    team_matches = matches[
        (matches['Team_Name_1'] == team_name) | 
        (matches['Team_Name_2'] == team_name)
    ]

    # Calculate stats
    total_matches = team_matches.shape[0]
    total_wins = (team_matches['winner_name'] == team_name).sum()

    # Display stats
    st.write(f"Total Matches Played: {total_matches}")
    st.write(f"Total Wins: {total_wins}")

    # Plot team wins
    try:
        st.plotly_chart(plot_team_wins(team_matches))
    except Exception as e:
        st.warning(f"Failed to generate team wins chart: {e}")
