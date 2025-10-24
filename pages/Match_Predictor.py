# ML Based Match Prediction - Updated
import streamlit as st
import pandas as pd
import pickle
import os

def run():
    st.title("🔮 Match Predictor")

    # Load teams from CSV if exists, otherwise fallback to hardcoded
    teams_file = "data/Team.csv"
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

    # Get venues from encoder to prevent unseen labels
    if 'Venue_Name' in encoders:
        venues = encoders['Venue_Name'].classes_.tolist()
    else:
        venues = ["Mumbai", "Delhi", "Chennai", "Kolkata"]  # fallback list

    # Streamlit inputs
    team1_code = st.selectbox("Team 1", team_shortcodes)
    team2_code = st.selectbox("Team 2", [t for t in team_shortcodes if t != team1_code])
    toss_winner_code = st.selectbox("Toss Winner", [team1_code, team2_code])
    venue_name = st.selectbox("Venue", venues)  # dropdown from encoder

    # Map shortcodes to Team_Id for model input
    team1_id = int(team_data.loc[team_data["Team_Short_Code"] == team1_code, "Team_Id"].values[0])
    team2_id = int(team_data.loc[team_data["Team_Short_Code"] == team2_code, "Team_Id"].values[0])
    toss_winner_id = int(team_data.loc[team_data["Team_Short_Code"] == toss_winner_code, "Team_Id"].values[0])

    # Predict
    if st.button("Predict Winner"):
        try:
            # Create input dataframe with correct feature names
            input_df = pd.DataFrame({
                "Team_Name_Id": [team1_id],
                "Opponent_Team_Id": [team2_id],
                "Toss_Winner_Id": [toss_winner_id],
                "Venue_Name": [venue_name]
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