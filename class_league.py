import numpy as np
import pandas as pd
import random as rand
import class_team as team
import class_pos as p
import copy


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
		return pd.read_csv(f'data/pre_draft_rank/espn_rankings_{year}_BYE.csv')

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
		snake = False
		for pi in picks:
			if snake == True:
				for t in reversed(range(len(self.dorder))):
					team = self.dorder[t]

					pick = self.rankings[self.rankings['pos'] == pi]
					pick = pick[pick['rank'] == pick['rank'].min()]
					self.league[team].add_roster(p.ffPlayer(pick['player'].iloc[0], pick['pos'].iloc[0], pick['team'].iloc[0], 
															pick['rank'].iloc[0], pick['bye'].iloc[0]))
					self.rankings.drop(pick.index, inplace=True)
				snake=False
			elif snake == False:
				for t in range(len(self.dorder)):
					team = self.dorder[t]

					pick = self.rankings[self.rankings['pos'] == pi]
					pick = pick[pick['rank'] == pick['rank'].min()]
					self.league[team].add_roster(p.ffPlayer(pick['player'].iloc[0], pick['pos'].iloc[0], pick['team'].iloc[0], 
															pick['rank'].iloc[0], pick['bye'].iloc[0]))
					self.rankings.drop(pick.index, inplace=True)
				snake=True


# Checks to see if draft is complete, True = Complete, all team rosters full
	def complete_draft(self):
		for key in self.league.keys():
			if not self.league[key].is_rosterfull():
				return False
		return True

# Returns a list of standings, not ordered
	def get_standings(self):
		win_totals = {}
		stnd_results = []
		empty_row = {'team':None, 'W':None, 'L':None, 'T':None}
		for team, record in self.standings.items():
			new_row = copy.copy(empty_row)
			new_row['team'] = team
			new_row['W'] = record[0]
			new_row['L'] = record[1]
			new_row['T'] = record[2]
			stnd_results.append(new_row)
		return pd.DataFrame(stnd_results).sort_values('W', ascending=False)

	def get_records(self):
		return [(team, record) for team,record in self.standings.items()]


	def get_pttotals(self):
		totals = []
		for team, roster in self.league.items():
			totals.append((team, roster.get_totalpoints()))
		return totals

# Sims 1 matchup, pass in the matchups via two lists
	def sim_matchup(self, div1, div2, wk):
	# Hard coded to just take in a player off the top, no algorithm for it yet
		for a, b in zip(div1, div2):
			a_score, b_score = 0, 0
			a_roster, b_roster = [], []
			a_bye = self.league[a].get_weekbye(wk)
			b_bye = self.league[b].get_weekbye(wk)

			for pos in self.starting:
				pa = self.league[a].get_player(pos)
				pb = self.league[b].get_player(pos)
				

				# Check to see if player is on bye
				if a_bye is not None:
					if pa.get_name() in a_bye:
						pa = self.league[a].get_player(pos, True)

				if b_bye is not None:
					if pb.get_name() in b_bye:
						pb = self.league[b].get_player(pos, True)

				week = self.ppts[f'w{wk}']

				pas = week[week['Player'] == pa.get_name()]
				pbs = week[week['Player'] == pb.get_name()]

				# Do i need this?
				if pa.get_name() in a_roster:
						pa = self.league[a].get_player(pos, False)
						pas = week[week['Player'] == pa.get_name()]

				# Do i need this?
				if pb.get_name() in b_roster:
					pb = self.league[b].get_player(pos, False)
					pbs = week[week['Player'] == pb.get_name()]

				if pas['Player'].count() == 0 and pbs['Player'].count() != 0:
					a_pos_score, b_pos_score = 0, pbs['Points'].iloc[0]
				elif pbs['Player'].count() == 0 and pas['Player'].count() != 0:
					b_pos_score, a_pos_score = 0, pas['Points'].iloc[0]
				elif pbs['Player'].count() == 0 and pas['Player'].count() == 0:
					a_pos_score, b_pos_score = 0, 0
				else:
					a_pos_score, b_pos_score = pas['Points'].iloc[0], pbs['Points'].iloc[0]

				a_score, b_score = a_score + a_pos_score, b_score + b_pos_score
				
			# Creating roster to save for the teams per matchup
				a_roster.append((pa.get_name(), a_pos_score))
				b_roster.append((pb.get_name(), b_pos_score))

			# Tracking point totals for that player
				pa.add_points(a_pos_score)
				pb.add_points(b_pos_score)



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

			self.league[a].clear_count()
			self.league[b].clear_count()


		


# Reads in preaseason ranking data
	def read_in_season_points(self, season, weeks=17):
		season_data = {}

		for w in range(1, weeks+1):
			week = pd.read_csv(f'data/points_20{season}/wk{w}_points.csv')
			week.drop(columns=['Rank', 'Avg', 'Games'], inplace=True)
			season_data[f'w{w}'] = week

		return season_data	

# This is extremely broken, not working yet
	def replace_player(self, player, team):
		pick = self.rankings[self.rankings['pos'] == player.get_pos()]
		replace = pick[pick['rank'] == pick['rank'].min()]
		

		self.league[team].add_roster(p.ffPlayer(replace['player'].iloc[0], replace['pos'].iloc[0], replace['team'].iloc[0],
												replace['rank'].iloc[0], replace['bye'].iloc[0]))
		self.rankings = self.rankings.append(pd.Series({'player' : player.get_name(),'pos' : player.get_pos(), 'team':player.get_team(),'rank':player.get_rank(),'bye':player.get_bye()}, name='rank') )
		self.rankings = self.rankings.drop(replace.index)


	def report_replaced(self):
		report = []
		for team, roster in self.league.items():
			inj = roster.get_injuries()
			report.append(f'{team} replaced {inj}')
		return report

	def get_byes(self):
		byes = []
		for team, roster in self.league.items():
			byes.append((team, roster.get_byes()))
		return byes




















