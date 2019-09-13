import numpy as np
import pandas as pd
import read_help as rh
import matplotlib.pyplot as plt

plt.style.use('ggplot')

year = 2000
dfs = {}
for i in range(7, 20, 1):
    dfs[f'{year+i}'] = rh.read_adp_csv(year+i)
    dfs[f'{year+i}']['year'] = year+i

count = 0
for df in dfs.values():
    if count == 0:
        full_df = pd.DataFrame(df)
        count+=1
    else:
        full_df=full_df.merge(df, how='outer')


leader_year = {}
for year in range(12, 18, 1):
    leader_year[f'20{year}'] = rh.read_leaders_csv(year)

new_rank = {}

for y in leader_year.keys():

	leader_year[y] = leader_year[y].rename(columns={'Player':'player'})

	adp_leader = pd.DataFrame(dfs['2012'].merge(leader_year[y], on="player", how='left'))
	adp_leader['pick_v_rank'] = adp_leader['pick'] - adp_leader['Rank']

	adp_leader_pos = {'RB':None, 'WR':None, 'QB':None, 'TE':None, 'DEF':None, 'PK':None}

	for pos in adp_leader_pos.keys():
	    adp_leader_pos[pos] = pd.DataFrame(adp_leader[adp_leader['pos'] == pos].sort_values('Points', ascending=False)).reset_index().drop('index', axis=1)
	    adp_leader_pos[pos]['pos_rank'] = adp_leader_pos[pos].index + 1
	    adp_leader_pos[pos] = adp_leader_pos[pos].set_index('pos_rank')
	    low = adp_leader_pos[pos]['pick_v_rank'].min()
	    adp_leader_pos[pos]['pick_v_rank'] = adp_leader_pos[pos]['pick_v_rank'].fillna(low)
	    adp_leader_pos[pos]['pick_v_posrank'] = adp_leader_pos[pos]['pick'] - adp_leader_pos[pos].index

	new_rank[y] = adp_leader_pos

positions = ['RB', 'WR', 'QB', 'TE', 'DEF', 'PK']

for p in positions:
	pick_rank = {}
	for k, v in new_rank.items():
		pick_rank[k] = (v[p])

	data = list()
	label = list()

	for pos, v in pick_rank.items():
		data.append(v['pick_v_posrank'])

		label.append(pos)
	fig, ax = plt.subplots( figsize=(10, 10))
	ax.boxplot(data, labels=label)
	ax.set_title(f'Pre season ADP - End of Season {p} Ranks')
	ax.set_ylabel(f'ADP - {p} Rank for that Year')
	plt.savefig(f'/Users/youngjungyoon/GalvanizeDataScience/capstone1/data/plots/{p}_year_posrank.png')












