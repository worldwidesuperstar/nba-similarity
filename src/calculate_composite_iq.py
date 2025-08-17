import pandas as pd
import numpy as np
import os

def calculate_percentiles_and_composite_iq():
    """
    Calculate percentiles for each IQ metric and composite IQ scores for all players.
    
    Creates two CSV files:
    1. player_iq_percentiles.csv - Detailed percentiles for each metric
    2. composite_iq_rankings.csv - Overall IQ rankings and scores
    """
    
    # Load the existing IQ metrics data
    print("Loading IQ metrics data...")
    iq_metrics = pd.read_csv('data/processed/all_player_iq_metrics.csv')
    
    # Define the 12 IQ metric columns
    metric_columns = [
        'ast_tov_ratio', 'late_clock_efficiency', 'clutch_ast_tov', 'efg_pct',
        'deflections_per_36', 'screen_assists_per_36', 'quick_decision_efficiency',
        'loose_balls_per_36', 'shooting_foul_pct', 'successful_boxouts_per_36'
        # 'shot_selection_value'
    ]
    
    print(f"Calculating percentiles for {len(iq_metrics)} players across {len(metric_columns)} metrics...")
    
    # Create dataframe for detailed percentiles
    base_columns = ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'GP', 'MIN']
    if 'POSITION' in iq_metrics.columns:
        base_columns.insert(3, 'POSITION')
    percentiles_df = iq_metrics[base_columns].copy()
    
    # Calculate percentiles for each metric
    for metric in metric_columns:
        if metric in ['screen_assists_per_36', 'successful_boxouts_per_36'] and 'POSITION' in iq_metrics.columns:
            # Position-based percentiles for screen assists and boxouts
            percentiles = []
            for idx, row in iq_metrics.iterrows():
                value = row[metric]
                position = row.get('POSITION', 'Unknown')
                
                if position == 'Unknown' or pd.isna(position):
                    # Fall back to league-wide percentiles if position is unknown
                    metric_values = iq_metrics[metric]
                    finite_values = metric_values[np.isfinite(metric_values)]
                    if np.isfinite(value):
                        percentile = (finite_values < value).mean() * 100
                    else:
                        percentile = np.nan
                else:
                    # Get values for players in the same position
                    same_position_values = iq_metrics[iq_metrics['POSITION'] == position][metric]
                    finite_position_values = same_position_values[np.isfinite(same_position_values)]
                    
                    if np.isfinite(value) and len(finite_position_values) > 1:
                        percentile = (finite_position_values < value).mean() * 100
                    else:
                        percentile = np.nan
                percentiles.append(percentile)
        else:
            # League-wide percentiles for all other metrics
            metric_values = iq_metrics[metric]
            finite_values = metric_values[np.isfinite(metric_values)]
            
            if metric == 'shooting_foul_pct':
                # For shooting fouls, lower is better, so we flip the percentile
                percentiles = []
                for value in metric_values:
                    if np.isfinite(value):
                        percentile = (finite_values > value).mean() * 100
                    else:
                        percentile = np.nan
                    percentiles.append(percentile)
            else:
                # For all other metrics, higher is better
                percentiles = []
                for value in metric_values:
                    if np.isfinite(value):
                        percentile = (finite_values < value).mean() * 100
                    else:
                        percentile = np.nan
                    percentiles.append(percentile)
        
        # Add percentile column
        percentiles_df[f'{metric}_percentile'] = percentiles
    
    # Calculate weighted composite IQ score
    print("Calculating weighted composite IQ scores...")
    
    # Define weights for each metric (emphasizing decision making and defensive awareness)
    weights = {
        # CORE DECISION MAKING (40% total)
        'ast_tov_ratio': 0.15,              # Most important - core IQ metric
        'clutch_ast_tov': 0.15,             # Clutch decision making under pressure
        'quick_decision_efficiency': 0.10,   # Quick processing/reactions
        
        # DEFENSIVE AWARENESS (25% total)  
        'deflections_per_36': 0.10,         # Anticipation and positioning
        'successful_boxouts_per_36': 0.05,  # Situational awareness (position-based)
        'shooting_foul_pct': 0.10,          # Smart fouling (lower is better)
        
        # OFFENSIVE EFFICIENCY (25% total)
        'efg_pct': 0.15,                    # Shot selection intelligence
        'late_clock_efficiency': 0.10,      # Pressure situation execution
        # 'shot_selection_value': 0.10,       # Overall shot IQ
        
        # HUSTLE/EFFORT (10% total)
        'screen_assists_per_36': 0.05,      # Team play awareness (position-based)
        'loose_balls_per_36': 0.05          # Effort/anticipation
    }
    
    # Calculate weighted score for each player
    weighted_scores = []
    for _, row in percentiles_df.iterrows():
        weighted_score = 0
        for metric, weight in weights.items():
            percentile_col = f"{metric}_percentile"
            if percentile_col in percentiles_df.columns and pd.notna(row[percentile_col]):
                weighted_score += row[percentile_col] * weight
        weighted_scores.append(weighted_score)
    
    percentiles_df['composite_iq_percentile'] = weighted_scores
    
    # Rank players by composite IQ (higher percentile = better rank)
    percentiles_df['iq_rank'] = percentiles_df['composite_iq_percentile'].rank(ascending=False, method='min')
    
    # Create processed data directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)
    
    # Save detailed percentiles
    percentiles_file = 'data/processed/player_iq_percentiles.csv'
    percentiles_df.to_csv(percentiles_file, index=False)
    print(f"Detailed percentiles saved to {percentiles_file}")
    
    # Create composite IQ rankings CSV
    composite_columns = ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'GP', 'MIN', 'composite_iq_percentile', 'iq_rank']
    if 'POSITION' in percentiles_df.columns:
        composite_columns.insert(3, 'POSITION')
    composite_df = percentiles_df[composite_columns].copy()
    
    # Round composite IQ percentile for readability
    composite_df['composite_iq_percentile'] = composite_df['composite_iq_percentile'].round(1)
    composite_df['iq_rank'] = composite_df['iq_rank'].astype(int)
    
    # Sort by rank
    composite_df = composite_df.sort_values('iq_rank')
    
    # Save composite rankings
    composite_file = 'data/processed/composite_iq_rankings.csv'
    composite_df.to_csv(composite_file, index=False)
    print(f"Composite IQ rankings saved to {composite_file}")
    
    # Print summary statistics
    print(f"\n=== COMPOSITE IQ SUMMARY ===")
    print(f"Players analyzed: {len(composite_df)}")
    print(f"Average composite IQ percentile: {composite_df['composite_iq_percentile'].mean():.1f}")
    print(f"Median composite IQ percentile: {composite_df['composite_iq_percentile'].median():.1f}")
    
    # Show top 15 highest IQ players with weighted formula
    print(f"\n=== TOP 15 WEIGHTED BASKETBALL IQ PLAYERS ===")
    print("Formula: 40% Decision Making, 25% Defensive Awareness, 25% Offensive Efficiency, 10% Hustle")
    top_15 = composite_df.head(15)
    for _, player in top_15.iterrows():
        if 'POSITION' in player:
            print(f"{player['iq_rank']:2d}. {player['PLAYER_NAME']:<25} ({player['POSITION']:<15}, {player['TEAM_ID']}) - {player['composite_iq_percentile']:.1f}%")
        else:
            print(f"{player['iq_rank']:2d}. {player['PLAYER_NAME']:<25} ({player['TEAM_ID']}) - {player['composite_iq_percentile']:.1f}%")
    
    return percentiles_df, composite_df

if __name__ == "__main__":
    percentiles_df, composite_df = calculate_percentiles_and_composite_iq()