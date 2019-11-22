import numpy as np
import pandas as pd
import src.batch_season as bseason

# Batch seasons here
# Only the 2015, 2016, 2018 seasons are working
bseason.sim_seasons(15, 'custom_draft')

# read in stats from simmed season
a = pd.read_csv('data/season_sim_18/sim_custom_draft.csv', index_col=0)

grouped = a.groupby('team')
grouped = grouped.sum()

grouped['win_percentage'] = grouped['W'] / (grouped['L'] + grouped['W'] + grouped['T'])

