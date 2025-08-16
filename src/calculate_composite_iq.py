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
    iq_metrics = pd.read_csv('../data/processed/all_player_iq_metrics.csv')
    
    # Define the 12 IQ metric columns
    metric_columns = [
        'ast_tov_ratio', 'late_clock_efficiency', 'clutch_ast_tov', 'efg_pct',
        'deflections_per_36', 'screen_assists_per_36', 'quick_decision_efficiency',
        'loose_balls_per_36', 'shooting_foul_pct', 'successful_boxouts_per_36',
        'charges_drawn_per_36', 'shot_selection_value'
    ]
    
    print(f"Calculating percentiles for {len(iq_metrics)} players across {len(metric_columns)} metrics...")
    
    # Create dataframe for detailed percentiles
    percentiles_df = iq_metrics[['PLAYER_ID', 'PLAYER_NAME', 'TEAM', 'GP', 'MIN']].copy()
    
    # Calculate percentiles for each metric
    for metric in metric_columns:
        metric_values = iq_metrics[metric]
        
        # Handle infinite values by filtering them out for percentile calculation
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
    
    # Calculate composite IQ score (average of all percentiles)
    print("Calculating composite IQ scores...")
    percentile_cols = [col for col in percentiles_df.columns if col.endswith('_percentile')]
    
    # Calculate mean percentile for each player (ignoring NaN values)
    percentiles_df['composite_iq_percentile'] = percentiles_df[percentile_cols].mean(axis=1)
    
    # Rank players by composite IQ (higher percentile = better rank)
    percentiles_df['iq_rank'] = percentiles_df['composite_iq_percentile'].rank(ascending=False, method='min')
    
    # Create processed data directory if it doesn't exist
    os.makedirs('../data/processed', exist_ok=True)
    
    # Save detailed percentiles
    percentiles_file = '../data/processed/player_iq_percentiles.csv'
    percentiles_df.to_csv(percentiles_file, index=False)
    print(f"Detailed percentiles saved to {percentiles_file}")
    
    # Create composite IQ rankings CSV
    composite_df = percentiles_df[['PLAYER_ID', 'PLAYER_NAME', 'TEAM', 'GP', 'MIN', 
                                   'composite_iq_percentile', 'iq_rank']].copy()
    
    # Round composite IQ percentile for readability
    composite_df['composite_iq_percentile'] = composite_df['composite_iq_percentile'].round(1)
    composite_df['iq_rank'] = composite_df['iq_rank'].astype(int)
    
    # Sort by rank
    composite_df = composite_df.sort_values('iq_rank')
    
    # Save composite rankings
    composite_file = '../data/processed/composite_iq_rankings.csv'
    composite_df.to_csv(composite_file, index=False)
    print(f"Composite IQ rankings saved to {composite_file}")
    
    # Print summary statistics
    print(f"\n=== COMPOSITE IQ SUMMARY ===")
    print(f"Players analyzed: {len(composite_df)}")
    print(f"Average composite IQ percentile: {composite_df['composite_iq_percentile'].mean():.1f}")
    print(f"Median composite IQ percentile: {composite_df['composite_iq_percentile'].median():.1f}")
    
    # Show top 10 highest IQ players
    print(f"\n=== TOP 10 BASKETBALL IQ PLAYERS ===")
    top_10 = composite_df.head(10)
    for _, player in top_10.iterrows():
        print(f"{player['iq_rank']:2d}. {player['PLAYER_NAME']} ({player['TEAM']}) - {player['composite_iq_percentile']:.1f}%")
    
    return percentiles_df, composite_df

if __name__ == "__main__":
    percentiles_df, composite_df = calculate_percentiles_and_composite_iq()