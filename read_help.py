import pandas as pd
import numpy as np

# helps read in adp csv files
def read_adp_csv(year):
	return pd.read_csv(f'data/std_adp/adp_{year}.csv')



def read_leaders_csv(year):
	return pd.read_csv(f'data/leaders_points/{year}_leaders.csv')
























