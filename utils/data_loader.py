
import pandas as pd

def load_all_data():
    """
    Loads matches, balls, players, and teams data.
    Automatically maps Team IDs to Team Names for matches.
    Returns:
        matches (DataFrame)
        balls (DataFrame)
        players (DataFrame)
        teams (DataFrame)
    """
    # Load CSV files
    matches = pd.read_csv("data/Match.csv")
    balls = pd.read_csv("data/Ball_by_Ball.csv")
    players = pd.read_csv("data/Player.csv")
    teams = pd.read_csv("data/Team.csv")

    # Strip whitespace from column names
    for df in [matches, balls, players, teams]:
        df.columns = df.columns.str.strip()

    # Map team IDs to team names in matches
    if 'Team_Name_Id' in matches.columns and 'Opponent_Team_Id' in matches.columns:
        matches = matches.merge(
            teams[['Team_Id', 'Team_Name']],
            left_on='Team_Name_Id',
            right_on='Team_Id',
            how='left'
        ).rename(columns={'Team_Name': 'Team_Name'})

        matches = matches.merge(
            teams[['Team_Id', 'Team_Name']],
            left_on='Opponent_Team_Id',
            right_on='Team_Id',
            how='left',
            suffixes=('', '_Opponent')
        ).rename(columns={'Team_Name_Opponent': 'Team_Name_Opponent'})

    # Ensure winner column exists
    if 'winner' not in matches.columns:
        matches['winner'] = None  # placeholder if missing

    return matches, balls, players, teams