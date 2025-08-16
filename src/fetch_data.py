from nba_api.stats.endpoints import (
    leagueleaders, playerdashboardbygeneralsplits, shotchartdetail, playerdashptshots,
    leaguehustlestatsplayer, leaguedashplayerclutch, playerdashptpass, assisttracker
)

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

    top200.to_csv('../dat/top200_per.csv', index=False)
    print('saved top 200 players by PPG to CSV.')
    print(df.head(30))

    return top200

def fetch_save_advanced_data(df, season='2024-25', delay=5):
    for idx, row in df.iterrows():
        # get player
        player_id = row['PLAYER_ID']
        player_name = row['PLAYER']

        general_data=retry_fetch_dashboard(player_id, season)
        general_data.to_csv(f'../data/raw/{player_id}_general_splits.csv', index=False)
        print("saved general splits for ",player_name, ".")

        shot_data=retry_fetch_shotchart(player_id, season)
        shot_data.to_csv(f'../data/raw/{player_id}_shot_data.csv', index=False)
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
            df = shots.get_data_frames()[0]
            return df
        except Exception as e:
            wait = pause * (attempt + 1)
            print(f"timeout/error for {player_id} on attempt {attempt+1}. retrying in {wait} seconds...")
            time.sleep(wait)
    print(f"failed to fetch data for {player_id} after {max_retries} attempts.")
    return None

def retry_fetch_shot_tracking(player_id, team_id, season, max_retries=3, pause=5):
    """
    Fetch shot tracking data for MBTI analysis
    """
    for attempt in range(max_retries):
        try:
            shot_tracking = playerdashptshots.PlayerDashPtShots(
                player_id=player_id,
                team_id=team_id,
                season=season,
                season_type_all_star='Regular Season',
                per_mode_simple='Per36',
            )
            dataframes = shot_tracking.get_data_frames()
            return dataframes
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"  Shot tracking: FAILED - {str(e)[:100]}...")
                return None
            time.sleep(pause)
    return None

def fetch_save_shot_tracking_data(df, season='2024-25', delay=8):
    
    for idx, row in df.iterrows():
        player_id = row['PLAYER_ID']
        team_id = row['TEAM_ID']
        player_name = row['PLAYER']
        
        print(f"\nfetching shot tracking for {player_name}...")
        
        tracking_data = retry_fetch_shot_tracking(player_id, team_id, season)
        
        if tracking_data:

            dataframe_names = [
                'ClosestDefender10ftPlusShooting',
                'ClosestDefenderShooting', 
                'DribbleShooting',
                'GeneralShooting',
                'Overall',
                'ShotClockShooting',
                'TouchTimeShooting'
            ]
            
            for i, df_track in enumerate(tracking_data):
                if not df_track.empty and i < len(dataframe_names):
                    filename = f'data/raw/{player_id}_{dataframe_names[i]}.csv'
                    df_track.to_csv(filename, index=False)
        
        time.sleep(delay)

def retry_fetch_hustle_stats(season, max_retries=3, pause=5):
    for attempt in range(max_retries):
        try:
            hustle = leaguehustlestatsplayer.LeagueHustleStatsPlayer(
                per_mode_time='Per36',
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
                ahead_behind='Ahead or Behind',
                clutch_time='Last 5 Minutes',
                measure_type_detailed_defense='Base',
                per_mode_detailed='Per36',
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

def retry_fetch_assist_tracker(season, max_retries=3, pause=5):
    for attempt in range(max_retries):
        try:
            assist = assisttracker.AssistTracker(
                per_mode_simple_nullable='PerGame',
                season_nullable=season,
                season_type_all_star_nullable='Regular Season'
            )
            df = assist.get_data_frames()[0]
            return df
        except Exception as e:
            wait = pause * (attempt + 1)
            print(f"timeout/error for assist tracker on attempt {attempt+1}. retrying in {wait} seconds...")
            time.sleep(wait)
    print(f"failed to fetch assist tracker after {max_retries} attempts.")
    return None

def fetch_jimmy_butler_data(season='2024-25'):
    """Manually fetch Jimmy Butler's data since he's not in top 200 PPG but has high basketball IQ."""
    
    # Jimmy Butler's player ID and team ID (Miami Heat)
    jimmy_butler_id = 202710
    miami_heat_id = 1610612748
    player_name = "Jimmy Butler"
    
    print(f"Fetching data for {player_name} (ID: {jimmy_butler_id})...")
    
    try:
        # Fetch general splits data
        general_data = retry_fetch_dashboard(jimmy_butler_id, season)
        if general_data is not None:
            general_data.to_csv(f'../data/raw/{jimmy_butler_id}_general_splits.csv', index=False)
            print(f"Saved general splits for {player_name}")
        
        # Fetch shot chart data
        shot_data = retry_fetch_shotchart(jimmy_butler_id, season)
        if shot_data is not None:
            shot_data.to_csv(f'../data/raw/{jimmy_butler_id}_shot_data.csv', index=False)
            print(f"Saved shot data for {player_name}")
        
        # Fetch shot tracking data
        tracking_data = retry_fetch_shot_tracking(jimmy_butler_id, miami_heat_id, season)
        if tracking_data:
            dataframe_names = [
                'ClosestDefender10ftPlusShooting',
                'ClosestDefenderShooting', 
                'DribbleShooting',
                'GeneralShooting',
                'Overall',
                'ShotClockShooting',
                'TouchTimeShooting'
            ]
            
            for i, df_track in enumerate(tracking_data):
                if not df_track.empty and i < len(dataframe_names):
                    filename = f'../data/raw/{jimmy_butler_id}_{dataframe_names[i]}.csv'
                    df_track.to_csv(filename, index=False)
                    print(f"Saved {dataframe_names[i]} for {player_name}")
        
        # Fetch passing data
        passing_data = retry_fetch_passing_data(jimmy_butler_id, miami_heat_id, season)
        if passing_data:
            dataframe_names = ['PassesMade', 'PassesReceived']
            
            for i, df_pass in enumerate(passing_data):
                if not df_pass.empty and i < len(dataframe_names):
                    filename = f'../data/raw/{jimmy_butler_id}_{dataframe_names[i]}.csv'
                    df_pass.to_csv(filename, index=False)
                    print(f"Saved {dataframe_names[i]} for {player_name}")
        
        print(f"Successfully fetched all data for {player_name}")
        
        # Add Jimmy Butler to top200 CSV if not already there
        try:
            top200_df = pd.read_csv('../data/raw/top200_per.csv')
            
            # Check if Jimmy Butler is already in the data
            if jimmy_butler_id not in top200_df['PLAYER_ID'].values:
                # Get his basic stats from league leaders (he should be in top 400 or so)
                leaders = leagueleaders.LeagueLeaders(
                    stat_category_abbreviation='PTS',
                    season=season,
                    per_mode48='PerGame'
                )
                all_players_df = leaders.get_data_frames()[0]
                
                jimmy_stats = all_players_df[all_players_df['PLAYER_ID'] == jimmy_butler_id]
                if not jimmy_stats.empty:
                    # Add Jimmy to our top200 dataset
                    updated_top200 = pd.concat([top200_df, jimmy_stats], ignore_index=True)
                    updated_top200.to_csv('../data/raw/top200_per.csv', index=False)
                    print(f"Added {player_name} to top200 dataset")
                else:
                    print(f"Could not find {player_name} in league leaders")
            else:
                print(f"{player_name} already in top200 dataset")
                
        except Exception as e:
            print(f"Error updating top200 with Jimmy Butler: {e}")
        
    except Exception as e:
        print(f"Error fetching data for {player_name}: {e}")

def fetch_save_basketball_iq_data(season='2024-25'):
    # fetch league hustle stats

    hustle_data = retry_fetch_hustle_stats(season)
    if hustle_data is not None:
        hustle_data.to_csv('../data/raw/league_hustle_stats.csv', index=False)
        print("saved league hustle stats.")
    
    # fetch league clutch stats  
    clutch_data = retry_fetch_clutch_stats(season)
    if clutch_data is not None:
        clutch_data.to_csv('../data/raw/league_clutch_stats.csv', index=False)
        print("saved league clutch stats.")
    
    # fetch league assist tracker
    assist_data = retry_fetch_assist_tracker(season)
    if assist_data is not None:
        assist_data.to_csv('../data/raw/league_assist_tracker.csv', index=False)
        print("saved league assist tracker.")

def fetch_save_passing_data(df, season='2024-25', delay=8):
    for idx, row in df.iterrows():
        player_id = row['PLAYER_ID']
        team_id = row['TEAM_ID']
        player_name = row['PLAYER']
        
        passing_data = retry_fetch_passing_data(player_id, team_id, season)
        
        if passing_data:
            # Save each dataframe with actual endpoint dataset names
            dataframe_names = [
                'PassesMade',
                'PassesReceived'
            ]
            
            for i, df_pass in enumerate(passing_data):
                if not df_pass.empty and i < len(dataframe_names):
                    filename = f'../data/raw/{player_id}_{dataframe_names[i]}.csv'
                    df_pass.to_csv(filename, index=False)
                    print(f"saved {dataframe_names[i]} for {player_name}.")
        
        time.sleep(delay)

if __name__ == "__main__":
    # top200 = fetch_top_200_pp48()
    
    # Uncomment the line below to fetch basic shot chart data for all 200 players
    # fetch_save_advanced_data(top200)
    
    # fetch_save_shot_tracking_data(top200)
    
    # 8/14 added new endpoints
    # fetch_save_basketball_iq_data()
    # fetch_save_passing_data(top200)
    
    # Fetch Jimmy Butler's data since he's known for high basketball IQ
    # Uncomment the line below to fetch Jimmy Butler's data
    fetch_jimmy_butler_data()

    print("data already collected no overwriting")
