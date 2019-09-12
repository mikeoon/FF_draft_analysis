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
		self.lineups= {}
		self.full = False
		self.wins = 0
		self.losses = 0
		self.total_points = 0
		self.standing = None
		self.week_score = {}
		self.injury = []
		self.byes = {}

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


# Adds a ffPlayer to the team's roster
# Updates the teams tracker, count, and byes
	def add_roster(self, player):
		flex_pos = ['WR', 'RB', 'TE']
		pos = player.get_pos()
		if not self.is_posfull(pos):
			self.tracker[pos] -= 1
		elif pos in flex_pos and not self.is_posfull('FLEX'): 
			self.tracker['FLEX'] -= 1

		self.roster[pos].append(player)
		player.set_ffteam(self.name)
		self.byes[player.get_bye()] = player.get_name()

# Drops player from roster, so far for just injury
	def drop_player(self, player):
		self.tracker[player.get_pos()] += 1
		self.count[player.get_pos()] -= 1
		self.injury.append(player)
		self.roster[player.get_pos()].remove(player)


# Returns player from the roster, best available
	def get_player(self, pos, bye=False):
		slot = self.count[pos]
		if bye:
			self.count[pos]+=1
			return self.roster[pos][slot]
		else:
			return self.roster[pos][slot]
			self.count[pos]+=1
		
	def clear_count(self):
		self.count ={'WR': 0, 'RB': 0, 
					'QB' : 0, 'TE' : 0, 
					'DST' : 0, 'K': 0}

# Saves the lineup for that week, key=wkx, value=list of players
	def record_lineup(self, lineup, wk):
		self.lineups[f'wk{wk}'] = lineup

# Returns the lineups for all weeks
	def get_lineups(self):
		for values in self.lineups.values():
			return [v.get_name() for v in values]

# Returns if the roster is full, True = full
	def is_rosterfull(self):
		return(sum(self.tracker.values()) == 0)

# Returns if the pos is filled for this team, True = filled
	def is_posfull(self, pos):
		return self.tracker[pos] == 0

# Returns number of wins for team
	def get_wins(self):
		return self.wins

# Adds a win for the team
	def add_win(self):
		self.wins+=1

# Returns number of losses for team
	def get_losses(self):
		return self.losses

# Adds loss for the team
	def add_loss(self):
		self.wins+=1

# Returns total points scored for the team
	def get_totalpoints(self):
		return sum(self.week_score.values())

# Returns points for that week
	def get_weekscore(self):
		return self.week_score
		
# Sets the score for the given week
	def set_weekscore(self, score,  wk):
		self.week_score[f'wk{wk}'] = score

# Returns the standing of the team
	def get_standing(self):
		return self.standing

# Returns the names of those replaced, hopefully by injury
	def get_injuries(self):
		return [i.get_name() for i in self.injury]

	def get_byes(self):
		return self.byes

# Returns the players on bye for that week. If none, returns None
	def get_weekbye(self, wk):
		if wk in self.byes.keys():
			return self.byes[wk]
		else:
			return None



















