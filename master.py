import numpy as np
import pandas as pd
import src.batch_season as bseason

# Batch seasons here
bseason.sim_seasons(18, 'custom_draft', num_sim=1000)

# read in stats from simmed season
a = pd.read_csv('data/season_sim_18/sim_custom_draft.csv', index_col=0)

grouped = a.groupby('team')
grouped = grouped.sum()

grouped['win_percentage'] = grouped['W'] / (grouped['L'] + grouped['W'] + grouped['T'])

