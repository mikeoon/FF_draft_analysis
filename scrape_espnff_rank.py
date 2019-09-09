import copy
import pandas as pd
from pymongo import MongoClient
import pprint


# Requests sends and recieves HTTP requests.
import requests

# Beautiful Soup parses HTML documents in python.
from bs4 import BeautifulSoup



espn = 'https://www.espn.com/fantasy/football/story/_/id/12866396/top-300-rankings-2015'
r = requests.get(espn)

print(r)
print()
'''
client = MongoClient('localhost', 27017)
db = client.espn_mbarry
pages = db.pages

pages.insert_one({'html': r.content})
'''

soup = BeautifulSoup(r.content, "lxml")

table = soup.find_all('aside', {'class' : 'inline inline-table'}, limit=2)

# table[1] is where the overall data is
tr = table[1].find('table', {'class' : 'inline-table'})
plist = tr.find('tbody')
ranks = plist.find_all('tr', {'class' : 'last'})


#all_rows = pd.DataFrame(columns=['rank', 'player', 'team', 'pos'])
all_rows=[]

empty_row = {'rank': None, 'player' : None, 'team' : None, 'pos' : None}

for i in ranks:
	copy_erow = copy.copy(empty_row)
	pr = i.find_all('td')
	if pr[0].string is not None:
		temp_string = pr[0].string.split(' ')
		copy_erow['rank'] = int(temp_string[0].strip('.'))
		copy_erow['player'] = temp_string[1] + ' ' + temp_string[2]
	else:
		copy_erow['rank'] = int(pr[0].contents[0].string.strip('. '))
		copy_erow['player'] = pr[0].find('a').string

	copy_erow['team'] = pr[1].string
	copy_erow['pos'] = pr[2].string

# This is for 2015 pre season rankings, formatted differently 
	'''
	if pr[3].string[:3] == 'DST':
		copy_erow['pos'] = pr[3].string[:3]
	else:
		copy_erow['pos'] = pr[3].string[:2]
	'''

	all_rows.append(copy_erow)

scrape_result=pd.DataFrame(all_rows)


scrape_result.to_csv('data/pre_draft_rank/espn_rankings_15.csv', index=False)

print('done')












