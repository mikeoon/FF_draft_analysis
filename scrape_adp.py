import copy
import pandas as pd
import pprint
import requests
from bs4 import BeautifulSoup


# scrapes Fantasy football calculator for ADP for the below years
# Batch so turn it off if you need to

years = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

for y in years:
	adp = f'https://fantasyfootballcalculator.com/adp/ppr/12-team/all/20{y}'
	r = requests.get(adp)

	print(r)
	print()


	soup = BeautifulSoup(r.content, "lxml")

	table = soup.find('table', {'class' : 'table adp'}).find_all('tr')

	empty_row = {'pick': None, 'player' : None, 'team' : None,
				 'pos' : None, 'overall' : None, 'stdev' : None,
				 'high' : None, 'low': None, 'num_drafted' : None}

	all_rows = []

	for row in range(1, len(table)):
		copy_row = copy.copy(empty_row)
		player = table[row].find_all('td')
		copy_row['pick'] = player[1].string
		copy_row['player'] = player[2].find('a').string # need to grab the actual string for name
		copy_row['pos'] = player[3].string
		copy_row['team'] = player[4].string
		copy_row['overall'] = player[5].string
		copy_row['stdev'] = player[6].string
		copy_row['high'] = player[7].string
		copy_row['low'] = player[8].string
		copy_row['num_drafted'] = player[9].string
		all_rows.append(copy_row)


	result_df = pd.DataFrame(all_rows)

	result_df.to_csv(f'data/adp/adp_20{y}.csv', index=False)

	print(f'done with 20{y}')



























