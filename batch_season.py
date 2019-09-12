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

def sim_seasons(year, name_sim='default', num_sim=1):
	schedule = [wk1, wk2, wk3, wk4, wk5, wk6, wk7, wk8, wk9, wk10, wk11, wk12, wk13]
	sim_data = []
	for _ in range(num_sim):
		season = cleague.createLeague(year)
		season.create_teams()
		season.set_draftorder()
		season.draft()

		week = 1
		for wk in schedule:
			season.sim_matchup(wk[0], wk[1], week)
			week+=1

		empty_row = {'team':None, 'W':None, 'L':None, 'total_points':None}
		# Standings are in form [W, L, T]
		for team in zip(season.get_standings(), season.get_pttotals()):
			new_row = copy.copy(empty_row)
			new_row['team'] = team[0][0]
			new_row['W'] = team[0][1][0]
			new_row['L'] = team[0][1][1]
			new_row['total_points'] = team[1][1]
			sim_data.append(pd.Series(new_row))
		print(f'Sim {_} complete')

	sim_results = pd.DataFrame(sim_data)
	sim_results.to_csv(f'data/season_sim_{year}/sim_{name_sim}.csv')
	print(f'Sim {name_sim} results saved to : \n data/season_sim_{year}/sim_{name_sim}.csv')














