# ML Based Match Prediction

import streamlit as st
import pandas as pd
import pickle
import os

def run():
    st.title("🔮 Match Predictor")

    # Load teams from CSV if exists, otherwise fallback to hardcoded
    teams_file = "data/teams.csv"
    if os.path.exists(teams_file):
        teams_df = pd.read_csv(teams_file)
        teams_df.columns = teams_df.columns.str.strip()
        team_data = teams_df[['Team_Id', 'Team_Name', 'Team_Short_Code']]
    else:
        team_data = pd.DataFrame([
            [1,"Kolkata Knight Riders","KKR"],
            [2,"Royal Challengers Bangalore","RCB"],
            [3,"Chennai Super Kings","CSK"],
            [4,"Kings XI Punjab","KXIP"],
            [5,"Rajasthan Royals","RR"],
            [6,"Delhi Daredevils","DD"],
            [7,"Mumbai Indians","MI"],
            [8,"Deccan Chargers","DC"],
            [9,"Kochi Tuskers Kerala","KTK"],
            [10,"Pune Warriors","PW"],
            [11,"Sunrisers Hyderabad","SRH"],
            [12,"Rising Pune Supergiants","RPS"],
            [13,"Gujarat Lions","GL"]
        ], columns=["Team_Id","Team_Name","Team_Short_Code"])

    team_shortcodes = team_data["Team_Short_Code"].tolist()

    # Streamlit inputs
    team1 = st.selectbox("Team 1", team_shortcodes)
    team2 = st.selectbox("Team 2", [t for t in team_shortcodes if t != team1])
    toss_winner = st.selectbox("Toss Winner", [team1, team2])
    venue = st.text_input("Venue", "Mumbai")

    # Load model and encoders safely
    model_path = "models/match_predictor.pkl"
    encoders_path = "models/encoders.pkl"

    if not os.path.exists(model_path) or os.path.getsize(model_path) == 0:
        st.error("Model file is missing or empty! Please train the model first.")
        return

    if not os.path.exists(encoders_path) or os.path.getsize(encoders_path) == 0:
        st.error("Encoders file is missing or empty!")
        return

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(encoders_path, "rb") as f:
        encoders = pickle.load(f)

    # Predict
    if st.button("Predict Winner"):
        try:
            # Create input dataframe
            input_df = pd.DataFrame({
                "team1": [team1],
                "team2": [team2],
                "toss_winner": [toss_winner],
                "venue": [venue]
            })

            # Encode input using saved encoders
            for col in input_df.columns:
                if col in encoders:
                    le = encoders[col]
                    input_df[col] = le.transform(input_df[col])
                else:
                    st.warning(f"No encoder found for column: {col}")

            # Predict winner
            pred = model.predict(input_df)[0]
            winner = encoders['winner'].inverse_transform([pred])[0]

            st.success(f"Predicted Winner: {winner}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")