import numpy as np

# Creates each team, only needs the team name to initialize
# Keeps track of how full the roster is and what positions you have
# Also has total points, current standings, and points for the week

class team_roster():

	def __init__(self, name):
		self.name = name
		self.tracker={'WR': 3, 'RB': 3, 
					'QB' : 2, 'TE' : 2, 
					'DST' : 2, 'K': 2,
					'FLEX' : 2}
		self.tracker={'WR': 0, 'RB': 0, 
					'QB' : 0, 'TE' : 0, 
					'DST' : 0, 'K': 0}
		self.full = False
		self.roster = list()
		self.wins = 0
		self.losses = 0
		self.total_points = 0
		self.standing = None
		self.week_score = None

	def get_name(self):
		return self.name

	def set_name(self, name):
		self.name = name

	def get_roster(self):
		return self.roster

	def get_rostercount(self):
		return len(self.roster)

	def add_roster(self, player):
		self.roster.append(player)
		pos = player.get_pos
		if self.tracker[pos] != 0:
			self.tracker[pos] -= 1
			self.count[pos] += 1
		else:
			self.tracker['FLEX'] -= 1
		player.set_ffteam(self.name)

	def is_rosterfull(self):
		return(sum(self.tracker.values()) == 0)

	def get_wins(self):
		return self.wins

	def get_losses(self):
		return self.losses

	def get_totalpoints(self):
		return self.total_points

	def get_weekscore(self):
		return self.week_score

	def get_standing(self):
		return self.standing

		






















