#adapted from http://savvastjortjoglou.com/nba-draft-part01-scraping.html
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


#Scrape the draft data from BBRef
url = "http://www.basketball-reference.com/draft/NBA_2016.html"

#Retrieve the HTML
html = urlopen(url)

#Make a BS object
soup = BeautifulSoup(html,"html.parser") #Need to also pass html parser

#Extract header information
column_headers = [th.getText() for th in 
                  soup.findAll('tr', limit=2)[1].findAll('th')]

data_rows = soup.findAll('tr')[2:]

#Extract Player Data
player_data = []  # create an empty list to hold all the data

for i in range(len(data_rows)):
    player_row = []  

    for td in data_rows[i].findAll('td'):
        player_row.append(td.getText())        

    player_data.append(player_row)

#Fixed assertion error
column_headers.remove(column_headers[0])

#Load data into dataframe
df = pd.DataFrame(player_data, columns=column_headers)

#Remove Null Values
df = df[df.Player.notnull()]

#Rename the columns because of the % and / identifiers 
df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)

df.columns = df.columns.str.replace('%', '_Perc')

#Differentiate the per game stats
df.columns.values[14:18] = [df.columns.values[14:18][col] +
							"_per_G" for col in range(4)]

#Convert values to correct type
df = df.convert_objects(convert_numeric=True)

#Replace NaNs (i.e. players who accumulated no stats) with zeroes.
df = df[:].fillna(0)

df.loc[:,'Yrs':'AST'] = df.loc[:,'Yrs':'AST'].astype(int)

df.insert(0, 'Draft_Yr', 2016)  

#Export data to CSV file
df.to_csv("draft_data_2016.csv")









