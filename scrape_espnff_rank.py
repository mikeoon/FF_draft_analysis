import copy
import pandas as pd
from pymongo import MongoClient
import pprint


# Requests sends and recieves HTTP requests.
import requests

# Beautiful Soup parses HTML documents in python.
from bs4 import BeautifulSoup



espn = 'https://www.espn.com/fantasy/football/story/_/page/18RanksPreseason300nonPPR/2018-fantasy-football-non-ppr-rankings-top-300'
r = requests.get(espn)

print(r)
print()

# For rankings without bye weeks
# currently set for 2018 buy weeks
bye_sched = {'NYJ':4, 'SF':4, 'DET':5, 'MIA':5, 'BUF':6, 'CHI':6, 'IND':6,
			'OAK':6, 'CAR':7, 'CLE':7, 'PIT':7, 'TB':7, 'BAL':8, 'DAL':8,
			'ATL':9, 'CIN':9, 'LAR':9, 'NO':9, 'DEN':10, 'HOU':10, 'JAC':10, 'NE':10,
			'PHI':10, 'WAS':10, 'GB':11, 'NYG':11, 'SEA':11, 'TEN':11, 'ARI':12,
			'KC':12, 'LAC':12, 'MIN':12, 'FA':8}

soup = BeautifulSoup(r.content, "lxml")

table = soup.find_all('aside', {'class' : 'inline inline-table'}, limit=2)

# table[1] is where the overall data is
tr = table[1].find('table', {'class' : 'inline-table'})
plist = tr.find('tbody')
ranks = plist.find_all('tr', {'class' : 'last'})


#all_rows = pd.DataFrame(columns=['rank', 'player', 'team', 'pos'])
all_rows=[]

empty_row = {'rank': None, 'player' : None, 'team' : None, 'pos' : None, 'bye' : None}

for i in ranks:
	copy_erow = copy.copy(empty_row)
	pr = i.find_all('td')
	if pr[0].string is not None:
		temp_string = pr[0].string.split('. ')
		copy_erow['player'] = temp_string[1].strip()
		copy_erow['rank'] = temp_string[0] 
	else:
		copy_erow['player'] = pr[0].find('a').string
		copy_erow['rank'] = pr[0].contents[0].strip('. ')

	copy_erow['team'] = pr[2].string.strip()
	copy_erow['pos'] = pr[1].string.strip()
	copy_erow['bye'] = bye_sched[pr[2].string.strip()]

	all_rows.append(copy_erow)

scrape_result=pd.DataFrame(all_rows)


scrape_result.to_csv('data/pre_draft_rank/espn_rankings_18_BYE.csv', index=False)

print('done')












