import numpy as np

# This creates a FF player
# Makes it easier to distinguish their name, pos, team, rank, 
#and which ff team they are on

class ffPlayer():
	def __init__(self, name, pos, team, rank, bye):
		self.name = name
		self.pos = pos
		self.team = team
		self.rank = rank
		self.bye = bye
		self.ff_team = None
		self.point_total = 0

# Makes player readable, just name
	def __str__(self):
		return f'{self.name}'

# Returns the name of the player
	def get_name(self):
		return self.name

# Returns the position of the player
	def get_pos(self):
		return self.pos

# Returns the rank of that player (Predraft)
	def get_rank(self):
		return self.rank

# Returns what team that player is on
	def set_ffteam(self, ff_team):
		self.ff_team = ff_team

# Adds to player's point total for the season
	def add_points(self, pts):
		self.point_total += pts

# Returns player's point total up to a point
	def get_pointtotal(self):
		return self.point_total

	def get_bye(self):
		return self.bye






















