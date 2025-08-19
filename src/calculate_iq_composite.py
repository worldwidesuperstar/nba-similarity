import pandas as pd
import numpy as np

def calculate_weighted_iq_rankings():
    iq_metrics = pd.read_csv('data/processed/all_player_iq_metrics.csv')
    
    metric_columns = [
        'ast_tov_ratio', 'late_clock_efficiency', 'clutch_ast_tov', 'efg_pct',
        'deflections_per_36', 'screen_assists_per_36',
        'shooting_foul_pct', 'personal_foul_rate', 'age', 'ast_pct'
    ]
    
    base_columns = ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'POSITION', 'GP', 'MIN']
    df = iq_metrics[base_columns].copy()
    
    for metric in metric_columns:
        if metric in ['screen_assists_per_36', 'shooting_foul_pct']:
            # screen assists and shooting fouls would differ a lot by position
            percentiles = []
            for idx, row in iq_metrics.iterrows():
                value = row[metric]
                position = row.get('POSITION', 'Unknown')
                
                same_position_values = iq_metrics[iq_metrics['POSITION'] == position][metric]
                finite_position_values = same_position_values[np.isfinite(same_position_values)]
                
                if np.isfinite(value) and len(finite_position_values) > 1:
                    if metric in ['shooting_foul_pct', 'personal_foul_rate']:
                        percentile = (finite_position_values > value).mean() * 100
                    else:
                        percentile = (finite_position_values < value).mean() * 100
                else:
                    percentile = np.nan

                percentiles.append(percentile)
        else:
            metric_values = iq_metrics[metric]
            finite_values = metric_values[np.isfinite(metric_values)]
            
            percentiles = []
            for value in metric_values:
                if np.isfinite(value):
                    # invert for personal foul rate
                    if metric in ['personal_foul_rate']:
                        percentile = (finite_values > value).mean() * 100
                    else:
                        percentile = (finite_values < value).mean() * 100
                else:
                    percentile = np.nan
                percentiles.append(percentile)
        
        df[f'{metric}_percentile'] = np.round(percentiles, 1)
        df[f'{metric}_percentile'] = df[f'{metric}_percentile'].fillna(50.0)
    
    weights = {
        # creation, decision making on offense
        'ast_tov_ratio_percentile': 0.15,
        'clutch_ast_tov_percentile': 0.05,
        'ast_pct_percentile': 0.15,

        # defensive discipline and anticipation
        'shooting_foul_pct_percentile': 0.15,
        'personal_foul_rate_percentile': 0.05,
        'deflections_per_36_percentile': 0.10,

        # floor awareness and ability to run plays properly
        'screen_assists_per_36_percentile': 0.10,

        # efficiency under time pressure, composure late in clock
        'late_clock_efficiency_percentile': 0.09,

        # smart and efficient shot-taking
        'efg_pct_percentile': 0.15,

        # experience in the league
        'age_percentile': 0.01
    }
    
    print("\nWeighted Basketball IQ Formula:")
    print(f"  AST/TOV Ratio: {weights['ast_tov_ratio_percentile']:.0%}")
    print(f"  Clutch AST/TOV Ratio: {weights['clutch_ast_tov_percentile']:.0%}")
    print(f"  Assist Percentage: {weights['ast_pct_percentile']:.0%}")
    print(f"  Deflection Rate: {weights['deflections_per_36_percentile']:.0%}")
    print(f"  Screen Assist Rate: {weights['screen_assists_per_36_percentile']:.0%}")
    print(f"  Late Clock Efficiency: {weights['late_clock_efficiency_percentile']:.0%}")
    print(f"  EFG%: {weights['efg_pct_percentile']:.0%}")
    print(f"  Shooting Foul Rate: {weights['shooting_foul_pct_percentile']:.0%}")
    print(f"  Personal Foul Rate: {weights['personal_foul_rate_percentile']:.0%}")
    print(f"  Age: {weights['age_percentile']:.0%}")
    print(f"  Total: {sum(weights.values()):.0%}")
    
    unscaled_iq = 0
    for metric, weight in weights.items():
        unscaled_iq += df[metric] * weight
    
    league_average = unscaled_iq.mean()
    league_std = unscaled_iq.std()
    df['composite_weighted_iq'] = ((unscaled_iq - league_average) / league_std) * 15 + 100
    df['rank_weighted_iq'] = df['composite_weighted_iq'].rank(ascending=False, method='min').astype(int)
    df['composite_weighted_iq'] = np.round(df['composite_weighted_iq'], 0)
    
    df = df.sort_values('rank_weighted_iq')
    df.to_csv('data/processed/weighted_iq_rankings.csv', index=False)
    
    top_50 = df.head(50)[['rank_weighted_iq', 'PLAYER_NAME', 'composite_weighted_iq']]
    top_50.index = top_50['rank_weighted_iq']
    print("\n")
    print(top_50[['PLAYER_NAME', 'composite_weighted_iq']].to_string(header=False))

if __name__ == "__main__":
    calculate_weighted_iq_rankings()
