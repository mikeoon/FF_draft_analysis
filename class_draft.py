import numpy as np
import pandas as pd
import random as rand
import class_team as team


class draftLeague():

	def __init__(self, year):
		self.num_teams = None
		self.league = {}
		self.rankings = self.get_ranks(year)
		self.dorder = None





# Reads in CSV file of predraft/season ranks
	def get_ranks(self, year):
		rankings = {'WR':None, 'RB':None, 'QB':None, 'TE':None, 'DST':None, 'K':None}
		csv_ranks = pd.read_csv(f'data/pre_draft_rank/espn_rankings_{year}.csv')
		for key in rankings.keys():
			rankings[key] = pd.DataFrame(csv_ranks[csv_ranks['pos'] == key])
		return rankings
# Creates the number of teams in the league from specified number
# Default is the minium which is set to 8
	def create_teams(self, num=8):
		self.num_teams = num
		for n in num:
			self.league[f'team{n}'] = team.ffTeam(f'team{n}')

	def get_teamnames(self):
		return self.league.keys()

	def get_numteams(self):
		return self.num_teams

	def make_draftorder(self, custom=False, **kwargs):
		if custom:
			self.dorder = kwargs['order']
		else:
			self.dorder = list()
			while len(self.dorder) != num_teams:
				self.dorder.append(rand.choice(self.league.keys()))
			print(self.dorder)


	def draft(self):
		pass


























