#!/usr/bin/env python3

import pandas as pd
import numpy as np
from nba_api.stats.endpoints import (
    leagueleaders, playerdashboardbygeneralsplits, playerdashptshots,
    leaguehustlestatsplayer, leaguedashplayerclutch
)
import time

def calculate_jimmy_butler_iq():
    """
    Calculate all 12 Basketball IQ metrics for Jimmy Butler and return as a dict
    that can be manually added to the all_player_iq_metrics.csv
    """
    
    # Jimmy Butler's info
    jimmy_butler_id = 202710
    miami_heat_id = 1610612748
    player_name = "Jimmy Butler"
    season = '2024-25'
    
    print(f"Calculating Basketball IQ metrics for {player_name}...")
    
    # Get basic stats from general splits (which has all the basic stats we need)
    print("Fetching basic stats...")
    dash = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(
        player_id=jimmy_butler_id,
        season=season
    )
    overall_stats = dash.get_data_frames()[0]  # Overall stats (first dataframe)
    jimmy_basic = overall_stats.iloc[0]  # Get the overall row
    
    # Get general splits (we already have the dashboard object)
    print("Getting general splits...")
    general_splits = dash.get_data_frames()[1]
    
    # Get shot tracking data
    print("Fetching shot tracking data...")
    shot_tracking = playerdashptshots.PlayerDashPtShots(
        player_id=jimmy_butler_id,
        team_id=miami_heat_id,
        season=season,
        season_type_all_star='Regular Season',
        per_mode_simple='Per36',
    )
    tracking_dfs = shot_tracking.get_data_frames()
    
    closest_defender = tracking_dfs[1] if len(tracking_dfs) > 1 else pd.DataFrame()
    dribble_shooting = tracking_dfs[2] if len(tracking_dfs) > 2 else pd.DataFrame()
    touch_time = tracking_dfs[6] if len(tracking_dfs) > 6 else pd.DataFrame()
    
    # Get hustle stats
    print("Fetching hustle stats...")
    hustle = leaguehustlestatsplayer.LeagueHustleStatsPlayer(
        per_mode_time='Per36',
        season=season,
        season_type_all_star='Regular Season'
    )
    hustle_df = hustle.get_data_frames()[0]
    jimmy_hustle = hustle_df[hustle_df['PLAYER_ID'] == jimmy_butler_id]
    
    # Get clutch stats
    print("Fetching clutch stats...")
    clutch = leaguedashplayerclutch.LeagueDashPlayerClutch(
        ahead_behind='Ahead or Behind',
        clutch_time='Last 5 Minutes',
        measure_type_detailed_defense='Base',
        per_mode_detailed='Per36',
        season=season,
        season_type_all_star='Regular Season'
    )
    clutch_df = clutch.get_data_frames()[0]
    jimmy_clutch = clutch_df[clutch_df['PLAYER_ID'] == jimmy_butler_id]
    
    print("Calculating IQ metrics...")
    
    # Now calculate all 12 metrics
    metrics = {
        'PLAYER_ID': jimmy_butler_id,
        'PLAYER_NAME': player_name,
        'TEAM': 'MIA',  # Miami Heat
        'GP': jimmy_basic['GP'],
        'MIN': jimmy_basic['MIN']
    }
    
    # 1. AST/TOV Ratio
    metrics['ast_tov_ratio'] = jimmy_basic['AST'] / jimmy_basic['TOV'] if jimmy_basic['TOV'] > 0 else 20.0
    
    # 2. Late Clock Efficiency
    if not dribble_shooting.empty:
        late_clock = dribble_shooting[dribble_shooting['SHOT_CLOCK_RANGE'] == '7-4 Late']
        very_late_clock = dribble_shooting[dribble_shooting['SHOT_CLOCK_RANGE'] == '4-0 Very Late']
        
        if not late_clock.empty and not very_late_clock.empty:
            late_fg_pct = late_clock['FG_PCT'].iloc[0]
            very_late_fg_pct = very_late_clock['FG_PCT'].iloc[0]
            late_freq = late_clock['FGA_FREQUENCY'].iloc[0]
            very_late_freq = very_late_clock['FGA_FREQUENCY'].iloc[0]
            
            if late_freq + very_late_freq > 0:
                metrics['late_clock_efficiency'] = (late_fg_pct * late_freq + very_late_fg_pct * very_late_freq) / (late_freq + very_late_freq)
            else:
                metrics['late_clock_efficiency'] = 0.403  # League average
        else:
            metrics['late_clock_efficiency'] = 0.403  # League average
    else:
        metrics['late_clock_efficiency'] = 0.403  # League average
    
    # 3. Clutch AST/TOV
    if not jimmy_clutch.empty:
        clutch_ast = jimmy_clutch.iloc[0]['AST']
        clutch_tov = jimmy_clutch.iloc[0]['TOV']
        
        if clutch_tov > 0:
            metrics['clutch_ast_tov'] = clutch_ast / clutch_tov
        else:
            # Use regular AST/TOV * 0.9 for clutch situations
            metrics['clutch_ast_tov'] = metrics['ast_tov_ratio'] * 0.9
    else:
        metrics['clutch_ast_tov'] = metrics['ast_tov_ratio'] * 0.9
    
    # 4. Effective Field Goal %
    metrics['efg_pct'] = (jimmy_basic['FGM'] + 0.5 * jimmy_basic['FG3M']) / jimmy_basic['FGA']
    
    # 5-11. Hustle stats (all per 36)
    if not jimmy_hustle.empty:
        hustle_data = jimmy_hustle.iloc[0]
        metrics['deflections_per_36'] = hustle_data['DEFLECTIONS']
        metrics['screen_assists_per_36'] = hustle_data['SCREEN_ASSISTS']
        metrics['loose_balls_per_36'] = hustle_data['LOOSE_BALLS_RECOVERED']
        metrics['successful_boxouts_per_36'] = hustle_data['BOX_OUT_PLAYER_REBS']
        metrics['charges_drawn_per_36'] = hustle_data['CHARGES_DRAWN']
    else:
        # Use league averages
        metrics['deflections_per_36'] = 2.392
        metrics['screen_assists_per_36'] = 1.094
        metrics['loose_balls_per_36'] = 0.702
        metrics['successful_boxouts_per_36'] = 0.462
        metrics['charges_drawn_per_36'] = 0.044
    
    # 7. Quick Decision Efficiency
    if not touch_time.empty:
        quick_decision = touch_time[touch_time['TOUCH_TIME_RANGE'] == 'Touch < 2 Seconds']
        if not quick_decision.empty:
            metrics['quick_decision_efficiency'] = quick_decision['FG_PCT'].iloc[0]
        else:
            metrics['quick_decision_efficiency'] = 0.471  # League average
    else:
        metrics['quick_decision_efficiency'] = 0.471  # League average
    
    # 9. Shooting Foul Percentage (using real Basketball Reference data)
    try:
        shooting_fouls_df = pd.read_csv('../data/processed/shooting_fouls_bbref_2024.csv')
        jimmy_shooting_fouls = shooting_fouls_df[shooting_fouls_df['Player'].str.contains('Jimmy Butler', na=False)]
        
        if not jimmy_shooting_fouls.empty:
            shooting_fouls = jimmy_shooting_fouls.iloc[0]['Fouls Committed_Shoot']
        else:
            shooting_fouls = 37  # League average
    except:
        shooting_fouls = 37  # League average
    
    # Calculate shots defended estimate
    if not closest_defender.empty and not general_splits.empty:
        shots_defended_per_game = closest_defender['FGA'].sum()
        games_played = general_splits.iloc[0]['GP']
        total_shots_defended = shots_defended_per_game * games_played
        
        if total_shots_defended > 0:
            metrics['shooting_foul_pct'] = (shooting_fouls / total_shots_defended) * 100
        else:
            metrics['shooting_foul_pct'] = 1.69  # League average per 36
    else:
        metrics['shooting_foul_pct'] = 1.69  # League average per 36
    
    # 12. Shot Selection Value
    if not closest_defender.empty:
        # Extract key zones
        close_shots = closest_defender[closest_defender['SHOT_TYPE'] == 'Less than 10 ft']
        catch_shoot = closest_defender[closest_defender['SHOT_TYPE'] == 'Catch and Shoot']
        pull_ups = closest_defender[closest_defender['SHOT_TYPE'] == 'Pull Ups']
        
        if not close_shots.empty and not catch_shoot.empty and not pull_ups.empty:
            close_range_value = close_shots.iloc[0]['FGA_FREQUENCY'] * (close_shots.iloc[0]['FG_PCT'] * 2)
            catch_shoot_value = catch_shoot.iloc[0]['FGA_FREQUENCY'] * catch_shoot.iloc[0]['EFG_PCT']
            pull_up_value = pull_ups.iloc[0]['FGA_FREQUENCY'] * pull_ups.iloc[0]['EFG_PCT']
            
            metrics['shot_selection_value'] = close_range_value + catch_shoot_value + pull_up_value
        else:
            metrics['shot_selection_value'] = 0.794  # League average
    else:
        metrics['shot_selection_value'] = 0.794  # League average
    
    print("\n=== JIMMY BUTLER'S BASKETBALL IQ METRICS ===")
    for metric, value in metrics.items():
        if metric not in ['PLAYER_ID', 'PLAYER_NAME', 'TEAM']:
            print(f"{metric}: {value:.3f}")
    
    return metrics

def add_jimmy_to_csv(jimmy_metrics):
    """Add Jimmy Butler's metrics to the all_player_iq_metrics.csv file."""
    
    try:
        # Load existing metrics
        df = pd.read_csv('../data/processed/all_player_iq_metrics.csv')
        
        # Check if Jimmy Butler is already in the data
        if jimmy_metrics['PLAYER_ID'] not in df['PLAYER_ID'].values:
            # Add Jimmy's metrics as a new row
            new_row = pd.DataFrame([jimmy_metrics])
            df_updated = pd.concat([df, new_row], ignore_index=True)
            
            # Save updated CSV
            df_updated.to_csv('../data/processed/all_player_iq_metrics.csv', index=False)
            print(f"\nAdded Jimmy Butler to all_player_iq_metrics.csv")
            print(f"Total players now: {len(df_updated)}")
        else:
            print("\nJimmy Butler already exists in the dataset")
            
    except Exception as e:
        print(f"\nError adding to CSV: {e}")
        print("Manual addition required:")
        print(jimmy_metrics)

if __name__ == "__main__":
    # Calculate Jimmy Butler's metrics
    jimmy_metrics = calculate_jimmy_butler_iq()
    
    # Add to CSV
    add_jimmy_to_csv(jimmy_metrics)