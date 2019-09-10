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
		self.year = int(year)
		self.ppts = self.read_in_season_points(year)
		self.starting = ['QB', 'WR', 'WR', 'RB', 'RB', 'TE', 'DST', 'K']
		# Standings are in form [W, L, T]
		self.standings = None





# Reads in CSV file of predraft/season ranks
	def get_ranks(self, year):
		return pd.read_csv(f'data/pre_draft_rank/espn_rankings_{year}.csv')
		

# Creates the number of teams in the league from specified number
# Default is the minium which is set to 8
	def create_teams(self, num=8):
		self.num_teams = num
		self.standings = {}
		for n in range(num):
			self.league[f'team{n+1}'] = team.ffTeam(f'team{n+1}')
			self.standings[f'team{n+1}'] = [0, 0, 0]
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

# Checks to see if draft is complete, True = Complete, all team rosters full
	def complete_draft(self):
		for key in self.league.keys():
			if not self.league[key].is_rosterfull():
				return False
		return True

# Returns a list of standings, not ordered
	def get_standings(self):
		return [(team, record) for team, record in self.standings.items()]


# Sims 1 matchup, pass in the matchups via two lists
	def sim_matchup(self, div1, div2, wk):
		
		# just for one week
		# Hard coded to just take in a player off the top, no algorithm for it yet
		for a, b in zip(div1, div2):
			a_score, b_score = 0, 0
			a_roster, b_roster = [], []

			for pos in self.starting:

				pa = self.league[a].get_player(pos)
				pb = self.league[b].get_player(pos)

				week = self.ppts[f'w{wk}']

				pas = week[week['Player'] == pa.get_name()]
				pbs = week[week['Player'] == pb.get_name()]

				print(pa)
				print(pb)
				if pas['Player'].count() == 0 or pa.get_name() in a_roster:
					pa = self.league[a].get_player(pos, False)
					pas = week[week['Player'] == pa.get_name()]

				if pbs['Player'].count() == 0 or pb.get_name() in b_roster:
					pb = self.league[b].get_player(pos, False)
					pbs = week[week['Player'] == pb.get_name()]

				print(pa)
				print(pb)
				print()
				a_score, b_score = a_score + pas['Points'].iloc[0], b_score + pbs['Points'].iloc[0]
				
			# Creating roster to save for the teams per matchup
				a_roster.append((pas['Player'].iloc[0], pas['Points'].iloc[0]))
				b_roster.append((pbs['Player'].iloc[0], pbs['Points'].iloc[0]))

			# Tracking point totals for that player
				pa.add_points(pas['Points'].iloc[0])
				pb.add_points(pbs['Points'].iloc[0])


		# Right now, hard coded to favor team B if the sores are equal
			if a_score > b_score:
				self.league[a].add_win()
				self.standings[a][0] += 1
				self.standings[b][1] += 1
				winner = a
			else:
				self.league[b].add_win()
				self.standings[a][1] += 1
				self.standings[b][0] += 1
				winner = b


		# Sets the score for that week within the team
			self.league[a].set_weekscore(a_score, wk)
			self.league[b].set_weekscore(b_score, wk)

		# Sets the roster for that week within the team
			self.league[a].record_lineup(a_roster, wk)
			self.league[b].record_lineup(b_roster, wk)

		# Clear team's counts so it can count for another matchup
			self.league[a].clear_count()
			self.league[b].clear_count()

		# Helper print messages to see one matchup
		# Delete when running through them all
		'''
			print(f'This is {a} vs {b}')
			print(f'{a}')
			print(f'Score: {a_score}')
			print(f'Lineup: {a_roster}')
			print()
			print(f'{b}')
			print(f'Score: {b_score}')
			print(f'Lineup: {b_roster}')
			print(f'Winner is: {winner}')
			print()
		'''


		


# Reads in preaseason ranking data
	def read_in_season_points(self, season, weeks=17):
		season_data = {}

		for w in range(1, weeks+1):
			week = pd.read_csv(f'data/points_20{season}/wk{w}_points.csv')
			week.drop(columns=['Rank', 'Avg', 'Games'], inplace=True)
			season_data[f'w{w}'] = week

		return season_data	





















