#### final_data.csv COLUMNS ###

# IDENTIFIER #
        Tm        :  NBA team
        Year      :  Season (Year-1)/(Year)

# FEATURES #
A. ROSTER STRENGTH
        PTS_k     :  Weighted mean of PTS per game of roster, lagged by k years
        VORP_k    :  Weighted mean of VORP (advanced metric) per game of roster, lagged by k years
        PER_k     :  Weighted mean of PER (advanced metric) per game of roster, lagged by k years
        WS_k      :  Weighted mean of win shares per game of roster, lagged by k years
B. HISTORICAL PERFORMANCE
        WinLoss_k :  Win-Loss % of the team, lagged by k years
        NRtg_k    :  Net rating (PTS scored - PTS against) of the team, lagged by k years   
        SRS_k     :  Team rating of the team, lagged by k years
C. SCHEDULE DIFFICULTY
        Rest      :  Average number of rest days of the team
        B2B       :  Number of back-to-back games
        distLB    :  Distance traveled (lower bound - from city to city)
        distUB    :  Distance traveled (upper bound - go back home after each game)

# TARGET #        
        WinLoss   :  Win-Loss % of Tm in Year

#### final_data.csv COLUMNS ###