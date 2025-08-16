#!/usr/bin/env python3

import pandas as pd
import requests
import os

def get_shooting_fouls_data():
    """
    Extract shooting fouls data from Basketball Reference Play-by-Play stats page.
    """
    
    print("=== EXTRACTING SHOOTING FOULS DATA ===")
    
    url = "https://www.basketball-reference.com/leagues/NBA_2025_play-by-play.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Use pandas to read HTML tables directly
        tables = pd.read_html(response.text)
        
        # Find the main play-by-play table (should be the largest one)
        main_table = max(tables, key=len)
        
        print(f"Main table shape: {main_table.shape}")
        print(f"Columns: {list(main_table.columns)}")
        
        # Fix column names for multi-level headers
        new_columns = []
        for col in main_table.columns:
            if isinstance(col, tuple):
                # Join multi-level column names
                if col[1] in ['Shoot', 'Off.']:
                    # For foul columns, include both levels
                    new_columns.append(f"{col[0]}_{col[1]}")
                elif col[0] == 'Unnamed: 1_level_0':
                    new_columns.append('Player')
                elif col[0] == 'Unnamed: 3_level_0':
                    new_columns.append('Team')
                else:
                    new_columns.append(col[1] if col[1] != col[0] else col[0])
            else:
                new_columns.append(str(col))
        
        main_table.columns = new_columns
        
        print(f"Fixed columns: {list(main_table.columns)}")
        
        # Extract key columns we need
        key_columns = ['Player', 'Team', 'G', 'MP']
        
        # Find shooting fouls columns
        shooting_foul_cols = [col for col in main_table.columns if 'Fouls Committed_Shoot' in col or 'Shoot' in col]
        print(f"Shooting foul columns found: {shooting_foul_cols}")
        
        # Extract relevant data
        if 'Fouls Committed_Shoot' in main_table.columns:
            shooting_fouls_col = 'Fouls Committed_Shoot'
        else:
            # Find the shooting fouls column
            for col in main_table.columns:
                if 'Shoot' in str(col) and 'Committed' in str(col):
                    shooting_fouls_col = col
                    break
            else:
                print("Could not find shooting fouls committed column")
                return None
        
        print(f"Using shooting fouls column: {shooting_fouls_col}")
        
        # Select relevant columns
        final_columns = key_columns + [shooting_fouls_col]
        available_columns = [col for col in final_columns if col in main_table.columns]
        
        shooting_fouls_df = main_table[available_columns].copy()
        
        # Clean the data
        shooting_fouls_df = shooting_fouls_df.dropna(subset=['Player'])
        shooting_fouls_df = shooting_fouls_df[shooting_fouls_df['Player'] != 'Player']  # Remove header rows
        
        # Convert shooting fouls to numeric
        shooting_fouls_df[shooting_fouls_col] = pd.to_numeric(shooting_fouls_df[shooting_fouls_col], errors='coerce')
        
        # Convert minutes to numeric and calculate per-36 rate
        if 'MP' in shooting_fouls_df.columns:
            shooting_fouls_df['MP'] = pd.to_numeric(shooting_fouls_df['MP'], errors='coerce')
            shooting_fouls_df['shooting_fouls_per_36'] = (
                shooting_fouls_df[shooting_fouls_col] / shooting_fouls_df['MP'] * 36
            ).round(3)
        
        # Save the data
        os.makedirs('../data/processed', exist_ok=True)
        output_file = '../data/processed/shooting_fouls_bbref_2024.csv'
        shooting_fouls_df.to_csv(output_file, index=False)
        
        print(f"\n=== RESULTS ===")
        print(f"Extracted shooting fouls data for {len(shooting_fouls_df)} players")
        print(f"Data saved to: {output_file}")
        
        # Show summary statistics
        print(f"\nShooting fouls summary:")
        print(f"Average shooting fouls per player: {shooting_fouls_df[shooting_fouls_col].mean():.1f}")
        print(f"Median shooting fouls per player: {shooting_fouls_df[shooting_fouls_col].median():.1f}")
        
        if 'shooting_fouls_per_36' in shooting_fouls_df.columns:
            print(f"Average shooting fouls per 36 min: {shooting_fouls_df['shooting_fouls_per_36'].mean():.2f}")
        
        # Show top 10 most disciplined defenders (fewest shooting fouls)
        print(f"\n=== MOST DISCIPLINED DEFENDERS (Fewest Shooting Fouls) ===")
        top_disciplined = shooting_fouls_df.nsmallest(10, shooting_fouls_col)
        for _, player in top_disciplined.iterrows():
            print(f"{player['Player']} ({player.get('Team', 'N/A')}): {player[shooting_fouls_col]} shooting fouls")
        
        # Show top 10 most shooting fouls
        print(f"\n=== MOST SHOOTING FOULS COMMITTED ===")
        most_fouls = shooting_fouls_df.nlargest(10, shooting_fouls_col)
        for _, player in most_fouls.iterrows():
            print(f"{player['Player']} ({player.get('Team', 'N/A')}): {player[shooting_fouls_col]} shooting fouls")
        
        return shooting_fouls_df
        
    except Exception as e:
        print(f"Error extracting shooting fouls data: {e}")
        return None

if __name__ == "__main__":
    shooting_fouls_data = get_shooting_fouls_data()