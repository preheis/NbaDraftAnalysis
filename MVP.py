#adapted from http://savvastjortjoglou.com/nba-draft-part01-scraping.html
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

#
#Retrieve the data from Basketball Reference
#

#Scrape the draft data from BBRef
url = "https://www.basketball-reference.com/awards/mvp.html"

#Retrieve the HTML
html = urlopen(url)

#Make a BS object
soup = BeautifulSoup(html,"html.parser") #Need to also pass html parser

#Extract header information
column_headers = [th.getText() for th in 
                  soup.findAll('tr', limit=2)[1].findAll('th')]

#Remove season column to get rid of the assertion error
column_headers.remove(column_headers[0])

data_rows = soup.findAll('tr')[2:]

#Extract the player data
player_data = [] 

for i in range(len(data_rows)): 
    player_row = []  

    for td in data_rows[i].findAll('td'):        

        player_row.append(td.getText())        

    player_data.append(player_row)

#Make a dataframe out of the player data
df = pd.DataFrame(player_data, columns=column_headers)

#
#Clean the data we obtained
#

#Rename columns
df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)
df.columns = df.columns.str.replace('%', '_Perc')

#Get rid of ABA players for now
df.drop(df.index[62:],inplace=True)

#Get rid of League, Voting and Team Columns (not necessary)
df.drop('Lg', axis='columns', inplace=True)
df.drop('Voting', axis='columns', inplace=True)
df.drop('Tm', axis='columns', inplace=True)

#Insert the season column back in to the dataframe
df.insert(0, 'Season', range(2016,1954,-1))

#Convert the types
df = df.convert_objects(convert_numeric=True)

#Get rid of the NaNs
df = df[:].fillna(0)

#Save to CSV file
df.to_csv("NBA_MVP.csv")
