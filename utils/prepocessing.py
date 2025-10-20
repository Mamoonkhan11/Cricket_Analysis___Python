import pandas as pd

def compute_player_average(player_match_df, player_id, stat='runs_scored'):
    player_data = player_match_df[player_match_df['player_id'] == player_id]
    if player_data.empty:
        return 0
    return player_data[stat].mean()

def compute_team_recent_form(matches_df, team_name, last_n=5):
    team_matches = matches_df[(matches_df['team1']==team_name) | (matches_df['team2']==team_name)]
    team_matches = team_matches.tail(last_n)
    wins = (team_matches['winner'] == team_name).sum()
    return wins / last_n if last_n > 0 else 0

def head_to_head(matches_df, team1, team2):
    h2h_matches = matches_df[((matches_df['team1']==team1) & (matches_df['team2']==team2)) |
                             ((matches_df['team1']==team2) & (matches_df['team2']==team1))]
    if h2h_matches.empty:
        return 0.5
    team1_wins = (h2h_matches['winner']==team1).sum()
    return team1_wins / h2h_matches.shape[0]
