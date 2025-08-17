#!/usr/bin/env python3

import pandas as pd
import numpy as np
from nba_api.stats.endpoints import (
    leagueleaders, playerdashboardbygeneralsplits, playerdashptshots,
    leaguehustlestatsplayer, leaguedashplayerclutch, commonplayerinfo
)
import time

def get_player_info(player_id):
    try:
        # Get player info from CommonPlayerInfo endpoint
        import time
        time.sleep(2)
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        player_data = player_info.get_data_frames()[0].iloc[0]
        
        player_name = player_data['DISPLAY_FIRST_LAST']
        team_id = player_data['TEAM_ID']
        team_abbrev = player_data['TEAM_ABBREVIATION']
        position = player_data['POSITION']
        
        # Get basic stats from general splits
        dash = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(
            player_id=player_id,
            season='2024-25'
        )
        overall_stats = dash.get_data_frames()[0]  # Overall season stats
        player_basic = overall_stats.iloc[0]
        print(overall_stats.head())
        
        return player_name, player_basic, team_id, team_abbrev, position
    except Exception as e:
        print(f"Error getting player info for ID {player_id}: {e}")
        return None, None, None, None, None

def calculate_player_iq(player_id, team_id=None):
    """
    Calculate all 12 Basketball IQ metrics for any player and return as a dict
    that can be manually added to the all_player_iq_metrics.csv
    """
    
    season = '2024-25'
    
    print(f"Getting player information for ID: {player_id}...")
    
    player_name, player_basic, player_team_id, team_abbrev, position = get_player_info(player_id)
    
    if player_name is None:
        print(f"Could not find player with ID {player_id}")
        return None
    
    print(f"Calculating Basketball IQ metrics for {player_name} ({position}, {team_abbrev})...")
    
    # Use the team_id from player info if not provided
    if team_id is None:
        team_id = player_team_id
        print(f"Using team ID {team_id} for {team_abbrev}")
    
    # Get general splits
    print("Getting general splits...")
    dash = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(
        player_id=player_id,
        season=season
    )
    general_splits = dash.get_data_frames()[0]  # Overall season stats
    
    # Get shot tracking data
    print("Fetching shot tracking data...")
    try:
        shot_tracking = playerdashptshots.PlayerDashPtShots(
            player_id=player_id,
            team_id=team_id,
            season=season,
            season_type_all_star='Regular Season',
            per_mode_simple='Per36',
        )
        tracking_dfs = shot_tracking.get_data_frames()
        
        closest_defender = tracking_dfs[1] if len(tracking_dfs) > 1 else pd.DataFrame()
        dribble_shooting = tracking_dfs[2] if len(tracking_dfs) > 2 else pd.DataFrame()
        touch_time = tracking_dfs[6] if len(tracking_dfs) > 6 else pd.DataFrame()
    except Exception as e:
        print(f"Warning: Could not get shot tracking data: {e}")
        closest_defender = pd.DataFrame()
        dribble_shooting = pd.DataFrame()
        touch_time = pd.DataFrame()
    
    # Get hustle stats
    print("Fetching hustle stats...")
    try:
        hustle = leaguehustlestatsplayer.LeagueHustleStatsPlayer(
            per_mode_time='Per36',
            season=season,
            season_type_all_star='Regular Season'
        )
        hustle_df = hustle.get_data_frames()[0]
        player_hustle = hustle_df[hustle_df['PLAYER_ID'] == player_id]
    except Exception as e:
        print(f"Warning: Could not get hustle stats: {e}")
        player_hustle = pd.DataFrame()
    
    # Get clutch stats
    print("Fetching clutch stats...")
    try:
        clutch = leaguedashplayerclutch.LeagueDashPlayerClutch(
            ahead_behind='Ahead or Behind',
            clutch_time='Last 5 Minutes',
            measure_type_detailed_defense='Base',
            per_mode_detailed='Per36',
            season=season,
            season_type_all_star='Regular Season'
        )
        clutch_df = clutch.get_data_frames()[0]
        player_clutch = clutch_df[clutch_df['PLAYER_ID'] == player_id]
    except Exception as e:
        print(f"Warning: Could not get clutch stats: {e}")
        player_clutch = pd.DataFrame()
    
    print("Calculating IQ metrics...")
    
    # Now calculate all 12 metrics
    metrics = {
        'PLAYER_ID': player_id,
        'PLAYER_NAME': player_name,
        'TEAM': team_abbrev,
        'POSITION': position,
        'GP': player_basic['GP'],
        'MIN': player_basic['MIN'] / player_basic['GP']
    }
    
    # 1. AST/TOV Ratio
    metrics['ast_tov_ratio'] = player_basic['AST'] / player_basic['TOV'] if player_basic['TOV'] > 0 else 20.0
    
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
    if not player_clutch.empty:
        clutch_ast = player_clutch.iloc[0]['AST']
        clutch_tov = player_clutch.iloc[0]['TOV']
        
        if clutch_tov > 0:
            metrics['clutch_ast_tov'] = clutch_ast / clutch_tov
        else:
            # Use regular AST/TOV * 0.9 for clutch situations
            metrics['clutch_ast_tov'] = metrics['ast_tov_ratio'] * 0.9
    else:
        metrics['clutch_ast_tov'] = metrics['ast_tov_ratio'] * 0.9
    
    # 4. Effective Field Goal %
    metrics['efg_pct'] = (player_basic['FGM'] + 0.5 * player_basic['FG3M']) / player_basic['FGA']
    
    # 5-11. Hustle stats (all per 36)
    if not player_hustle.empty:
        hustle_data = player_hustle.iloc[0]
        metrics['deflections_per_36'] = hustle_data['DEFLECTIONS']
        metrics['screen_assists_per_36'] = hustle_data['SCREEN_ASSISTS']
        metrics['loose_balls_per_36'] = hustle_data['LOOSE_BALLS_RECOVERED']
        metrics['successful_boxouts_per_36'] = hustle_data['BOX_OUT_PLAYER_REBS']
        metrics['charges_drawn_per_36'] = hustle_data['CHARGES_DRAWN']
    else:
        # Use league averages
        print("Using league averages for hustle stats (player not found in hustle data)")
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
        shooting_fouls_df = pd.read_csv('data/processed/shooting_fouls_bbref_2024.csv')
        player_shooting_fouls = shooting_fouls_df[shooting_fouls_df['Player'].str.contains(player_name.split()[-1], na=False)]
        
        if not player_shooting_fouls.empty:
            shooting_fouls = player_shooting_fouls.iloc[0]['Fouls Committed_Shoot']
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
    
    print(f"\n=== {player_name.upper()}'S BASKETBALL IQ METRICS ===")
    for metric, value in metrics.items():
        if metric not in ['PLAYER_ID', 'PLAYER_NAME', 'TEAM', 'POSITION']:
            print(f"{metric}: {value:.3f}")
    
    return metrics

def add_player_to_csv(player_metrics):
    """Add player's metrics to the all_player_iq_metrics.csv file."""
    
    if player_metrics is None:
        print("No metrics to add")
        return
    
    try:
        # Load existing metrics
        df = pd.read_csv('data/processed/all_player_iq_metrics.csv')
        
        # Check if player is already in the data
        if player_metrics['PLAYER_ID'] in df['PLAYER_ID'].values:
            # Update existing player data
            for col, value in player_metrics.items():
                df.loc[df['PLAYER_ID'] == player_metrics['PLAYER_ID'], col] = value
            df.to_csv('data/processed/all_player_iq_metrics.csv', index=False)
            print(f"\nUpdated {player_metrics['PLAYER_NAME']} in all_player_iq_metrics.csv")
        elif player_metrics['PLAYER_ID'] not in df['PLAYER_ID'].values:
            # Add player's metrics as a new row
            new_row = pd.DataFrame([player_metrics])
            df_updated = pd.concat([df, new_row], ignore_index=True)
            
            # Save updated CSV
            df_updated.to_csv('data/processed/all_player_iq_metrics.csv', index=False)
            print(f"\nAdded {player_metrics['PLAYER_NAME']} to all_player_iq_metrics.csv")
            print(f"Total players now: {len(df_updated)}")
            
    except Exception as e:
        print(f"\nError adding to CSV: {e}")
        print("Manual addition required:")
        print(player_metrics)

def main():
    """Main function to get user input and calculate IQ metrics."""
    
    print("=== NBA PLAYER BASKETBALL IQ CALCULATOR ===")
    print()
    print("Common player IDs:")
    print("- Kawhi Leonard: 202695")
    print("- Jimmy Butler: 202710") 
    print("- LeBron James: 2544")
    print("- Stephen Curry: 201939")
    print("- Giannis Antetokounmpo: 203507")
    print()
    
    while True:
        try:
            player_id_input = input("Enter NBA player ID (or 'quit' to exit): ").strip()
            
            if player_id_input.lower() == 'quit':
                print("Goodbye!")
                break
                
            player_id = int(player_id_input)
            
            # Optional: Ask for team ID
            team_id_input = input("Enter team ID (optional, press Enter to skip): ").strip()
            team_id = int(team_id_input) if team_id_input else None
            
            # Calculate metrics
            player_metrics = calculate_player_iq(player_id, team_id)
            
            if player_metrics:
                # Ask if user wants to add to CSV
                add_to_csv = input(f"\nAdd {player_metrics['PLAYER_NAME']} to dataset? (y/n): ").strip().lower()
                
                if add_to_csv == 'y':
                    add_player_to_csv(player_metrics)
                else:
                    print("Metrics calculated but not added to dataset.")
            
            print("\n" + "="*50 + "\n")
            
        except ValueError:
            print("Please enter a valid player ID (numbers only)")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nInput terminated. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()