import numpy as np
import copy
import pandas as pd
import class_pos as cp
import read_season_data as rsd
import class_team as ct
import class_league as cleague
import json


# Hard code schedule
# each team plays division 3 times, plays other divison once
wk1 = (['team1', 'team2', 'team5', 'team6'], ['team3', 'team4', 'team7', 'team8'])
wk2 = (['team1', 'team2', 'team5', 'team6'], ['team4', 'team3', 'team8', 'team7'])
wk3 = (['team1', 'team3', 'team5', 'team7'], ['team2', 'team4', 'team6', 'team8'])

wk4 = (['team1', 'team2', 'team3', 'team4'], ['team5', 'team6', 'team7', 'team8'])
wk5 = (['team1', 'team2', 'team3', 'team4'], ['team6', 'team7', 'team8', 'team5'])
wk6 = (['team1', 'team2', 'team3', 'team4'], ['team7', 'team8', 'team5', 'team6'])
wk7 = (['team1', 'team2', 'team3', 'team4'], ['team8', 'team5', 'team6', 'team7'])

wk8 = (['team1', 'team2', 'team5', 'team6'], ['team3', 'team4', 'team7', 'team8'])
wk9 = (['team1', 'team2', 'team5', 'team6'], ['team4', 'team3', 'team8', 'team7'])
wk10 = (['team1', 'team3', 'team5', 'team7'], ['team2', 'team4', 'team6', 'team8'])

wk11 = (['team1', 'team2', 'team5', 'team6'], ['team3', 'team4', 'team7', 'team8'])
wk12 = (['team1', 'team2', 'team5', 'team6'], ['team4', 'team3', 'team8', 'team7'])
wk13 = (['team1', 'team3', 'team5', 'team7'], ['team2', 'team4', 'team6', 'team8'])


team1_picks = ['WR','WR', 'WR', 'WR', 'RB', 'RB', 'RB', 'RB', 'QB','QB', 'TE', 'TE', 'DST', 'K', 'DST', 'K']
team2_picks = ['WR','RB', 'WR', 'RB', 'WR', 'RB', 'WR', 'RB', 'QB','TE', 'QB', 'TE', 'DST', 'K', 'DST', 'K']
team3_picks = ['RB','WR', 'RB', 'WR', 'RB', 'WR', 'RB', 'WR', 'QB','QB', 'TE', 'TE', 'DST', 'K', 'DST', 'K']
team4_picks = ['WR','WR', 'WR', 'RB', 'WR', 'RB', 'RB', 'RB', 'QB','QB', 'TE', 'TE', 'DST', 'K', 'DST', 'K']
team5_picks = ['RB','RB', 'RB', 'RB', 'WR', 'WR', 'WR', 'WR', 'QB','QB', 'TE', 'TE', 'DST', 'K', 'DST', 'K']
team6_picks = ['WR','RB', 'QB', 'WR', 'TE', 'RB', 'RB', 'RB', 'WR','QB', 'RB', 'TE', 'DST', 'K', 'DST', 'K']
team7_picks = ['RB','RB', 'WR', 'WR', 'RB', 'RB', 'WR', 'WR', 'QB','QB', 'TE', 'TE', 'DST', 'K', 'DST', 'K']
team8_picks = ['WR','RB', 'WR', 'WR', 'WR', 'QB', 'TE', 'RB', 'RB','QB', 'RB', 'TE', 'DST', 'K', 'DST', 'K']





def sim_seasons(year, name_sim='default', num_sim=1):
	schedule = [wk1, wk2, wk3, wk4, wk5, wk6, wk7, wk8, wk9, wk10, wk11, wk12, wk13]
	team_picks = [team1_picks, team2_picks, team3_picks, team4_picks, team5_picks, team6_picks, team7_picks, team8_picks]
	sim_data = []
	for _ in range(num_sim):
		season = cleague.createLeague(year)
		season.create_teams()
		season.set_dftpicks(team_picks)
		season.set_draftorder()
		season.draft()

		week = 1
		for wk in schedule:
			season.sim_matchup(wk[0], wk[1], week)
			week+=1

		season_stnd = season.get_standings().reset_index()
		empty_row = {'team':None, 'W':None, 'L':None, 'T':None, 'total_points':None, 'stnd':None}

		# Records for teams are in form [W, L, T]
		for team in season.get_pttotals():
			new_row = copy.copy(empty_row)
			record = season_stnd[season_stnd['team'] == team[0]]

			new_row['team'] = team[0]
			new_row['W'] = record['W'].iloc[0]
			new_row['L'] = record['L'].iloc[0]
			new_row['T'] = record['T'].iloc[0]
			new_row['stnd'] = record.index[0]
			new_row['total_points'] = team[1]

			sim_data.append(pd.Series(new_row))
		print(f'Sim {_} complete')

	sim_results = pd.DataFrame(sim_data)
	sim_results.to_csv(f'data/season_sim_{year}/sim_{name_sim}.csv')
	print(f'Sim {name_sim} results saved to : \n data/season_sim_{year}/sim_{name_sim}.csv')














