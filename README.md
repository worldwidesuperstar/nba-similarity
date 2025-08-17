# nba-iq

aim: quantify the always-vague "basketball IQ" term using NBA statistical data across four core dimensions.

## Scope

All data is retrieved from the top 300 players by PPG according to the nba-api LeagueLeaders endpoint.

## Limitations/Assumptions:

-   2024-25 regular season data
-   55 games played minimum
-   If given the choice, data always standardized to per 36 minutes

## Endpoints

nba-api was used for all data collection/exploration. Endpoints used include:

-   leagueleaders
-   playerdashboardbygeneralsplits
-   shotchartdetail
-   playerdashptshots,
-   leaguehustlestatsplayer
-   leaguedashplayerclutch
-   playerdashptpass
-   assisttracker

## Statpoint Reasoning

For my study, I wanted to quantify basketball IQ according to "soft skills" that are indicative of intelligence. Thus, each stat was picked to best represent a player's ability in decision making, situational awareness, and risk management.

## Statpoints

1. **Assist-to-Turnover Ratio** - Shows decision-making and risk aversion.

2. **Late Clock Efficiency** - Shows composure and smart shot selection under time pressure.

3. **Clutch AST/TOV Ratio** - Indicates decision-making in high-pressure, game-deciding moments.

4. **Effective Field Goal %** - Demonstrates ability to recognize and consistently capitalize on scoring opportunities.

5. **Deflections per 36** - Shows anticipation and ability to read plays before they happen.

6. **Screen Assists per 36** - Indicates ability to run plays and strong teammate awareness. Percentiles based on position.

Percentiles based on position.

7. **Quick Decision Efficiency** - Evaluates efficiency on shots taken very briefly after reciving the ball, indicating quick decision-making.

8. **Loose Balls Recovered per 36** - Shows anticipation, positioning awareness, and effort on 50/50 plays.

9. **Shooting Foul Rate** - Shows ability to contest shots without fouling.

~~10. **Box Out Success Rate** - Shows smart positioning and situational awareness. Percentiles based on position.~~

Percentiles based on position.

~~11. **Charges Drawn per 36** - Shows ability to read plays and have good positioning.~~

Deprecated due to poor data distribution.

12. **Smart Shot Selection** - Shows a player's understanding of what shots they are best/most efficient at.

## Overall IQ Metric

For each IQ statpoint, players are ranked by percentile and are placed on an IQ
curve according to their average composite percentile relative to other players.

Plan: average IQ around 100, standard deviation of 15.
