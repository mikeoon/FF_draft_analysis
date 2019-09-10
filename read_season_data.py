import pandas as pd



# This function reads in csv from a Season wnd which weeks
# returns a dictionary with keys by week, ex: 'wk1', and values of pandas dataframes
# Pandas DataFrame has player, team, position, points for that week
def read_in_season_points(season, weeks=17):
	season_data = {}

	for w in range(1, weeks+1):
		week = pd.read_csv(f'data/points_20{season}/wk{w}_points.csv')
		week.drop(columns=['Rank', 'Avg', 'Games'], inplace=True)
		season_data[f'w{w}'] = week

	return season_data






























