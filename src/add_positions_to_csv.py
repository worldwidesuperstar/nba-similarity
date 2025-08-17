#!/usr/bin/env python3

import pandas as pd
import numpy as np
from nba_api.stats.endpoints import commonplayerinfo
import time

def get_player_position(player_id):
    """Get player position from NBA API."""
    try:
        time.sleep(2)
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        player_data = player_info.get_data_frames()[0].iloc[0]
        return player_data['POSITION']
    except Exception as e:
        print(f"Could not get position for player {player_id}: {e}")
        return 'Unknown'

def add_positions_to_csv():
    """Add POSITION column to existing all_player_iq_metrics.csv file."""
    
    print("Loading existing IQ metrics data...")
    df = pd.read_csv('data/processed/all_player_iq_metrics.csv')
    
    print(f"Found {len(df)} players in the dataset")
    
    # Check if POSITION column already exists
    if 'POSITION' in df.columns:
        print("POSITION column already exists. Checking for missing positions...")
        missing_positions = df[df['POSITION'].isna() | (df['POSITION'] == 'Unknown')]
        if missing_positions.empty:
            print("All players already have position data!")
            return df
        else:
            print(f"Found {len(missing_positions)} players with missing position data")
            players_to_update = missing_positions
    else:
        print("POSITION column does not exist. Adding positions for all players...")
        # Add empty POSITION column
        df['POSITION'] = 'Unknown'
        players_to_update = df
    
    failed_players = []
    
    # Process each player to get their position
    for idx, player in players_to_update.iterrows():
        player_id = player['PLAYER_ID']
        player_name = player['PLAYER_NAME']
        
        print(f"Getting position for {player_name} (ID: {player_id})...")
        
        try:
            position = get_player_position(player_id)
            df.loc[idx, 'POSITION'] = position
            print(f"  {player_name}: {position}")
        except Exception as e:
            print(f"  Failed to get position for {player_name}: {e}")
            failed_players.append((player_name, player_id))
            df.loc[idx, 'POSITION'] = 'Unknown'
    
    # Reorder columns to put POSITION after TEAM
    columns = df.columns.tolist()
    if 'POSITION' in columns:
        columns.remove('POSITION')
        # Find the index of TEAM and insert POSITION after it
        team_idx = columns.index('TEAM')
        columns.insert(team_idx + 1, 'POSITION')
        df = df[columns]
    
    # Save updated CSV
    print(f"\nSaving updated dataset...")
    df.to_csv('data/processed/all_player_iq_metrics.csv', index=False)
    
    # Report results
    position_counts = df['POSITION'].value_counts()
    print(f"\n=== POSITION DATA SUMMARY ===")
    print(f"Total players: {len(df)}")
    print("\nPosition breakdown:")
    for position, count in position_counts.items():
        print(f"  {position}: {count}")
    
    if failed_players:
        print(f"\n=== FAILED TO GET POSITIONS ({len(failed_players)}) ===")
        for name, player_id in failed_players:
            print(f"  {name} (ID: {player_id})")
    
    print(f"\nUpdated dataset saved to data/processed/all_player_iq_metrics.csv")
    return df

if __name__ == "__main__":
    updated_df = add_positions_to_csv()