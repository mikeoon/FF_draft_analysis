import numpy as np

# Creates each team, only needs the team name to initialize
# Keeps track of how full the roster is and what positions you have
# Also has total points, current standings, and points for the week

class ffTeam():

	def __init__(self, name):
		self.name = name
		self.tracker={'WR': 3, 'RB': 3, 
					'QB' : 2, 'TE' : 2, 
					'DST' : 2, 'K': 2,
					'FLEX' : 2}
		self.count={'WR': 0, 'RB': 0, 
					'QB' : 0, 'TE' : 0, 
					'DST' : 0, 'K': 0}
		self.roster = {'WR': [], 'RB': [], 
					'QB' : [], 'TE' : [], 
					'DST' : [], 'K': []}
		self.full = False
		self.wins = 0
		self.losses = 0
		self.total_points = 0
		self.standing = None
		self.week_score = None

# Returns name of team
	def get_name(self):
		return self.name

# Sets the name of the team
	def set_name(self, name):
		self.name = name

# Returns a readable, printable list of players for each position
	def get_roster(self):
		readable_roster = {}
		for key, values in self.roster.items():
			readable_roster[key] = [str(v) for v in values]
		return readable_roster
			
# Returns how many players are on the roster
	def get_rostercount(self):
		return sum(self.count.values())

# Adds a ffPlayer to the team's roster
# Updates the teams tracker and count
	def add_roster(self, player):
		flex_pos = ['WR', 'RB', 'TE']
		pos = player.get_pos()
		if not self.is_posfull(pos):
			self.tracker[pos] -= 1
		elif pos in flex_pos and not self.is_posfull('FLEX'): 
			self.tracker['FLEX'] -= 1

		self.count[pos] += 1

		self.roster[pos].append(player)
		player.set_ffteam(self.name)


	def get_player(self, pos, rankhigh=False):
		if not rankhigh:
			return self.roster[pos][0]
		else:
			for p in self.roster[pos]:
				return(p.get_rank())


# Returns if the roster is full, True = full
	def is_rosterfull(self):
		return(sum(self.tracker.values()) == 0)

# Returns if the pos is filled for this team, True = filled
	def is_posfull(self, pos):
		return self.tracker[pos] == 0

# Returns number of wins for team
	def get_wins(self):
		return self.wins

# Returns number of losses for team
	def get_losses(self):
		return self.losses

# Returns total points scored for the team
	def get_totalpoints(self):
		return self.total_points

# Returns points for that week
	def get_weekscore(self):
		return self.week_score
		
# Returns the standing of the team
	def get_standing(self):
		return self.standing

		























