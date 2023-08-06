import pandas as pd

fpath = '../data/10yrCMrate.csv'

df = pd.read_csv(fpath)

print(df.head())