import plotly.express as px

def plot_team_wins(matches_df):
    win_counts = matches_df['winner'].value_counts().reset_index()
    win_counts.columns = ['Team','Wins']
    fig = px.bar(win_counts, x='Team', y='Wins', title='Team Wins', color='Wins', text='Wins')
    return fig

def plot_player_runs(player_match_df, player_name):
    df = player_match_df[player_match_df['player_name']==player_name]
    fig = px.line(df, x='match_id', y='runs_scored', title=f'{player_name} Runs per Match', markers=True)
    return fig