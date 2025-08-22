## [nba-iq](https://github.com/worldwidesuperstar/nba-iq)

aim: quantify the always-vague "basketball IQ" term using NBA statistical data.

## Scope

All data is retrieved from the top 300 players by PPG according to the nba-api leaguedashplayerstats endpoint.

## Limitations/Assumptions:

-   2024-25 regular season data
-   limited to the top 300 players by PPG
-   if given the choice, data always standardized to per36

## Endpoints/Sources

nba-api

-   leaguedashplayerstats
-   playerdashboardbygeneralsplits
-   shotchartdetail
-   playerdashptshots
-   leaguehustlestatsplayer
-   leaguedashplayerclutch
-   playerdashptpass

Basketball Reference (2024-25 season data, CSVs exported from website)

-   totals
-   play-by-play
-   advanced

## Statpoint Selection

For my study, I wanted to quantify basketball IQ according to "soft skills" that are indicative of intelligence, such as decision-making, risk management, situational awareness, anticipation, and pattern recognition. Thus, the composite IQ metric I made for this study is based on statistics that reflect a player's strength in one or more of these indicators.

This metric is not representative of a player's actual, physical intellect. It focuses solely on the "smartness" of their basketball performance on the court. While there is much more that goes into a player's understanding of the game, I believe that the statistics chosen are good representations of smart play and basketball knowledge.

## Statpoints

1. **Assist-to-Turnover Ratio** - Shows decision-making and risk aversion.

2. **Clutch AST/TOV Ratio** - Shows the above skills but in high-pressure, game-deciding moments.

3. **Late Clock Efficiency** - Shows composure and smart shot selection under time pressure.

4. **Effective Field Goal %** - Indicator of good shot selection and offensive decision-making. Percentiles relative to position.

5. **Deflections per 36** - Shows anticipation and pattern recognition through reading plays.

6. **Screen Assists per 36** - Indicates ability to run plays and strong teammate awareness. Percentiles relative to position.

7. **Shooting Foul Rate** - Shows risk-averse ability to contest shots without fouling. Percentiles relative to position.

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

## Statpoint/Weight Explanation + Superlatives (minimum 30GP)

High Weight Categories (15%):

1. AST/TOV Ratio

In my opinion, I feel like a player's assist to turnover ratio is a very good indicator of their ability to make good, smart decisions on offense. Creating looks for teammates clearly shows smart decision making and court awareness, and mitigating turnovers requires good risk management and composure.

    Top 5
        -   Tyrese Haliburton
        -   Tre Jones
        -   Miles McBride
        -   Tyus Jones
        -   Jeff Dowtin Jr.

I always thought of Tyrese Haliburton as a very good facilitator but was pleasantly surprised to see that he had the best assist-turnover ratio in the entire league. Also-- Tyus Jones (fourth here) scored extremely high in a lot of the chosen metrics and ended up with the 6th highest composite IQ in the entire league, and he plays surprisingly smart for a player that gets so much negative press these days.

2. EFG% (Position-based)

EFG% is a great general tell that a player understands what shot types are most efficient for them, and also an indicator of good discipline. However, when I calculated percentiles for the first time, centers, specifically centers that took a vast majority of their shots from paint range, dominated the percentile rankings. Thus, I calculated percentiles by position instead to give a rough grouping of shot diet relative to their role on the court.

    Top 5:
        -   Vít Krejčí
        -   Aaron Nesmith
        -   Jarrett Allen
        -   Christian Braun
        -   Payton Pritchard

3. Assist Percentage

As previously explained in the AST/TOV metric section, I value passing and creation extremely highly when it comes to evaluating a player's basketball IQ. A player's assist percentage measures the percentage of teammate field goals they assist on, displaying their ability to understand the floor and their awareness of the movement of their teammates. This stat was derived from Basketball Reference.

    Top 5:
        -   Trae Young
        -   Nikola Jokić
        -   LaMelo Ball
        -   Cade Cunningham
        -   LeBron James

This list isn't necessarily surprising, but Jokić having the second highest assist percentage in the entire league as a center is simply crazy.

4. Shooting Foul Rate (Position-based)

Given that the free throw is the most efficient shot for most players in the league, it is extremely imporant to make smart contests and not to gamble on defense. You simply do not want to give your opponent free throws. To measure this, I calculated the ratio between the number of shots a player was the closest defender against (basically how many "contests") per game, and divided that by their shooting fouls per game. This statistic was heavily inspired by CraftedNBA's take on Basketball IQ, and I derived this statistic using shooting foul data from Basketball Reference and closestDefender data from nba-api.

    Top 5: (Percentiles are reversed, these are the players with the LOWEST shooting foul rate)
        - Jeff Dowtin Jr.
        - LeBron James
        - Kawhi Leonard
        - Nikola Jokić
        - Mikal Bridges

I didn't know LeBron had such good foul control-- he's ranked extremely well in personal foul rate too.

Mid Weight Categories (10%)

5. Deflections per 36

Smart players have good anticipation skills and are able to predict plays as they happen. To me, this is a bit less important as a defensive IQ metric than shooting foul rate but still very indicative of play-reading and prediction ability.

    Top 5:
        -   Dyson Daniels
        -   Herbert Jones
        -   Kelly Oubre Jr.
        -   Paul George
        -   Nikola Jokić

I'd like to shout out Matisse Thybulle, who would have been in the top 5 had he played greater than 20 games. A long time ago, I watched a Thinking Basketball video about him and I thought his defensive playstyle was super unique and refreshing.

6. Screen Assists per 36 (Position-based)

I think screen assists are a very overlooked statistic that I believe indicates a strong level of basketball IQ. Consistently getting screen assists requires a good ability to run plays and a good overall awareness of the floor. I wanted to include at least one statistic related to off-ball movement as I think off-ball play in general is where smarter players really get rewarded.

    Top 5
        -   Josh Hart
        -   Fred VanVleet
        -   Domantas Sabonis
        -   Tim Hardaway Jr.
        -   Cason Wallace

Josh Hart being at the top of this list is no surprise. As a Knicks fan, I've always appreciated his non-box contributions and overall smart, high-effort play. Also, Fred VanVleet being just behind him is really interesting, as I didn't know he had really good off-ball play.

7. Late Clock Efficiency (Position-based)

Being efficient in the late clock shows a player's ability to improvise and take efficient shots under the pressure of time. I think composure is a big part of basketball IQ and being able to make quick and smart decisions is an important ability to have. I calculated this statistic as a player's EFG% on shots taken with 8 seconds or less on the shot clock. Like raw EFG%, this metric's percentiles were calculated relative to position.

    Top 5
        -   Brandon Williams
        -   Kevin Durant
        -   Dereck Lively II
        -   Caris LeVert
        -   Tre Jones

Lower Weight Categories (1-5%):

8. Clutch AST/TOV

Supplementary to AST/TOV. Shows the same abilities but under pressure.

9. Personal Foul Rate

Supplementary to shooting foul rate, but I consider comitting a personal foul to have less negative consequence than a shooting foul.

10. Age (1 percent of final IQ)

I thought I had to incorporate age to an extent just to give some level of respect to league experience.

## Data Collection Procedure

1. ran fetch_data.py to fetch all 2024-2025 data for the top 300 in PPG. all API queries here are made to nba-api and the endpoints listed above.

2. downloaded the necessary CSV files from basketball reference (thank you!) to use for metric processing

3. ran calculate_iq_metrics.py to get all raw metrics for each player from the fetched data. stored results in all_player_iq_metrics.csv

4. ran calculate_iq_composite.py to get percentiles for each player according to the raw statistics in the CSV from step 3, and to plug these percentiles into the weighted formula for the composite IQ metric. stored IQ data for each player in weighted_iq_rankings.csv

5. used csvjson.com to convert the raw and composite data into a JSON file for the frontend

To anyone reading this, feel free to try using your own weights by editing the calculate_iq_composite.py file, where the weights are defined. With some adjustments, the fetch_data script could also potentially fetch data from previous seasons, which I may take a look at in the future as well.

## Overall Opinion on Findings

When finalizing the data collection and eventually getting the composite IQ rankings according to my formula, I was actually very satisfied with the result I got. Many of the players that made the top 25 in IQ are players that I (and also the general NBA fanbase) consider very smart. I was surprised to see Haliburton all the way at number 1, even though I knew his style of play was extremely geared towards creation and careful passing. Some players who I consider very smart on the defensive end, like Kawhi Leonard, didn't get as high a placing as I predicted. Kawhi was brought down quite a bit by his moderately high turnover rate on the other end, something I overlooked as a flaw in his game. It was generally fun looking at the top rankers for each metric too. For example, seeing that Kevin Durant was one of the most efficient players with less than 8 seconds on the shot clock made so much sense to me.

One thing I appreciate about this self-study is that it showed me many examples of players who exhibit high levels of basketball IQ but do not get very many minutes. Tyus Jones, whose usage is a decently low 16%, has the 5th highest composite IQ score in the entire league. While I am aware that a metric like this cannot possibly tell the full story about a player and their impact, I do wonder if players that exhibit high bbIQ behavior should be given more usage, since the metrics I used are indicative of efficient and smart decisions while on the floor.

I have always believed that basketball IQ is a trait that contributes to winning, but the term's lack of a clear and statistical definition made me curious as to what factors are actually indicative of it. I found this project very fulfilling as it gave me a lot of appreciation for the "little things" in basketball, and because I am a big fan of smart, "ethical" NBA play. I also found this project insightful as a way to teach myself how to use Python and Python libraries within a data analysis context. I find data analysis, especially in the context of the NBA, extremely fascinating, and I think there is a lot of valuable information yet to be learned that hides within the many random statistics the league has to offer. Numbers don't lie, as they say. To those who took the time to read until here, thank you, and I hope this project was interesting!

## Tech

    Backend
        - **python**
        - **pandas**
        - **numpy**
    Frontend
        - **react**
        - **vite**
        - **bootstrap**
        - **plotly**
        - **react-markdown**
