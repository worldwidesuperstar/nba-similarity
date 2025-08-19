# nba-iq

aim: quantify the always-vague "basketball IQ" term using NBA statistical data.

## Scope

all data is retrieved from the top 300 players by PPG according to the nba-api LeagueLeaders endpoint.

## Limitations/Assumptions:

-   2024-25 regular season data
-   limited to the top 300 players by PPG
-   if given the choice, data always standardized to per36

## Endpoints/Sources

nba-api

-   leagueleaders
-   playerdashboardbygeneralsplits
-   shotchartdetail
-   playerdashptshots,
-   leaguehustlestatsplayer
-   leaguedashplayerclutch
-   playerdashptpass

Basketball Reference (2024-25 season data, CSVs exported from website)

-   totals
-   play-by-play
-   advanced

## Statpoint Reasoning

For my study, I wanted to quantify basketball IQ according to "soft skills" that are indicative of intelligence. Thus, each stat was picked to best represent a player's ability in decision making, situational awareness, and risk management.

## Statpoints

1. **Assist-to-Turnover Ratio** - Shows decision-making and risk aversion.

2. **Clutch AST/TOV Ratio** - Shows the above skills but in high-pressure, game-deciding moments.

3. **Late Clock Efficiency** - Shows composure and smart shot selection under time pressure.

4. **Effective Field Goal %** - Indicator of good shot selection and offensive decision-making.

5. **Deflections per 36** - Shows anticipation and pattern recognition through reading plays.

6. **Screen Assists per 36** - Indicates ability to run plays and strong teammate awareness. Percentiles relative to position.

7. **Shooting Foul Rate** - Shows risk-averse ability to contest shots without fouling. Percentiles based on position.

8. **Personal Foul Rate** - Shows overall defensive discipline and control.

9. **Assist Percentage** - Shows a player's teammate awareness and decision-making skills through creation.

10. **Age** - Decent measure of a player's league experience and maturity. Factored in very slightly.

## Overall IQ Metric

For each IQ statpoint, players are ranked by percentile and are placed on an IQ
curve according to their average composite percentile relative to other players.

IQ curve has a baseline (average) IQ of 100, with a standard deviation of 15.

## Weighting Formula

-   **AST/TOV Ratio**: 15%
-   **Clutch AST/TOV Ratio**: 5%
-   **Effective Field Goal %**: 15%
-   **Assist Percentage**: 15%
-   **Deflections per 36**: 10%
-   **Screen Assists per 36**: 10%
-   **Late Clock Efficiency**: 9%
-   **Shooting Foul Rate**: 15%
-   **Personal Foul Rate**: 5%
-   **Age**: 1%
