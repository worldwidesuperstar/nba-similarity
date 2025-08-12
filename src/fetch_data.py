from nba_api.stats.endpoints import leagueleaders, playerdashboardbygeneralsplits, shotchartdetail
import pandas as pd
import time

def fetch_top_200_pp48(season='2024-25'):
    # fetch top 200 in PPG
    leaders = leagueleaders.LeagueLeaders(
        stat_category_abbreviation='PTS',
        season=season,
        per_mode48='PerGame'
    )

    df = leaders.get_data_frames()[0]
    top200 = df.head(200)

    top200.to_csv('data/raw/top200_per.csv', index=False)
    print('saved top 200 players by PTS/48 to CSV.')
    return top200

def fetch_save_advanced_data(df, season='2024-25', delay=5):
    for idx, row in df.iterrows():
        # get player
        player_id = row['PLAYER_ID']
        player_name = row['PLAYER']

        general_data=retry_fetch_dashboard(player_id, season)
        general_data.to_csv(f'data/raw/{player_id}_general_splits.csv', index=False)
        print("saved general splits for ",player_name, ".")

        shot_data=retry_fetch_dashboard(player_id, season)
        shot_data.to_csv(f'data/raw/{player_id}_shot_data.csv', index=False)
        print("saved shot data for ",player_name, ".") 

        time.sleep(delay)

def retry_fetch_dashboard(player_id, season, max_retries=5, pause=5):
    for attempt in range(max_retries):
        try:
            dash = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(
                player_id=player_id,
                season=season
            )
            df = dash.get_data_frames()[1]
            return df
        except Exception as e:
            wait = pause * (attempt + 1)
            print(f"timeout/error for {player_id} on attempt {attempt+1}. retrying in {wait} seconds...")
            time.sleep(wait)

    print(f"failed to fetch data for {player_id} after {max_retries} attempts.")
    return None

def retry_fetch_shotchart(player_id, season, max_retries=5, pause=5):
    for attempt in range(max_retries):
        try:
            shots=shotchartdetail.ShotChartDetail(
                team_id=0,
                player_id=player_id,
                season_type_all_star='Regular Season',
                season_nullable=season
            )
            df = shots.get_data_frames()[1]
            return df
        except Exception as e:
            wait = pause * (attempt + 1)
            print(f"timeout/error for {player_id} on attempt {attempt+1}. retrying in {wait} seconds...")
            time.sleep(wait)
    print(f"failed to fetch data for {player_id} after {max_retries} attempts.")
    return None

if __name__ == "__main__":
    top200 = fetch_top_200_pp48()
    fetch_save_advanced_data(top200)