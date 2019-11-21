import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


# Currently set to scraping the 2017 predraft rankings
espn = 'https://www.espn.com/fantasy/football/story/_/page/17RanksPreseason200nonPPR/2017-fantasy-football-standard-rankings-non-ppr-top-200'
season='17'
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

#table = soup.find_all('aside', {'class' : 'inline inline-table'}, limit=2)

table = soup.find_all('table', {'class' : 'inline-table'}, limit=2)
# table[1] is where the overall data is
#tr = table[1].find('table', {'class' : 'inline-table'})
plist = table[1].find('tbody')
ranks = plist.find_all('tr', {'class' : 'last'})


#all_rows = pd.DataFrame(columns=['rank', 'player', 'team', 'pos'])
all_rows=[]

empty_row = {'rank': None, 'player' : None, 'team' : None, 'pos' : None, 'bye' : None}

for row in ranks:
	copy_erow = empty_row.copy()
	player_info =  row.find_all('td')
	first = re.split('\d{1,}\.', player_info[0].text)
	second = first[1].split(', ')
	copy_erow['player'] = second[0].strip()
	copy_erow['rank'] = re.match('\d{1,}\.', player_info[0].text)[0].strip('. ')
	copy_erow['pos'] = second[1].strip().replace('/', '') # Replace is here for D/ST change to DST
	copy_erow['bye'] = player_info[2].text.strip()
	copy_erow['team'] = second[2].strip()

	all_rows.append(copy_erow)

scrape_result=pd.DataFrame(all_rows)

print(scrape_result.head())
scrape_result.to_csv(f'data/pre_draft_rank/espn_rankings_{season}_BYE.csv', index=False)

print('done')












