from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time
from tabulate import tabulate
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains

#launch url
url = "https://247sports.com/season/2022-football/compositeteamrankings/"

# create a new Firefox session
driver = webdriver.Firefox(service_log_path = os.devnull)
driver.implicitly_wait(30)
driver.get(url)

#scroll down and click to load more
for n in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(120)
    try:
    	python_button = driver.find_element_by_partial_link_text('Load')
    except:
    	break
    try:
    	python_button.click() #click link
    except:
    	break

datalist = [] #empty list

#Selenium hands the page source to Beautiful Soup
soup_level1=BeautifulSoup(driver.page_source, "lxml")

table = soup_level1.find_all('li', attrs={'class':'rankings-page__list-item'})

i = 0
for i in range(len(table)):
    try:
        team = table[i].div.a.text.strip()
        if team == '':
            team = table[i].find('div', attrs={'class','team'}).text.strip()
    except:
        team = np.nan
    total_commits = table[i].find('div', attrs={'class','total'}).text.split()[0]
    five_star = table[i].ul.text.split()[1]
    four_star = table[i].ul.text.split()[3]
    try:
        three_star = table[i].ul.text.split()[5]
    except:
        three_star = np.nan
    datalist.append((team, total_commits, five_star, four_star, three_star))

#end the Selenium browser session
driver.quit()

#combine all pandas dataframes in the list into one big dataframe
result = pd.DataFrame(datalist, columns=['team', 'total_commits', 'five_star', 'four_star', 'three_star'])

#convert the pandas dataframe to JSON
json_records = result.to_json(orient='records')

#pretty print to CLI with tabulate
#converts to an ascii table
print(tabulate(result, headers=['team', 'total_commits', 'five_star', 'four_star', 'three_star'],tablefmt='psql'))

#get current working directory
path = os.getcwd()

#open, write, and close the file
f = open(os.path.join('data', '2022_data.json'), "w")
f.write(json_records)
f.close()