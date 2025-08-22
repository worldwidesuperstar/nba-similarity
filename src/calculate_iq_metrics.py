import pandas as pd
import numpy as np
from pathlib import Path
from nba_api.stats.endpoints import commonplayerinfo

def get_player_position(player_name):
    """ retrieve player position from bbref data """
    try:

        basic_stats_df = pd.read_csv('data/processed/basic_stats_36_bbref.csv')
        player_row = basic_stats_df[basic_stats_df['Player'] == player_name]
        
        if player_row.empty:
            print("unknown pos")
            return 'Unknown'
        
        position = player_row.iloc[0]['Pos']
        return position
        
    except Exception as e:
        print(f"Could not get position for player {player_name}: {e}")
        return 'Unknown'

def load_player_data(player_id):
    """ load basic stats and all relevant CSV files for one player """
    
    try:
        top300 = pd.read_csv('data/top300_per.csv')
        basic_stats = top300[top300['PLAYER_ID'] == int(player_id)]
        if basic_stats.empty:
            print(f"Player {player_id} not found in top300_per.csv")
            return None
            
        basic_stats = basic_stats.iloc[0]
        player_name = basic_stats['PLAYER_NAME']
        
        position = get_player_position(player_name)
        
        files_to_load = {
            'general_splits': f'{player_id}_general_splits.csv',
            'closest_defender': f'{player_id}_ClosestDefenderShooting.csv',
            'dribble_shooting': f'{player_id}_DribbleShooting.csv',
            'touch_time': f'{player_id}_TouchTimeShooting.csv',
            'overall_shooting': f'{player_id}_Overall.csv'
        }
        
        loaded_data = {'basic_stats': basic_stats, 'position': position}
        missing_files = []
        
        for key, filename in files_to_load.items():
            file_path = 'data/raw/' + filename
            if file_path:
                try:
                    loaded_data[key] = pd.read_csv(file_path)
                except Exception as e:
                    print(f"Error reading {filename} for {player_name} (ID: {player_id}): {e}")
                    loaded_data[key] = pd.DataFrame()
                    missing_files.append(filename)
            else:
                loaded_data[key] = pd.DataFrame()
                missing_files.append(filename)
        
        league_files = {
            'hustle_stats': 'league_hustle_stats.csv',
            'clutch_stats': 'league_clutch_stats.csv'
        }
        
        for key, filename in league_files.items():
            file_path = 'data/raw/' + filename
            if file_path:
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

def calculate_ast_tov_ratio(data):
    """Assist-to-Turnover Ratio"""
    try:
        basic = data['basic_stats']
        ast = basic['AST']
        tov = basic['TOV']
        return ast / tov if tov > 0 else np.inf
    except:
        return np.nan

def calculate_late_clock_efficiency(data):
    """Late Clock Efficiency"""
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

def calculate_clutch_ast_tov(data):
    """Clutch AST/TOV Ratio"""
    try:
        clutch = data['clutch_stats']
        if clutch.empty:
            return np.nan
            
        ast = clutch['AST']
        tov = clutch['TOV']
        
        if tov > 0:
            return ast / tov
        else:
            # 0 clutch turnovers indicates limited clutch playtime, just use
            # regular ratio * 0.9 if so
            basic = data['basic_stats']
            regular_ast_tov = basic['AST'] / basic['TOV'] if basic['TOV'] > 0 else 3.0
            return regular_ast_tov * 0.9
    except:
        return np.nan

def calculate_efg_pct(data):
    """Effective Field Goal %"""
    try:
        basic = data['basic_stats']
        fgm = basic['FGM']
        fg3m = basic['FG3M']
        fga = basic['FGA']
        return (fgm + 0.5 * fg3m) / fga if fga > 0 else 0
    except:
        return np.nan

def calculate_deflections_per_36(data):
    """Deflections per 36"""
    try:
        hustle = data['hustle_stats']
        if hustle.empty:
            return np.nan
        return hustle['DEFLECTIONS']
    except:
        return np.nan

def calculate_screen_assists_per_36(data):
    """Screen Assists per 36"""
    try:
        hustle = data['hustle_stats']
        if hustle.empty:
            return np.nan
        return hustle['SCREEN_ASSISTS']
    except:
        return np.nan

def calculate_shooting_foul_percentage(data):
    """Shooting Foul Rate"""
    try:
        general_splits = data['general_splits']
        closest_defender = data['closest_defender']
        basic_stats = data['basic_stats']
        
        if general_splits.empty or closest_defender.empty:
            return np.nan
            
        overall_stats = general_splits.iloc[0]
        games_played = overall_stats['GP']
        player_name = basic_stats['PLAYER_NAME']
        
        shots_defended_per_game = closest_defender['FGA'].sum()
        total_shots_defended = shots_defended_per_game * games_played

        if total_shots_defended == 0:
            return np.nan
            
        shooting_fouls = get_shooting_fouls(player_name)
        
        # divide shooting fouls by number of "contests" 
        # (opponent FGA with player as closest defender)
        shooting_foul_percentage = (shooting_fouls / total_shots_defended) * 100
        return shooting_foul_percentage
    except:
        return np.nan

def get_shooting_fouls(player_name):
    """get data from bbref csv"""
    try:
        shooting_fouls_df = pd.read_csv('data/processed/shooting_fouls_bbref_2024.csv')
        player_entries = shooting_fouls_df[shooting_fouls_df['Player'] == player_name]
        
        if not player_entries.empty:
            if len(player_entries) > 1:
                player_entries = player_entries.sort_values('G', ascending=False)
            return player_entries.iloc[0]['Shoot']
        
        return np.nan
        
    except Exception as e:
        print(f"Could not load shooting fouls for {player_name}: {e}")
        return np.nan


def calculate_personal_foul_rate(data):
    """Personal Foul Rate per 36"""
    try:
        basic = data['basic_stats']
        player_name = basic['PLAYER_NAME']
        
        # using bbref data
        basic_stats_df = pd.read_csv('data/processed/basic_stats_36_bbref.csv')
        player_row = basic_stats_df[basic_stats_df['Player'] == player_name]
        
        if player_row.empty:
            return np.nan
            
        pf_per_36 = player_row.iloc[0]['PF']
        return pf_per_36
        
    except:
        return np.nan

def calculate_age(data):
    """Age"""
    try:
        basic = data['basic_stats']
        player_name = basic['PLAYER_NAME']
        
        # data contained in bbref csv
        basic_stats_df = pd.read_csv('data/processed/basic_stats_36_bbref.csv')
        player_row = basic_stats_df[basic_stats_df['Player'] == player_name]

        if player_row.empty:
            return np.nan
        
        age = player_row.iloc[0]['Age']
        return age

    except:
        return np.nan

def calculate_assist_percentage(data):
    """Assist Percentage"""
    try:
        basic = data['basic_stats']
        player_name = basic['PLAYER_NAME']
        
        # data contained in bbref csv
        advanced_stats_df = pd.read_csv('data/processed/advanced_stats_bbref_2024.csv')
        player_row = advanced_stats_df[advanced_stats_df['Player'] == player_name]
        
        if player_row.empty:
            return np.nan

        ast_pct = player_row.iloc[0]['AST%']
        return ast_pct
        
    except:
        return np.nan

def calculate_all_metrics_for_player(player_id):
    """calculate all 10 IQ metrics for a single player"""
    data = load_player_data(player_id)
    if data is None:
        return None
    
    basic = data['basic_stats']
    player_name = basic['PLAYER_NAME']
    position = get_player_position(player_name)
    
    metrics = {
        'PLAYER_ID': int(player_id),
        'PLAYER_NAME': player_name,
        'TEAM_ID': basic['TEAM_ID'],
        'POSITION': position,
        'GP': basic['GP'],
        'MIN': basic['MIN'],

        'ast_tov_ratio': calculate_ast_tov_ratio(data),
        'late_clock_efficiency': calculate_late_clock_efficiency(data),
        'clutch_ast_tov': calculate_clutch_ast_tov(data),
        'efg_pct': calculate_efg_pct(data),
        'deflections_per_36': calculate_deflections_per_36(data),
        'screen_assists_per_36': calculate_screen_assists_per_36(data),
        'shooting_foul_pct': calculate_shooting_foul_percentage(data),
        'personal_foul_rate': calculate_personal_foul_rate(data),
        'age': calculate_age(data),
        'ast_pct': calculate_assist_percentage(data)
    }
    
    return metrics

def process_all_players():
    """process iq metrics for all 300 players"""

    # list of all players
    top300 = pd.read_csv('data/top300_per.csv')

    
    print(f"\nprocessing {len(top300)} players")
    print("note: missing data will return NaN and be replaced with 50th percentile in composite IQ calculation\n")
    
    all_metrics = []
    failed_players = []
    
    for _, player in top300.iterrows():
        player_id = str(player['PLAYER_ID'])
        player_name = player['PLAYER_NAME']
        
        print(f"processing {player_name} (ID: {player_id})...")
        
        try:
            metrics = calculate_all_metrics_for_player(player_id)
            if metrics:
                all_metrics.append(metrics)
                print(f"  successfully processed {player_name}")
            else:
                failed_players.append((player_name, player_id, "data loading failed"))
                print(f"  failed to process {player_name} - data loading failed")
        except Exception as e:
            failed_players.append((player_name, player_id, f"exception: {str(e)}"))
            print(f"  failed to process {player_name} - exception: {str(e)}")
    
    # convert to dataframe
    df = pd.DataFrame(all_metrics)
    
    # output failed players if any
    if failed_players:
        print(f"\n=== failed players: ({len(failed_players)}/{len(top300)}) ===")
        for name, player_id, reason in failed_players:
            print(f"  {name} (ID: {player_id}) - {reason}")
    else:
        print(f"\nall {len(top300)} players processed successfully!")
    
    output_file = 'data/processed/all_player_iq_metrics.csv'
    
    df.to_csv(output_file, index=False, float_format='%.3f')
    
    print(f"\nprocessed {len(df)} players")
    print(f"results saved to {output_file}")
    
    # data availability for debugging
    print("\n=== data availability ===")
    for col in df.columns:
        if col not in ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'GP', 'MIN']:
            non_null_count = df[col].notna().sum()
            print(f"{col}: {non_null_count}/{len(df)} players ({non_null_count/len(df)*100:.1f}%)")
    
    return df

if __name__ == "__main__":
    results = process_all_players()