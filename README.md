# balling-on-the-edge
Analytics Edge Project: Clara, Lucas, Martin &amp; Val


I Scope
Every season, the NBA tip-off night comes with thrilling excitement among basketball fans all over
the world. This project does not want to have to wait for the playoffs and thinks the regular season
standings can be inferred from a blend of historical factors. By predicting the standings, it will
explore the driving factors of a successful season and uncover the underlying dynamics that decide
which NBA team has what is takes to win it all.



II Datasets
The data will be scraped from public websites Basketball Reference and RealGM. It contains data
relating to all NBA seasons in history alongside advanced player and team metrics.

1. Past team performance : this set of features are used to quantify past performance of teams
weighted towards more recent years. It considers the number of wins in previous seasons,
performance metrics – points scored (ORtg), points against (DRtg), net rating (NRtg) – and
team stats – number of assists (AST), number of rebounds (TRB) and so on.

2. Roster strengths : Second, the relative strength of the team is evaluated from the historical performance of the players on their roster. This features will be weighted by projected
minutes played to give more relative importance to players with larger roles. It considers basic player stats such as points per game (PTS), AST (or even more advanced metrics like PER
and VORP). Another proxy for roster strength can be extracted from the video game series
NBA 2K player ratings. Moreover, injuries are prevalent factors to a team’s performance during the season. The features will also incorporate how much a team’s players have historically
been injured.

3. Schedule and opponent strength : Finally, the NBA calendar is busy as each team plays
82 games in less than six months all over the US. Fitness and rest are thus major factors in
success. The model will thus incorporate the number of days between games, the distance
traveled during the season, the number of back-to-back games. It will also consider the relative
strengths of a team’s division and conference.




III Analytical techniques

The first stage of the project includes data scraping, cleaning, and pre-processing. The aim is to
assemble an analysis dataset by creating the desired metrics from the relevant scraped public data.
Each team from every previous season will serve as an observation and be described by features which
would have been recorded at the start of the season. Every observation will be linked to a target
that is the number of wins.
The project will consider models ranging from linear regression, CART, ensemble methods (Random Forests and Boosted Trees). The out-of-sample performance will most likely be evaluated on
the mean squared error. Feature selection will be heuristically performed based on relevance, multicolinearity and insights from the exploration of the underlying trends in the data. Finally, the
hyperparameters of our predictive models will be fine-tuned against the validation set to optimize
the model’s performance.
Regarding model validation, the considered baseline models are: 
(1) a model that simply predicts
a team’s number of wins in the previous season, 
(2) a model that predicts 50% wins, and, if available,
(3) a more elaborate model based on betting odds.
