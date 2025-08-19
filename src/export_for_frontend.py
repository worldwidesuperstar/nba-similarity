import pandas as pd
import json
import os

def export_player_data():
    """export weighted IQ rankings to JSON for frontend"""
    
    csv_path = 'data/processed/weighted_iq_rankings.csv'
    json_path = 'frontend/src/data/players.json'
    
    if not os.path.exists(csv_path):
        print(f"error: {csv_path} not found")
        return
    
    df = pd.read_csv(csv_path)
    
    frontend_data = []
    for _, row in df.iterrows():
        player_data = {
            'rank': int(row['rank_weighted_iq']),
            'name': row['PLAYER_NAME'],
            'team': int(row['TEAM_ID']),
            'position': row.get('POSITION', 'Unknown'),
            'iq_score': round(float(row['composite_weighted_iq']), 1),
            'minutes': round(float(row['MIN']), 1),
            'games': int(row['GP'])
        }
        frontend_data.append(player_data)
    
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w') as f:
        json.dump(frontend_data, f, indent=2)
    
    print(f"exported {len(frontend_data)} players to {json_path}")

if __name__ == "__main__":
    export_player_data()