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