import pandas as pd
import os
import re
import numpy as np

#get current working directory
path = os.getcwd()

#concatenate json files
df1 = pd.read_json(os.path.join('data', '2022_data.json'))
df2 = pd.read_json(os.path.join('data', '2021_data.json'))
df3 = pd.read_json(os.path.join('data', '2020_data.json'))
df4 = pd.read_json(os.path.join('data', '2019_data.json'))

frames = [df1, df2, df3, df4]
result1 = pd.concat(frames)
result2 = result1.groupby('team').aggregate(['sum'])
result2.columns = ['total_commits_sum', 'five_star_sum', 'four_star_sum', 'three_star_sum']
result2['blue_chip'] = result2['five_star_sum'] + result2['four_star_sum']
result2['blue_chip_ratio'] = result2['blue_chip']/result2['total_commits_sum']
result2 = result2.sort_values(by='blue_chip_ratio', ascending=False)
result2.columns = ['Total Commits', '5-Star total', '4-Star total', '3-Star total', 'Blue Chips Total', '2022 Blue Chip Ratio']
result = result2['2022 Blue Chip Ratio']
print(result)
#path=r'C:\Users\carandangc\Desktop\testscrape\'
#path = os.getcwd()
#result.to_csv(os.path.join('data', '2021_blue_chip_ratio.csv'))
