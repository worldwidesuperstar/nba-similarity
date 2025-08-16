import pandas as pd
import numpy as np
import os
from pathlib import Path

def calculate_league_averages():
    """Calculate league averages for all IQ metrics to use as fallbacks."""
    data_path = Path('../data/raw/')
    top200 = pd.read_csv(data_path / 'top200_per.csv')
    
    # Calculate basic metric averages from top200 players
    league_avg_ast_tov = (top200['AST'] / top200['TOV'].replace(0, np.nan)).mean()
    league_avg_efg = ((top200['FGM'] + 0.5 * top200['FG3M']) / top200['FGA'].replace(0, np.nan)).mean()
    
    # Load league files for other averages
    try:
        hustle_stats = pd.read_csv(data_path / 'league_hustle_stats.csv')
        clutch_stats = pd.read_csv(data_path / 'league_clutch_stats.csv')
        
        league_averages = {
            'ast_tov_ratio': league_avg_ast_tov,
            'late_clock_efficiency': 0.35,  # Typical late clock efficiency
            'clutch_ast_tov': (clutch_stats['AST'] / clutch_stats['TOV'].replace(0, np.nan)).mean(),
            'efg_pct': league_avg_efg,
            'deflections_per_36': hustle_stats['DEFLECTIONS'].mean(),
            'screen_assists_per_36': hustle_stats['SCREEN_ASSISTS'].mean(),
            'quick_decision_efficiency': 0.45,  # Typical quick decision efficiency
            'loose_balls_per_36': hustle_stats['LOOSE_BALLS_RECOVERED'].mean(),
            'shooting_foul_pct': 3.0,  # Typical shooting foul percentage
            'successful_boxouts_per_36': hustle_stats['BOX_OUT_PLAYER_REBS'].mean(),
            'charges_drawn_per_36': hustle_stats['CHARGES_DRAWN'].mean(),
            'shot_selection_value': 0.50  # Typical shot selection value
        }
        
    except Exception as e:
        print(f"Warning: Could not load league files for averages: {e}")
        # Fallback averages if league files are missing
        league_averages = {
            'ast_tov_ratio': 1.8,
            'late_clock_efficiency': 0.35,
            'clutch_ast_tov': 1.5,
            'efg_pct': 0.54,
            'deflections_per_36': 2.8,
            'screen_assists_per_36': 2.5,
            'quick_decision_efficiency': 0.45,
            'loose_balls_per_36': 1.2,
            'shooting_foul_pct': 3.0,
            'successful_boxouts_per_36': 3.5,
            'charges_drawn_per_36': 0.3,
            'shot_selection_value': 0.50
        }
    
    return league_averages

def load_player_data(player_id):
    """Load all necessary data files for a player."""
    data_path = Path('../data/raw/')
    
    try:
        # Load basic stats from top200
        top200 = pd.read_csv(data_path / 'top200_per.csv')
        basic_stats = top200[top200['PLAYER_ID'] == int(player_id)]
        if basic_stats.empty:
            print(f"Player {player_id} not found in top200_per.csv")
            return None
            
        basic_stats = basic_stats.iloc[0]
        player_name = basic_stats['PLAYER']
        
        # Load additional data files
        files_to_load = {
            'general_splits': f'{player_id}_general_splits.csv',
            'closest_defender': f'{player_id}_ClosestDefenderShooting.csv',
            'dribble_shooting': f'{player_id}_DribbleShooting.csv',  # Contains shot clock data
            'touch_time': f'{player_id}_TouchTimeShooting.csv'
        }
        
        loaded_data = {'basic_stats': basic_stats}
        missing_files = []
        
        for key, filename in files_to_load.items():
            file_path = data_path / filename
            if file_path.exists():
                try:
                    loaded_data[key] = pd.read_csv(file_path)
                except Exception as e:
                    print(f"Error reading {filename} for {player_name} (ID: {player_id}): {e}")
                    loaded_data[key] = pd.DataFrame()
                    missing_files.append(filename)
            else:
                loaded_data[key] = pd.DataFrame()
                missing_files.append(filename)
        
        # Load league-wide data
        league_files = {
            'hustle_stats': 'league_hustle_stats.csv',
            'clutch_stats': 'league_clutch_stats.csv'
        }
        
        for key, filename in league_files.items():
            file_path = data_path / filename
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path)
                    player_data = df[df['PLAYER_ID'] == int(player_id)]
                    if player_data.empty:
                        print(f"Player {player_name} (ID: {player_id}) not found in {filename}")
                        loaded_data[key] = pd.Series()
                    else:
                        loaded_data[key] = player_data.iloc[0]
                except Exception as e:
                    print(f"Error reading {filename} for {player_name} (ID: {player_id}): {e}")
                    loaded_data[key] = pd.Series()
            else:
                loaded_data[key] = pd.Series()
                print(f"League file {filename} not found")
        
        if missing_files:
            print(f"Missing files for {player_name} (ID: {player_id}): {missing_files}")
        
        return loaded_data
        
    except Exception as e:
        print(f"Critical error loading data for player {player_id}: {e}")
        return None

def calculate_metric_1_ast_tov_ratio(data):
    """1. Assist-to-Turnover Ratio"""
    try:
        basic = data['basic_stats']
        ast = basic['AST']
        tov = basic['TOV']
        return ast / tov if tov > 0 else np.inf
    except:
        return np.nan

def calculate_metric_2_late_clock_efficiency(data):
    """2. Late Clock Efficiency"""
    try:
        dribble_shooting = data['dribble_shooting']
        if dribble_shooting.empty:
            return np.nan
            
        late_clock = dribble_shooting[dribble_shooting['SHOT_CLOCK_RANGE'] == '7-4 Late']
        very_late_clock = dribble_shooting[dribble_shooting['SHOT_CLOCK_RANGE'] == '4-0 Very Late']
        
        if late_clock.empty or very_late_clock.empty:
            return np.nan
            
        late_fg_pct = late_clock['FG_PCT'].iloc[0]
        very_late_fg_pct = very_late_clock['FG_PCT'].iloc[0]
        late_freq = late_clock['FGA_FREQUENCY'].iloc[0]
        very_late_freq = very_late_clock['FGA_FREQUENCY'].iloc[0]
        
        if late_freq + very_late_freq == 0:
            return np.nan
            
        combined_efficiency = (late_fg_pct * late_freq + very_late_fg_pct * very_late_freq) / (late_freq + very_late_freq)
        return combined_efficiency
    except:
        return np.nan

def calculate_metric_3_clutch_ast_tov(data):
    """3. Clutch AST/TOV Ratio"""
    try:
        clutch = data['clutch_stats']
        if clutch.empty:
            return np.nan
            
        ast = clutch['AST']
        tov = clutch['TOV']
        
        if tov > 0:
            return ast / tov
        else:
            # If 0 clutch turnovers, use regular AST/TOV ratio but make it 10% worse
            # since clutch situations are more pressure-filled
            basic = data['basic_stats']
            regular_ast_tov = basic['AST'] / basic['TOV'] if basic['TOV'] > 0 else 3.0
            return regular_ast_tov * 0.9
    except:
        return np.nan

def calculate_metric_4_efg_pct(data):
    """4. Effective Field Goal %"""
    try:
        basic = data['basic_stats']
        fgm = basic['FGM']
        fg3m = basic['FG3M']
        fga = basic['FGA']
        return (fgm + 0.5 * fg3m) / fga if fga > 0 else 0
    except:
        return np.nan

def calculate_metric_5_deflections_per_36(data):
    """5. Deflections per 36"""
    try:
        hustle = data['hustle_stats']
        if hustle.empty:
            return np.nan
        return hustle['DEFLECTIONS']
    except:
        return np.nan

def calculate_metric_6_screen_assists_per_36(data):
    """6. Screen Assists per 36"""
    try:
        hustle = data['hustle_stats']
        if hustle.empty:
            return np.nan
        return hustle['SCREEN_ASSISTS']
    except:
        return np.nan

def calculate_metric_7_quick_decision_efficiency(data):
    """7. Quick Decision Efficiency"""
    try:
        touch_time = data['touch_time']
        if touch_time.empty:
            return np.nan
            
        quick_decision = touch_time[touch_time['TOUCH_TIME_RANGE'] == 'Touch < 2 Seconds']
        if quick_decision.empty:
            return np.nan
            
        return quick_decision['FG_PCT'].iloc[0]
    except:
        return np.nan

def calculate_metric_8_loose_balls_per_36(data):
    """8. Loose Balls Recovered per 36"""
    try:
        hustle = data['hustle_stats']
        if hustle.empty:
            return np.nan
        return hustle['LOOSE_BALLS_RECOVERED']
    except:
        return np.nan

def calculate_metric_9_shooting_foul_percentage(data):
    """9. Shooting Foul Percentage (lower is better) - Now using real Basketball Reference shooting fouls"""
    try:
        general_splits = data['general_splits']
        closest_defender = data['closest_defender']
        basic_stats = data['basic_stats']
        
        if general_splits.empty or closest_defender.empty:
            return np.nan
            
        # Use overall stats row (total season stats)
        overall_stats = general_splits.iloc[0]
        games_played = overall_stats['GP']
        player_name = basic_stats['PLAYER']
        
        # Calculate total shots defended
        shots_defended_per_game = closest_defender['FGA'].sum()
        total_shots_defended = shots_defended_per_game * games_played
        
        if total_shots_defended == 0:
            return np.nan
            
        # Get actual shooting fouls from Basketball Reference data
        shooting_fouls = get_actual_shooting_fouls(player_name)
        
        # Calculate shooting foul percentage
        shooting_foul_percentage = (shooting_fouls / total_shots_defended) * 100
        return shooting_foul_percentage
    except:
        return np.nan

def get_actual_shooting_fouls(player_name):
    """Get actual shooting fouls committed by player from Basketball Reference data."""
    try:
        # Load Basketball Reference shooting fouls data
        shooting_fouls_df = pd.read_csv('../data/processed/shooting_fouls_bbref_2024.csv')
        
        # Try exact name match first
        exact_match = shooting_fouls_df[shooting_fouls_df['Player'] == player_name]
        if not exact_match.empty:
            return exact_match.iloc[0]['Fouls Committed_Shoot']
        
        # Try partial name matching (last name)
        player_last_name = player_name.split()[-1]
        for _, row in shooting_fouls_df.iterrows():
            bbref_name = row['Player']
            if player_last_name in bbref_name or bbref_name.split()[-1] in player_name:
                return row['Fouls Committed_Shoot']
        
        # If not found, estimate using league average rate
        # League average is about 36.9 shooting fouls per player
        return 37  # Fallback to league average
        
    except Exception as e:
        print(f"Warning: Could not load shooting fouls for {player_name}: {e}")
        return 37  # Fallback to league average

def calculate_metric_10_successful_boxouts_per_36(data):
    """10. Successful Box Outs per 36"""
    try:
        hustle = data['hustle_stats']
        if hustle.empty:
            return np.nan
        return hustle['BOX_OUT_PLAYER_REBS']
    except:
        return np.nan

def calculate_metric_11_charges_drawn_per_36(data):
    """11. Charges Drawn per 36"""
    try:
        hustle = data['hustle_stats']
        if hustle.empty:
            return np.nan
        return hustle['CHARGES_DRAWN']
    except:
        return np.nan

def calculate_metric_12_shot_selection_value(data):
    """12. Personalized Shot Selection Intelligence"""
    try:
        closest_defender = data['closest_defender']
        if closest_defender.empty:
            return np.nan
            
        # Extract key shot types
        close_shots = closest_defender[closest_defender['SHOT_TYPE'] == 'Less than 10 ft']
        catch_shoot = closest_defender[closest_defender['SHOT_TYPE'] == 'Catch and Shoot']
        pull_ups = closest_defender[closest_defender['SHOT_TYPE'] == 'Pull Ups']
        
        if close_shots.empty or catch_shoot.empty or pull_ups.empty:
            return np.nan
            
        # Calculate shot selection value (frequency weighted by efficiency)
        close_range_value = close_shots.iloc[0]['FGA_FREQUENCY'] * (close_shots.iloc[0]['FG_PCT'] * 2)  # 2 points
        catch_shoot_value = catch_shoot.iloc[0]['FGA_FREQUENCY'] * catch_shoot.iloc[0]['EFG_PCT']
        pull_up_value = pull_ups.iloc[0]['FGA_FREQUENCY'] * pull_ups.iloc[0]['EFG_PCT']
        
        total_shot_value = close_range_value + catch_shoot_value + pull_up_value
        return total_shot_value
    except:
        return np.nan

def calculate_all_metrics_for_player(player_id, league_averages=None):
    """Calculate all 12 IQ metrics for a single player."""
    data = load_player_data(player_id)
    if data is None:
        return None
    
    basic = data['basic_stats']
    player_name = basic['PLAYER']
    
    # Get league averages if not provided
    if league_averages is None:
        league_averages = calculate_league_averages()
    
    # Track which metrics use league averages
    using_league_averages = []
    
    def safe_calculate(metric_func, metric_name, data):
        try:
            result = metric_func(data)
            if pd.isna(result):
                # Use league average as fallback
                result = league_averages.get(metric_name, np.nan)
                using_league_averages.append(metric_name)
            return result
        except Exception as e:
            # Use league average as fallback
            result = league_averages.get(metric_name, np.nan)
            using_league_averages.append(f"{metric_name} (Error)")
            return result
    
    metrics = {
        'PLAYER_ID': int(player_id),
        'PLAYER_NAME': player_name,
        'TEAM': basic['TEAM'],
        'GP': basic['GP'],
        'MIN': basic['MIN'],
        
        # IQ Metrics
        'ast_tov_ratio': safe_calculate(calculate_metric_1_ast_tov_ratio, 'ast_tov_ratio', data),
        'late_clock_efficiency': safe_calculate(calculate_metric_2_late_clock_efficiency, 'late_clock_efficiency', data),
        'clutch_ast_tov': safe_calculate(calculate_metric_3_clutch_ast_tov, 'clutch_ast_tov', data),
        'efg_pct': safe_calculate(calculate_metric_4_efg_pct, 'efg_pct', data),
        'deflections_per_36': safe_calculate(calculate_metric_5_deflections_per_36, 'deflections_per_36', data),
        'screen_assists_per_36': safe_calculate(calculate_metric_6_screen_assists_per_36, 'screen_assists_per_36', data),
        'quick_decision_efficiency': safe_calculate(calculate_metric_7_quick_decision_efficiency, 'quick_decision_efficiency', data),
        'loose_balls_per_36': safe_calculate(calculate_metric_8_loose_balls_per_36, 'loose_balls_per_36', data),
        'shooting_foul_pct': safe_calculate(calculate_metric_9_shooting_foul_percentage, 'shooting_foul_pct', data),
        'successful_boxouts_per_36': safe_calculate(calculate_metric_10_successful_boxouts_per_36, 'successful_boxouts_per_36', data),
        'charges_drawn_per_36': safe_calculate(calculate_metric_11_charges_drawn_per_36, 'charges_drawn_per_36', data),
        'shot_selection_value': safe_calculate(calculate_metric_12_shot_selection_value, 'shot_selection_value', data)
    }
    
    if using_league_averages:
        print(f"  Using league averages for {player_name} (ID: {player_id}): {', '.join(using_league_averages)}")
    
    return metrics

def process_all_players():
    """Process all 200 players and calculate their IQ metrics."""
    # Load the list of all players
    top200 = pd.read_csv('../data/raw/top200_per.csv')
    
    # Minimum games played filter
    min_games = 55
    eligible_players = top200[top200['GP'] >= min_games]
    
    print(f"Processing {len(eligible_players)} players (minimum {min_games} games played)")
    
    # Calculate league averages once for efficiency
    print("Calculating league averages...")
    league_averages = calculate_league_averages()
    print("League averages calculated.")
    
    all_metrics = []
    failed_players = []
    
    for _, player in eligible_players.iterrows():
        player_id = str(player['PLAYER_ID'])
        player_name = player['PLAYER']
        
        print(f"Processing {player_name} (ID: {player_id})...")
        
        try:
            metrics = calculate_all_metrics_for_player(player_id, league_averages)
            if metrics:
                all_metrics.append(metrics)
                print(f"  Successfully processed {player_name}")
            else:
                failed_players.append((player_name, player_id, "Data loading failed"))
                print(f"  Failed to process {player_name} - Data loading failed")
        except Exception as e:
            failed_players.append((player_name, player_id, f"Exception: {str(e)}"))
            print(f"  Failed to process {player_name} - Exception: {str(e)}")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_metrics)
    
    # Report failed players
    if failed_players:
        print(f"\n=== FAILED PLAYERS ({len(failed_players)}/{len(eligible_players)}) ===")
        for name, player_id, reason in failed_players:
            print(f"  {name} (ID: {player_id}) - {reason}")
    else:
        print(f"\nAll {len(eligible_players)} players processed successfully!")
    
    # Create processed data directory if it doesn't exist
    os.makedirs('../data/processed', exist_ok=True)
    
    output_file = '../data/processed/all_player_iq_metrics.csv'
    
    df.to_csv(output_file, index=False, float_format='%.3f')
    
    print(f"\nProcessed {len(df)} players")
    print(f"Results saved to {output_file}")
    
    # Print summary statistics
    print("\n=== DATA AVAILABILITY SUMMARY ===")
    for col in df.columns:
        if col not in ['PLAYER_ID', 'PLAYER_NAME', 'TEAM', 'GP', 'MIN']:
            non_null_count = df[col].notna().sum()
            print(f"{col}: {non_null_count}/{len(df)} players ({non_null_count/len(df)*100:.1f}%)")
    
    return df

if __name__ == "__main__":
    results = process_all_players()