# nba-iq

aim: quantify the always-vague "basketball IQ" term using NBA statistical data across four core dimensions.

## Scope

All data is retrieved from the top 200 players by PPG according to the nba-api LeagueLeaders endpoint.

Limitations/Assumptions:

2024-25 regular season data
55 games played minimum
If given the choice, data always standardized to per 36 minutes

## Statpoint Reasoning

For my study, I wanted to quantify basketball IQ according to "soft skills" that are indicative of intelligence. Thus, each stat was picked to best represent a player's ability in decision making, situational awareness, and risk management.

## Statpoints

1. **Assist-to-Turnover Ratio** - Measures decision-making quality under pressure and ability to create opportunities while minimizing mistakes.

2. **Late Clock Efficiency** - Shows composure and smart shot selection when forced to make quick decisions under time pressure.

3. **Clutch AST/TOV Ratio** - Indicates decision-making quality in high-pressure, game-deciding moments.

4. **Effective Field Goal %** - Demonstrates smart shot selection and recognition of good scoring opportunities.

5. **Deflections per 36** - Shows anticipation skills and ability to read offensive patterns before they develop.

6. **Screen Assists per 36** - Indicates understanding of how to create opportunities for teammates through intelligent positioning.

7. **Quick Decision Efficiency** - Measures basketball instincts and pattern recognition when forced to decide in under 2 seconds.

8. **Loose Balls Recovered per 36** - Shows anticipation, positioning awareness, and effort on 50/50 plays.

9. **Defensive Discipline (Shooting Foul Rate)** - Shows ability to contest shots without fouling.

10. **Successful Box Outs per 36** - Demonstrates positioning intelligence and effectiveness in creating rebounding opportunities.

11. **Charges Drawn per 36** - Shows willingness to take calculated risks for defensive advantage.

12. **Road Performance Maintenance** - Measures ability to maintain performance levels in challenging away environments.

13. **Personalized Shot Selection Intelligence** - Evaluates whether a player takes the best shots for their specific skillset rather than league-average optimal shots.

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

## Overall IQ Metric
