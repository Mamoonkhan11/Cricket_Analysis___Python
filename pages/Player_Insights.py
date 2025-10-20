# Individual Player Analytics

import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data

def run():
    st.title("🎯 Player Insights")
    
    # Load all data
    matches, balls, players, teams = load_all_data()

    # Clean column names
    for df in [players, balls]:
        df.columns = df.columns.str.strip()

    # Rename columns to match expected format
    if 'Striker_Id' in balls.columns:
        balls = balls.rename(columns={'Striker_Id': 'Player_Id'})
    if 'Batsman_Scored' in balls.columns:
        balls = balls.rename(columns={'Batsman_Scored': 'runs'})

    # Ensure Player_Id and runs exist
    if 'Player_Id' not in balls.columns:
        st.error("Balls data missing Player_Id column. Cannot calculate player stats.")
        return
    if 'runs' not in balls.columns:
        st.error("Balls data missing 'runs' column. Cannot calculate player runs.")
        return

    # Player selection
    player_name = st.selectbox("Select Player", players['Player_Name'].unique())
    player_row = players[players['Player_Name'] == player_name]
    if player_row.empty:
        st.warning("Selected player not found in data.")
        return
    player_id = player_row['Player_Id'].values[0]

    # Filter balls for this player
    player_balls = balls[balls['Player_Id'] == player_id]
    
    # Convert runs to numeric
    player_balls.loc[:, 'runs'] = pd.to_numeric(player_balls['runs'], errors='coerce').fillna(0)

    # Calculate stats
    total_runs = player_balls['runs'].sum()
    total_balls = player_balls.shape[0]
    strike_rate = (total_runs / total_balls * 100) if total_balls > 0 else 0

    # Display stats
    st.write(f"**Total Runs:** {total_runs}")
    st.write(f"**Total Balls:** {total_balls}")
    st.write(f"**Strike Rate:** {strike_rate:.2f}")