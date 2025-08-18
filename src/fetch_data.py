from nba_api.stats.endpoints import (
    leaguedashplayerstats, playerdashboardbygeneralsplits, shotchartdetail, playerdashptshots,
    leaguehustlestatsplayer, leaguedashplayerclutch, playerdashptpass
)

import pandas as pd
import time
import os

def fetch_top_300_ppg(season='2024-25'):

    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        league_id_nullable='00',
        season=season,
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    )

    df = player_stats.get_data_frames()[0]
    top300 = df.nlargest(300, 'PTS')

    top300.to_csv('data/top300_per.csv', index=False)
    print('saved top 300 players by PPG to CSV.')

    return top300

def fetch_save_advanced_data(df, season='2024-25', delay=5):
    for idx, row in df.iterrows():
        # get player
        player_id = row['PLAYER_ID']
        player_name = row['PLAYER_NAME']

        general_splits_path = f'data/raw/{player_id}_general_splits.csv'
        shot_data_path = f'data/raw/{player_id}_shot_data.csv'
        
        # check if general splits data already exists
        fetched_data = False
        if not os.path.exists(general_splits_path):
            general_data=retry_fetch_dashboard(player_id, season)
            if general_data is not None:
                general_data.to_csv(general_splits_path, index=False)
                print(f"saved general splits for {player_name}.")
                fetched_data = True
        else:
            print(f"general splits for {player_name} already exists, skipping.")

        # check if shot data already exists
        if not os.path.exists(shot_data_path):
            shot_data=retry_fetch_shotchart(player_id, season)
            if shot_data is not None:
                shot_data.to_csv(shot_data_path, index=False)
                print(f"saved shot data for {player_name}.") 
                fetched_data = True
        else:
            print(f"shot data for {player_name} already exists, skipping.")

        # only sleep if we actually fetched data
        if fetched_data:
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
            shots = shotchartdetail.ShotChartDetail(
                team_id=0,
                player_id=player_id,
                season_type_all_star='Regular Season',
                season_nullable=season
            )
            df = shots.get_data_frames()[0]
            return df
        except Exception as e:
            wait = pause * (attempt + 1)
            print(f"timeout/error for {player_id} on attempt {attempt+1}. retrying in {wait} seconds...")
            time.sleep(wait)
    print(f"failed to fetch data for {player_id} after {max_retries} attempts.")
    return None

def retry_fetch_shot_tracking(player_name, player_id, team_id, season, max_retries=3, pause=5):
    for attempt in range(max_retries):
        try:
            shot_tracking = playerdashptshots.PlayerDashPtShots(
                player_id=player_id,
                team_id=team_id,
                season=season,
                season_type_all_star='Regular Season',
                per_mode_simple='PerGame', # per36 not available
            )
            print(f"saved shot tracking data for {player_name}")
            dataframes = shot_tracking.get_data_frames()
            return dataframes
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"failed to fetch shot tracking for {player_name}")
                return None
            time.sleep(pause)
    return None

def fetch_save_shot_tracking_data(df, season='2024-25', delay=2):
    
    for idx, row in df.iterrows():
        player_id = row['PLAYER_ID']
        team_id = row['TEAM_ID']
        player_name = row['PLAYER_NAME']
        
        dataframe_names = [
            'ClosestDefender10ftPlusShooting',
            'ClosestDefenderShooting', 
            'DribbleShooting',
            'GeneralShooting',
            'Overall',
            'ShotClockShooting',
            'TouchTimeShooting'
        ]
        
        # check if any shot tracking files are missing
        missing_files = []
        for name in dataframe_names:
            filepath = f'data/raw/{player_id}_{name}.csv'
            if not os.path.exists(filepath):
                missing_files.append(name)
        
        if missing_files:
            tracking_data = retry_fetch_shot_tracking(player_name, player_id, team_id, season)
            
            if tracking_data:
                for i, df_track in enumerate(tracking_data):
                    if not df_track.empty and i < len(dataframe_names):
                        filename = f'data/raw/{player_id}_{dataframe_names[i]}.csv'
                        df_track.to_csv(filename, index=False)
            # only sleep if we actually fetched data
            time.sleep(delay)
        else:
            print(f"shot tracking data for {player_name} already exists, skipping.")

def retry_fetch_hustle_stats(season, max_retries=3, pause=5):
    for attempt in range(max_retries):
        try:
            hustle = leaguehustlestatsplayer.LeagueHustleStatsPlayer(
                per_mode_time='PerGame',
                season=season,
                season_type_all_star='Regular Season'
            )
            df = hustle.get_data_frames()[0]
            return df
        except Exception as e:
            wait = pause * (attempt + 1)
            print(f"timeout/error for hustle stats on attempt {attempt+1}. retrying in {wait} seconds...")
            time.sleep(wait)
    print(f"failed to fetch hustle stats after {max_retries} attempts.")
    return None

def retry_fetch_clutch_stats(season, max_retries=3, pause=5):
    for attempt in range(max_retries):
        try:
            clutch = leaguedashplayerclutch.LeagueDashPlayerClutch(
                league_id_nullable='00',
                ahead_behind='Ahead or Behind',
                clutch_time='Last 5 Minutes',
                measure_type_detailed_defense='Base',
                per_mode_detailed='PerGame',
                season=season,
                season_type_all_star='Regular Season'
            )
            df = clutch.get_data_frames()[0]
            return df
        except Exception as e:
            wait = pause * (attempt + 1)
            print(f"timeout/error for clutch stats on attempt {attempt+1}. retrying in {wait} seconds...")
            time.sleep(wait)
    print(f"failed to fetch clutch stats after {max_retries} attempts.")
    return None

def retry_fetch_passing_data(player_id, team_id, season, max_retries=3, pause=5):
    for attempt in range(max_retries):
        try:
            passing = playerdashptpass.PlayerDashPtPass(
                player_id=player_id,
                team_id=team_id,
                season=season,
                season_type_all_star='Regular Season',
                per_mode_simple='PerGame'
            )
            dataframes = passing.get_data_frames()
            return dataframes
        except Exception as e:
            wait = pause * (attempt + 1)
            print(f"timeout/error for {player_id} passing data on attempt {attempt+1}. retrying in {wait} seconds...")
            time.sleep(wait)
    print(f"failed to fetch passing data for {player_id} after {max_retries} attempts.")
    return None

def fetch_save_basketball_iq_data(season='2024-25'):
    # fetch league hustle stats
    hustle_path = 'data/raw/league_hustle_stats.csv'
    if not os.path.exists(hustle_path):
        hustle_data = retry_fetch_hustle_stats(season)
        if hustle_data is not None:
            hustle_data.to_csv(hustle_path, index=False)
            print("saved league hustle stats.")
    else:
        print("league hustle stats already exists, skipping.")
    
    # fetch league clutch stats  
    clutch_path = 'data/raw/league_clutch_stats.csv'
    if not os.path.exists(clutch_path):
        clutch_data = retry_fetch_clutch_stats(season)
        if clutch_data is not None:
            clutch_data.to_csv(clutch_path, index=False)
            print("saved league clutch stats.")
    else:
        print("league clutch stats already exists, skipping.")

def fetch_save_passing_data(df, season='2024-25', delay=8):
    for idx, row in df.iterrows():
        player_id = row['PLAYER_ID']
        team_id = row['TEAM_ID']
        player_name = row['PLAYER_NAME']
        
        dataframe_names = [
            'PassesMade',
            'PassesReceived'
        ]
        
        # check if any passing files are missing
        missing_files = []
        for name in dataframe_names:
            filepath = f'data/raw/{player_id}_{name}.csv'
            if not os.path.exists(filepath):
                missing_files.append(name)
        
        if missing_files:
            passing_data = retry_fetch_passing_data(player_id, team_id, season)
            
            if passing_data:
                for i, df_pass in enumerate(passing_data):
                    if not df_pass.empty and i < len(dataframe_names):
                        filename = f'data/raw/{player_id}_{dataframe_names[i]}.csv'
                        df_pass.to_csv(filename, index=False)
                        print(f"saved {dataframe_names[i]} for {player_name}.")
            # only sleep if we actually fetched data
            time.sleep(delay)
        else:
            print(f"passing data for {player_name} already exists, skipping.")

if __name__ == "__main__":
    
    top300 = fetch_top_300_ppg()
    
    fetch_save_advanced_data(top300)
    fetch_save_shot_tracking_data(top300)
    fetch_save_basketball_iq_data()
    fetch_save_passing_data(top300)
    