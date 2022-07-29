#!/usr/bin/env python
# coding: utf-8

# In[144]:


import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from lxml import etree
from lxml import html
from datetime import datetime
import seaborn as sns
import nflfastpy
pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.max_columns', None)


# In[236]:


#date mapping and random other functions
currentYear = 2022
if datetime.now().year > currentYear:
    currentYear = datetime.now().year
currentDay = datetime.now().day
currentMonth = datetime.now().month
str_date = str(currentYear)+'.'+str(currentMonth)+'.'+str(currentDay)

date_map = {
    
    'Jan': '1',
    'Feb': '2',
    'Mar': '3',
    'Apr': '4',
    'May': '5',
    'Jun': '6',
    'Jul': '7',
    'Aug': '8',
    'Sep': '9',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

def fix_new_year(x):
    for n in x:
        if n[:2] == 'Jan':
            return x + f', {currentYear}'
        else:
            return x + ', 2022' 


# In[151]:


scoring_weights = {
    'rec': 0.5,
    'rec_yds': 0.1,
    'rec_td': 6,
    'FL': -2,
    'rush_yds': 0.1,
    'rush_td': 6,
    'pass_yds': 0.04,
    'pass_td': 4,
    'int': -2
}


# In[238]:


#scrapes redzone attempts per yardline (20,15,10,5) per year
def rz_total(season):
    
    rz_stats = pd.DataFrame()

    qb_total = pd.DataFrame()

    for yard in np.arange(5, 25 , 5):

        for i in range(1, 19):

            url = f'https://www.fantasypros.com/nfl/red-zone-stats/qb.php?year={season}&week={i}&range=week&yardline={yard}'
            link = requests.get(url).content
            soup = bs(link, 'html.parser')
            read = etree.HTML(str(soup))

            #qb
            players = read.xpath('//tr/td[2]/a/text()')
            rz_passing_att = read.xpath('//tr/td[4]/text()')
            rz_passing_td = read.xpath('//tr/td[8]/text()')
            rz_rushing_att = read.xpath('//tr/td[11]/text()')
            rz_rushing_td = read.xpath('//tr/td[13]/text()')

            data = {
                'player': players,
                'pos': 'QB',
                'week': i,
                'inside_yardline': yard,
                'rz_passing_att': rz_passing_att,
                'rz_passing_td': rz_passing_td,
                'rz_rushing_att': rz_rushing_att,
                'rz_rushing_td': rz_rushing_td
            }

            df = pd.DataFrame(data)
            qb_total = pd.concat([qb_total, df])
    
    rb_total = pd.DataFrame()

    for yard in np.arange(5, 25 , 5):

        for i in range(1, 19):

            url = f'https://www.fantasypros.com/nfl/red-zone-stats/rb.php?year={season}&week={i}&range=week&yardline={yard}'
            link = requests.get(url).content
            soup = bs(link, 'html.parser')
            read = etree.HTML(str(soup))

            #rb
            players = read.xpath('//tr/td[2]/a/text()')
            rz_rushing_att = read.xpath('//tr/td[3]/text()')
            rz_rushing_td = read.xpath('//tr/td[6]/text()')
            rz_rec_target = read.xpath('//tr/td[9]/text()')
            rz_rec_td = read.xpath('//tr/td[13]/text()')

            data = {
                        'player': players,
                        'pos': 'RB',
                        'week': i,
                        'inside_yardline': yard,
                        'rz_rushing_att': rz_rushing_att,
                        'rz_rushing_td': rz_rushing_td,
                        'rz_rec_target': rz_rushing_att,
                        'rz_rec_td': rz_rushing_td
                    }

            df = pd.DataFrame(data)
            rb_total = pd.concat([rb_total, df])
            
    wr_total = pd.DataFrame()

    for yard in np.arange(5, 25 , 5):

        for i in range(1, 19):

            url = f'https://www.fantasypros.com/nfl/red-zone-stats/wr.php?year={season}&week={i}&range=week&yardline={yard}'
            link = requests.get(url).content
            soup = bs(link, 'html.parser')
            read = etree.HTML(str(soup))

            #wr
            players = read.xpath('//tr/td[2]/a/text()')
            rz_rec_target = read.xpath('//tr/td[4]/text()')
            rz_rec_td = read.xpath('//tr/td[8]/text()')
            rz_rushing_att = read.xpath('//tr/td[10]/text()')
            rz_rushing_td = read.xpath('//tr/td[12]/text()')

            data = {
                'player': players,
                'pos': 'WR',
                'week': i,
                'inside_yardline': yard,
                'rz_rec_target': rz_rec_target,
                'rz_rec_td': rz_rec_td,
                'rz_rushing_att': rz_rushing_att,
                'rz_rushing_td': rz_rushing_td
            }

            df = pd.DataFrame(data)
            wr_total = pd.concat([wr_total, df])
            
    te_total = pd.DataFrame()

    for yard in np.arange(5, 25 , 5):

        for i in range(1, 19):

            url = f'https://www.fantasypros.com/nfl/red-zone-stats/wr.php?year=2020&week={i}&range=week&yardline={yard}'
            link = requests.get(url).content
            soup = bs(link, 'html.parser')
            read = etree.HTML(str(soup))

            #wr
            players = read.xpath('//tr/td[2]/a/text()')
            rz_rec_target = read.xpath('//tr/td[4]/text()')
            rz_rec_td = read.xpath('//tr/td[8]/text()')
            rz_rushing_att = read.xpath('//tr/td[10]/text()')
            rz_rushing_td = read.xpath('//tr/td[12]/text()')

            data = {
                'player': players,
                'pos': 'TE',
                'week': i,
                'inside_yardline': yard,
                'rz_rec_target': rz_rec_target,
                'rz_rec_td': rz_rec_td,
                'rz_rushing_att': rz_rushing_att,
                'rz_rushing_td': rz_rushing_td
            }

            df = pd.DataFrame(data)
            te_total = pd.concat([te_total, df])
            
    rz_stats = pd.concat([qb_total, rb_total, wr_total, te_total]).reset_index(drop=True)
    
    return rz_stats

#scrapes snap counts per week
def ff_snaps(season):

    weekly_snaps = pd.DataFrame()

    for i in range (1, 19):

        url = f'https://www.fantasypros.com/nfl/reports/snap-count-analysis/?year={season}&range=week&week={i}'
        link = requests.get(url).content
        soup = bs(link, 'html.parser')
        read = etree.HTML(str(soup))

        players = read.xpath('//tr/td[1]/a/text()')
        positions = read.xpath('//tr/td[2]/text()')
        teams = read.xpath('//tr/td[3]/a/text()')
        snaps = read.xpath('//tr/td[5]/text()')
        snap_percent = read.xpath('//tr/td[7]/text()')
        rush_percent = read.xpath('//tr/td[8]/text()')
        target_percent = read.xpath('//tr/td[9]/text()')
        touch_percent = read.xpath('//tr/td[10]/text()')
        util_percent = read.xpath('//tr/td[11]/text()')

        columns = ['players', 'positions', 'teams', 'snaps', 'snap_percent', 'rush_percent', 'tgt_percent',
                   'touch_percent', 'util_percent']
        columns_data = [players, positions, teams, snaps, snap_percent, rush_percent, target_percent, touch_percent,
                        util_percent]

        data = {
            'players': players,
            'positions': positions,
            'teams': teams,
            'week': i,
            'snaps': snaps,
            'snap_perc': snap_percent,
            'rush_perc': rush_percent,
            'tgt_perc': target_percent,
            'touch_perc': touch_percent,
            'util_perc': util_percent
        }

        data_df = pd.DataFrame(data)
        weekly_snaps = pd.concat([weekly_snaps, data_df])
    
    return weekly_snaps

#pulls weather, ids, and matchup data from nflfastpy
def nflpy_tables(season):
  
  def pull_temp(row):
      for t in row['weather'].split():
          for tt in t:
              if '°' in tt:
                  return int((t[:-1]))
              
  def pull_humid(row):
      for t in row['weather'].split():
          for tt in t:
              if '%' in tt:
                  return int(t[:-2])
              
  def pull_wind(row):
      for t in row['weather'].split():
            try:
                return int(t)
            except ValueError:
                pass

  df_raw = nflfastpy.load_pbp_data(year=season)
  df = df_raw.copy()
  df['weather'] = df['weather'].astype(str)

  #id dataframe
  ids = df[['id', 'name', 'posteam']].dropna().groupby('id', as_index=False).max()

  df['temperature'] = df.apply(pull_temp, axis=1)
  df['humidity'] = df.apply(pull_humid, axis=1)
  df['wind_speed'] = df.apply(pull_wind, axis=1)

  #weather
  weather = df[['week', 'posteam', 'posteam_type', 'temperature', 'humidity', 'wind_speed']].groupby(['week', 'posteam', 'posteam_type'], as_index=False).max()
  #matchups
  matchups = df[['week', 'posteam', 'defteam']].dropna().groupby(['week', 'posteam'], as_index=False).max()

  return ids, weather, matchups

def injury_tracker():
    
    url = 'https://www.covers.com/sport/football/nfl/injuries'
    link = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
    soup = bs(link, 'html.parser')
    read = etree.HTML(str(soup))

    players_raw = read.xpath('//tr/td/a/text()')
    players = [n.replace('\n','').replace('\r','').replace(' ','').strip() for n in players_raw]
    players = [n for n in players if n != '']

    pos = read.xpath('//tr/td[2]/text()')

    last_updated = read.xpath('//tr/td[3]/text()')
    last_updated = [n.replace('\n','').replace('\r','').replace('(','').replace(')', '').strip()[5:] for n in last_updated]

    injury = read.xpath('//tr/td/b/text()')

    data = {
        'Player': players,
        'POS': pos,
        'Last Update': last_updated,
        'Injury': injury
    }

    df = pd.DataFrame(data)
    df['Last Update'] = df['Last Update'].apply(fix_new_year)
    df['Last Update'] = pd.to_datetime(df['Last Update'], format='%b %d, %Y')
    
    return df

def pull_adp(scoring):    

    if scoring == 'standard':
        score = 'overall'
    elif scoring == 'ppr':
        score = 'ppr-overall'
    elif scoring == 'halfppr':
        score = 'half-point-ppr-overall'

    url = f'https://www.fantasypros.com/nfl/adp/{score}.php'
    link = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
    soup = bs(link, 'html.parser')
    read = etree.HTML(str(soup))

    if scoring == 'standard':
        players = read.xpath('//tr/td/a/text()')[:300]
        pos = [n[:2] for n in read.xpath('//tr/td[3]/text()')[:300]]
        adp = read.xpath('//tr/td[9]/text()')[:300]

    elif scoring == 'ppr':
        players = read.xpath('//tr/td/a/text()')[:300]
        pos = [n[:2] for n in read.xpath('//tr/td[3]/text()')[:300]]
        adp = read.xpath('//tr/td[10]/text()')[:300]

    elif scoring == 'halfppr':
        players = read.xpath('//tr/td/a/text()')[:300]
        pos = [n[:2] for n in read.xpath('//tr/td[3]/text()')[:300]]
        adp = read.xpath('//tr/td[8]/text()')[:300]

    data = {
        'Player': players,
        'POS': pos,
        'ADP': adp
    }

    df = pd.DataFrame(data)
    df['ADP'] = df['ADP'].astype(float)
    df = df.loc[df['POS'].isin(['QB', 'RB', 'WR', 'TE'])].sort_values('ADP')
    df = df.reset_index(drop=True)

    return df

#pull raw projected stats from fantasypros and apply custom formulas from scoring_weights
def pull_projected_custom():
    
    scoring_weights = {
        'rec': 0.5,
        'rec_yds': 0.1,
        'rec_td': 6,
        'FL': -2,
        'rush_yds': 0.1,
        'rush_td': 6,
        'pass_yds': 0.04,
        'pass_td': 4,
        'int': -2
    }

    for position in ['qb', 'rb', 'wr', 'te']:

        url = f'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft'
        link = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
        soup = bs(link, 'html.parser')
        read = etree.HTML(str(soup))

        if position == 'qb':
            players = read.xpath('//tr/td/a/text()')
            players = [n for n in players if n not in ('Site Projections', 'CBS Sports', 'ESPN', 'numberFire', 'FFToday')]
            pass_yds = [n.replace(',','') for n in read.xpath('//tr/td[4]/text()')[:-4]]
            pass_td = read.xpath('//tr/td[5]/text()')
            ints = read.xpath('//tr/td[6]/text()')
            rush_yds = [n.replace(',','') for n in read.xpath('//tr/td[8]/text()')]
            rush_td = read.xpath('//tr/td[9]/text()')
            FL = read.xpath('//tr/td[10]/text()')

            data = {
                'players': players,
                'pos': 'QB',
                'pass_yds': pass_yds,
                'pass_td': pass_td,
                'int': ints,
                'rush_yds': rush_yds,
                'rush_td': rush_td,
                'FL': FL
            }

            df_qb = pd.DataFrame(data)

        if position == 'rb':
            players = read.xpath('//tr/td/a/text()')
            players = [n for n in players if n not in ('Site Projections', 'CBS Sports', 'ESPN', 'numberFire', 'FFToday')]
            rush_yds = [n.replace(',','') for n in read.xpath('//tr/td[3]/text()')]
            rush_td = read.xpath('//tr/td[4]/text()')[:-4]
            rec = read.xpath('//tr/td[5]/text()')
            rec_yds = [n.replace(',','') for n in read.xpath('//tr/td[6]/text()')]
            rec_td = read.xpath('//tr/td[7]/text()')
            FL = read.xpath('//tr/td[8]/text()')

            data = {
                'players': players,
                'pos': 'RB',
                'rush_yds': rush_yds,
                'rush_td': rush_td,
                'rec': rec,
                'rec_yds': rec_yds,
                'rec_td': rec_td,
                'FL': FL
            }


            df_rb = pd.DataFrame(data)

        if position == 'wr':
            players = read.xpath('//tr/td/a/text()')
            players = [n for n in players if n not in ('Site Projections', 'CBS Sports', 'ESPN', 'numberFire', 'FFToday')]
            rec = read.xpath('//tr/td[2]/text()')
            rec_yds = [n.replace(',','') for n in read.xpath('//tr/td[3]/text()')]
            rec_td = read.xpath('//tr/td[4]/text()')[:-4]
            rush_yds = [n.replace(',','') for n in read.xpath('//tr/td[6]/text()')]
            rush_td = read.xpath('//tr/td[7]/text()')
            FL = read.xpath('//tr/td[8]/text()')

            data = {
                'players': players,
                'pos': 'WR',
                'rec': rec,
                'rec_yds': rec_yds,
                'rec_td': rec_td,
                'rush_yds': rush_yds,
                'rush_td': rush_td,
                'FL': FL
            }


            df_wr = pd.DataFrame(data)

        if position == 'te':
            players = read.xpath('//tr/td/a/text()')
            players = [n for n in players if n not in ('Site Projections', 'CBS Sports', 'ESPN', 'numberFire', 'FFToday')]
            rec = read.xpath('//tr/td[2]/text()')
            rec_yds = [n.replace(',','') for n in read.xpath('//tr/td[3]/text()')]
            rec_td = read.xpath('//tr/td[4]/text()')[:-4]
            FL = read.xpath('//tr/td[5]/text()')

            data = {
                'players': players,
                'pos': 'TE',
                'rec': rec,
                'rec_yds': rec_yds,
                'rec_td': rec_td,
                'FL': FL
            }


            df_te = pd.DataFrame(data)


    df_final = pd.concat([df_qb, df_rb, df_wr, df_te])
    df_final = df_final.fillna(0)

    for col in df_final.columns[2:]:
        df_final[col] = df_final[col].astype(float)

    df_final['fantasy_points'] = df_final['pass_yds']*scoring_weights['pass_yds']+df_final['pass_td']*scoring_weights['pass_td']+            df_final['int']*scoring_weights['int']+df_final['rush_yds']*scoring_weights['rush_yds']+            df_final['rush_td']*scoring_weights['rush_td']+df_final['FL']*scoring_weights['FL']+            df_final['rec']*scoring_weights['rec']+df_final['rec_yds']*scoring_weights['rec_yds']+            df_final['rec_td']*scoring_weights['rec_td']
    
    df_final = df_final[['players', 'pos', 'fantasy_points']]
    return df_final


#choose STD, HALF, or PPR
def pull_projected_points(scoring):

    # we are going to concatenate our individual position dfs into this larger final_df
    final_df = pd.DataFrame()

    #url has positions in lower case
    for position in ['rb', 'qb', 'te', 'wr']:
        
        BASE_URL = f'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring={scoring}&week=draft'

        res = requests.get(BASE_URL) # format our url with the position
        if res.ok:
            soup = bs(res.content, 'html.parser')
            table = soup.find('table', {'id': 'data'})
            df = pd.read_html(str(table))[0]

            df.columns = df.columns.droplevel(level=0) # our data has a multi-level column index. The first column level is useless so let's drop it.
            df['PLAYER'] = df['Player'].apply(lambda x: ' '.join(x.split()[:-1])) # fixing player name to not include team
            df['TEAM'] = df['Player'].apply(lambda x: x[-3:].replace(' ', '').strip())

            df['POS'] = position.upper() # add a position column

            df = df[['PLAYER', 'TEAM', 'POS', 'FPTS']]
            final_df = pd.concat([final_df, df]) # iteratively add to our final_df
        else:
            print('oops something didn\'t work right', res.status_code)

    final_df = final_df.sort_values(by='FPTS', ascending=False) # sort df in descending order on FPTS column
    
    return final_df

#choose standard, ppr, or halfppr
def get_draft_board(scoring):

    replacement_players = {
        'QB': '',
        'RB': '',
        'WR': '',
        'TE': ''
    }

    adp_df = pull_adp(scoring)

    if scoring == 'standard':
        score_system = 'STD'
    elif scoring == 'ppr':
        score_system = 'PPR'
    elif scoring == 'halfppr':
        score_system = 'HALF'

    projections = pull_projected_points(score_system)
    adp_df_cutoff = adp_df[:100]

    for _, row in adp_df_cutoff.iterrows():
        position = row['POS']
        player = row['Player']

        if position in replacement_players:
            replacement_players[position] = player

    replacement_values = {}

    for position, player_name in replacement_players.items():
        player = projections.loc[projections.PLAYER == player_name]
        replacement_values[position] = player['FPTS'].tolist()[0]

    projections = projections.loc[projections.POS.isin(['QB', 'RB', 'WR', 'TE'])]
    projections['VOR'] = projections.apply(lambda row: row['FPTS'] - replacement_values.get(row['POS']), axis=1)
    projections['VOR Rank'] = projections['VOR'].rank(ascending=False).astype(int)
    projections = projections.sort_values('VOR', ascending=False)

    adp_df = adp_df.rename({'Player': 'PLAYER'}, axis=1)
    complete_df = projections.merge(adp_df, how='left', on=['PLAYER', 'POS'])[:200].dropna()
    complete_df['ADP Rank'] = complete_df['ADP'].rank().astype(int)
    complete_df['Sleeper Score'] = complete_df['ADP Rank'] - complete_df['VOR Rank']
    complete_df = complete_df[['PLAYER', 'POS', 'VOR Rank', 'ADP Rank', 'Sleeper Score']]
    
    return complete_df

#downloads standard, ppr, and halfppr draftboards to a folder
def pull_draft_boards():

    score_system_list = ['standard', 'ppr', 'halfppr']
    for score in score_system_list:
        df = get_draft_board(score)
        df.to_excel(f'C:/Users/Tyler/Desktop/NFL Tables/Draft Boards/{score}_asof_{str_date}.xlsx', index=False)


# In[6]:


#fantasypros fantasy points allowed
#depth chart per team
#touchdown regression
##https://gist.github.com/fantasydatapros/3ddda4b29b3b8fa5ba045737c7a14f13#file-is24p-ipynb
#format player names
#weekly fantasy projected stats
#add adp scraping and the VOR method
#schedule data for matchups
#test stuff out in access


# In[169]:


#ids, weather, matchups = nflpy_tables(2021)
injuries = injury_tracker()
ff_snaps = ff_snaps(2021)
rz_total = rz_total(2021)

export = {
    'ids': ids, 
    'weather': weather,
    'matchups': matchups,
    'injuries': injuries,
    'ff_snaps': ff_snaps, 
    'rz_total': rz_total
}

for file_name, data in export.items():
    data.to_excel(f'C:/Users/Tyler/Desktop/NFL Tables/{file_name}.xlsx', index=False)


# In[164]:


injuries.to_excel('C:/Users/Tyler/Desktop/NFL Tables/injuries.xlsx', index=False)


# In[189]:


#this whole code is used for custom projections NOT regular scoring
replacement_players = {
    'QB': '',
    'RB': '',
    'WR': '',
    'TE': ''
}

adp_df = pull_adp('halfppr')
projections = pull_projected_custom()
adp_df_cutoff = adp_df[:100]

for _, row in adp_df_cutoff.iterrows():
    position = row['POS']
    player = row['Player']
    
    if position in replacement_players:
        replacement_players[position] = player
        
replacement_values = {}

for position, player_name in replacement_players.items():
    player = projections.loc[projections.players == player_name]
    replacement_values[position] = player['fantasy_points'].tolist()[0]
    
projections = projections.loc[projections.pos.isin(['QB', 'RB', 'WR', 'TE'])]
projections['VOR'] = projections.apply(lambda row: row['fantasy_points'] - replacement_values.get(row['pos']), axis=1)
projections['VOR Rank'] = projections['VOR'].rank(ascending=False).astype(int)
projections = projections.sort_values('VOR', ascending=False)

adp_df = adp_df.rename({'Player': 'players',
                        'POS': 'pos'}, axis=1)
complete_df = projections.merge(adp_df, how='left', on=['players', 'pos'])[:200]
complete_df['ADP Rank'] = complete_df['ADP'].rank()
complete_df['Sleeper Score'] = complete_df['ADP Rank'] - complete_df['VOR Rank']
complete_df = complete_df[['players', 'pos', 'ADP Rank', 'VOR Rank', 'Sleeper Score']]
complete_df


# In[239]:


pull_draft_boards()


# In[237]:





# In[235]:





# In[ ]:




