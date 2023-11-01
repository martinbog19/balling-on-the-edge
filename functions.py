import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import calendar
import time
months = [month.lower() for month in calendar.month_name[1:]]


# This function scrapes the NBA schedule and outputs a dataframe of the calendar for an input year
def Schedule(year) :

    # Scrape every team's information -- number of regular season games & team ID
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    soup.find('tr', class_ = 'over_header').decompose()
    table = soup.find('table')
    teams_dict = pd.read_html(str(table))[0][['Team', 'W', 'L']]
    teams_dict['code'] = [x['href'].split('/')[2] for x in table.find_all('a', href = True)]
    ngames_dict = dict(zip(teams_dict['code'], teams_dict['W'] + teams_dict['L']))
    teams_dict  = dict(zip(teams_dict['Team'], teams_dict['code']))

    # Scrape the year's schedule page
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_games.html'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    # Make a list of each month page urls
    monthly_url = [x['href'] for x in soup.find_all('a', href = True) if x['href'].split('.html')[0].split('-')[-1] in months]
    while soup.find('tr', class_ = 'thead') is not None:
        soup.find('tr', class_ = 'thead') .decompose()

    # Concatenate all monthly schedules
    games = pd.read_html(str(soup.find('table')))[0]
    for m_url in monthly_url[1:]:

        url = 'https://www.basketball-reference.com/' + m_url
        soup = BeautifulSoup(requests.get(url).content, 'lxml')
        m_games = pd.read_html(str(soup.find('table')))[0]
        games = pd.concat([games, m_games])
        time.sleep(3)

    # Data cleaning
    games = games.rename(columns = {'Start (ET)':'Time', 'Visitor/Neutral':'Away', 'Home/Neutral':'Home', 'PTS':'PTS_away', 'PTS.1':'PTS_home'})
    games = games[games['PTS_home'] != 'Playoffs']
    if 'Time' in games.columns :
        games['Date'] = games['Date'] + games['Time'].apply(lambda x: ' ' + x[:-1] + x[-1].upper() + 'M')
    games['Date'] = pd.to_datetime(games['Date'])
    games = games[['Date', 'Home', 'Away', 'PTS_home', 'PTS_away']] # Keep necessary columns
    games = games.sort_values('Date').reset_index(drop = True)
    games['Home'] = games['Home'].apply(lambda x: teams_dict.get(x))
    games['Away'] = games['Away'].apply(lambda x: teams_dict.get(x))
    games = games[games.index <= sum(ngames_dict.values()) / 2 - 1] # Only keep regular season games

    return games




def PlayerStats(year) :

    def single_team(df) :
        # For an input player, this function returns only a row with total stats and the latest team of the player
        if len(df) > 1:
            row = df[df['Tm'] == 'TOT']
            row['Tm'] = df['Tm'].values[-1]
            return row
        else :
            return df

    # Scrape per game stats -- PTS, TRB, AST, ...
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table')
    while table.find(class_ = 'thead') is not None :
        table.find(class_ = 'thead').decompose()
    data_pg = pd.read_html(str(table))[0].drop(columns = ['Rk'])
    data_pg.insert(1, 'href', [str(x).split('.html')[0].split('/')[-1] for x in table.find_all('a', href = True) if 'players' in str(x)])
    data_pg = data_pg.groupby('href').apply(single_team).reset_index(drop = True)
    data_pg['Player'] = data_pg['Player'].str.replace('*', '', regex = False)

    # Scrape advanced stats -- PER, BPM, WS, VORP, ...
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table')
    while table.find(class_ = 'thead') is not None :
        table.find(class_ = 'thead').decompose()
    data_adv = pd.read_html(str(table))[0]
    data_adv = data_adv.drop(columns = ['Rk'] + [x for x in data_adv.columns if 'Unnamed' in x])
    data_adv.insert(1, 'href', [str(x).split('.html')[0].split('/')[-1] for x in table.find_all('a', href = True) if 'players' in str(x)])
    data_adv = data_adv.groupby('href').apply(single_team).reset_index(drop = True)
    data_adv['Player'] = data_adv['Player'].str.replace('*', '', regex = False)

    # Merge per game and advanced stats together
    data = data_pg.merge(data_adv, on = ['Player', 'href'], suffixes = ('', '_y'))
    data = data.drop(columns = [col for col in data.columns if '_y' in col]).reset_index(drop = True) # Delete duplicated columns
    data.insert(2, 'Year', len(data) * [year])

    if len(data) != len(data_pg) or len(data) != len(data_adv):
        Warning('Merge between per game and advanced stats is not 1:1 !!')

    return data




# This function creates a dictionary for any input year, where the key is the name of the team and the item is a list of players on the opening day roster
def OpeningDayRoster(year) :

    # Explore the page with all teams and links to rosters
    url = f'https://basketball.realgm.com/nba/teams/{year}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    # Make a list of all teams alongside their unique identifier
    teams = [(x['href'].split('/')[4], x['href'].split('/')[3]) for x in soup.find_all('a', href = True) if '/teams/' in str(x) and 'Rosters' in str(x) and str(year) in str(x)]
    
    # Loop along each team
    dict = {}
    for i, tm in teams :
        # Scrape the opening day roster table of the looped team and assign the list of players to the dictionary
        url = f'https://basketball.realgm.com/nba/teams/{tm}/{i}/Rosters/Opening_Day/{year}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        table = [x for x in soup.find_all('table') if x.get('class') == ['tablesaw']][0]
        dict[' '.join(tm.split('-'))] = pd.read_html(str(table))[0]['Player'].to_list()

    return dict