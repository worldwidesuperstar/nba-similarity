nba-iq

Basketball IQ Traits with Exact Formulas

1. Decision Making

quick_decision_efficiency
= TouchTimeShooting["Touch < 2 Seconds"]["FG_PCT"] / TouchTimeShooting["Touch 6+ Seconds"]["FG_PCT"]
= 0.405 / 0.438 = 0.924

assist_turnover_ratio
= top200_per["AST"] / top200_per["TOV"]
= 7.4 / 1.6 = 4.625

assist_efficiency
= sum(PassesMade["AST"]) / sum(PassesMade["PASS"])
= (0.87 + 1.48 + 0.61 + ...) / (8.37 + 8.07 + 3.76 + ...)

clutch_decision_quality
= league_clutch_stats[player_id]["AST"] / league_clutch_stats[player_id]["TOV"]

early_vs_late_shot_efficiency
= ShotClockShooting["22-18 Very Early"]["FG_PCT"] / ShotClockShooting["7-4 Late"]["FG_PCT"]

2. Situational Awareness

deflections_per_36
= league_hustle_stats[player_id]["DEFLECTIONS"] \* 36 / league_hustle_stats[player_id]["MIN"]

loose_ball_recovery_rate
= league_hustle_stats[player_id]["LOOSE_BALLS_RECOVERED"] / league_hustle_stats[player_id]["MIN"] \* 36

screen_assist_rate
= league_hustle_stats[player_id]["SCREEN_ASSISTS"] / league_hustle_stats[player_id]["MIN"] \* 36

fourth_quarter_shot_selection
= shot_data[shot_data["PERIOD"] == 4]["SHOT_MADE_FLAG"].mean() / shot_data["SHOT_MADE_FLAG"].mean()

quick_touch_frequency
= TouchTimeShooting["Touch < 2 Seconds"]["FGA_FREQUENCY"]
= 0.271

3. Pattern Recognition

defensive_pressure_adaptation
= ClosestDefenderShooting["2-4 Feet - Tight"]["FG_PCT"] / ClosestDefenderShooting["6+ Feet - Wide
Open"]["FG_PCT"]
= 0.481 / 0.443 = 1.086

dribble_efficiency_pattern
= DribbleShooting["0 Dribbles"]["FG_PCT"] / DribbleShooting["7+ Dribbles"]["FG_PCT"]
= 0.399 / 0.435 = 0.917

teammate_optimization
= 1 / std_dev(PassesMade["FG_PCT"])
= 1 / standard_deviation([0.392, 0.446, 0.509, 0.4, 0.4, 0.377, ...])

shot_type_efficiency_variance
= 1 / std_dev(shot_data.groupby("ACTION_TYPE")["SHOT_MADE_FLAG"].mean())

4. Risk Management

late_clock_avoidance
= 1 - sum(ShotClockShooting[late_clock_ranges]["FGA_FREQUENCY"])
where late_clock_ranges = ["7-4 Late", "4-0 Very Late"]

smart_defensive_risk
= league_hustle_stats[player_id]["CHARGES_DRAWN"] / (top200_per["PF"] +
league_hustle_stats[player_id]["CHARGES_DRAWN"])

shot_risk_management
= ClosestDefenderShooting["6+ Feet - Wide Open"]["FGA_FREQUENCY"] / ClosestDefenderShooting["0-2 Feet -
Very Tight"]["FGA_FREQUENCY"]
= 0.302 / 0.002 = 151

steal_foul_ratio
= top200_per["STL"] / top200_per["PF"]
= 1.3 / 1.6 = 0.8125

clutch_turnover_avoidance
= 1 / (league_clutch_stats[player_id]["TOV"] / league_clutch_stats[player_id]["MIN"])

Chris Paul Example Values:

-   Decision Making: 0.924, 4.625, 0.14, clutch_ratio, early_late_ratio
-   Situational Awareness: deflections_rate, loose_balls_rate, screen_rate, q4_ratio, 0.271
-   Pattern Recognition: 1.086, 0.917, teammate_std, shot_type_std
-   Risk Management: late_avoidance, defensive_risk, 151, 0.8125, clutch_tov_rate
