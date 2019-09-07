import numpy as np

# This creates a FF player
# Makes it easier to distinguish their name, pos, team, rank, 
#and which ff team they are on

class ffPlayer():
	def __init__(self, name, pos, team, rank):
		self.name = name
		self.pos = pos
		self.team = team
		self.rank = rank
		self.ff_team = None

	def get_name(self):
		return self.name

	def get_pos(self):
		return self.pos

	def get_rank(self):
		return self.rank

	def set_ffteam(self, ff_team):
		self.ff_team = ff_team




















