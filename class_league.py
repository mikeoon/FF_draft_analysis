import numpy as np
import pandas as pd
import random as rand
import class_team as team
import class_pos as p


class createLeague():

# Initializes the league with what year you want to use preseason data
	def __init__(self, year):
		self.num_teams = None
		self.league = {}
		self.rankings = self.get_ranks(year)
		self.dorder = None
		self.team_names = None





# Reads in CSV file of predraft/season ranks
	def get_ranks(self, year):
		return pd.read_csv(f'data/pre_draft_rank/espn_rankings_{year}.csv')
		

# Creates the number of teams in the league from specified number
# Default is the minium which is set to 8
	def create_teams(self, num=8):
		self.num_teams = num
		for n in range(num):
			self.league[f'team{n+1}'] = team.ffTeam(f'team{n+1}')
		self.team_names = list(self.league.keys())

# Returns the team names in the league
	def get_teamnames(self):
		return self.team_names

# Returns number of teams in the league
	def get_numteams(self):
		return self.num_teams

	def view_rosters(self):
		for key, values in self.league.items():
			print(f'This is team {key}: ')
			print(f'{values.get_roster()}')
			print()

	def get_teams(self):
		return self.league

# Sets draft order, can set it manually or randomly choose
# MUST KNOW DRAFT NAMES! accepts order as list
	def set_draftorder(self, custom=False, **kwargs):
		if custom:
			self.dorder = kwargs['order']
		else:
			self.dorder = list()
			temp = list(self.league.keys())
			while len(self.dorder) != self.num_teams:
				pick = rand.choice(temp)
				self.dorder.append(pick)
				temp.pop(temp.index(pick))

# For now this is hardcoded to the below picks
# I should code up something to help with picking the picks
	def draft(self):
		picks = ['WR','WR', 'WR', 'WR', 'RB', 'RB', 'RB', 'RB', 'QB',
				'QB', 'TE', 'TE', 'K', 'K',
				'DST', 'DST']

		for pi in picks:
			for t in range(len(self.dorder)):
				team = self.dorder[t]

				pick = self.rankings[self.rankings['pos'] == pi]
				pick = pick[pick['rank'] == pick['rank'].min()]
				self.league[team].add_roster(p.ffPlayer(pick['player'].iloc[0], pick['pos'].iloc[0], pick['team'].iloc[0], pick['rank'].iloc[0]))
				self.rankings.drop(pick.index, inplace=True)


	def complete_draft(self):
		for key in self.league.keys():
			if not self.league[key].is_rosterfull():
				return False
		return True

















