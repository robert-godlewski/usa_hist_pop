# import sqlite3
import pandas

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
baseUrl = 'https://en.wikipedia.org'
url = 'https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_historical_population'

driver.get(url)

# Need to narrow down here
#elements = driver.find_element(by=By.TAG_NAME, value="table")
elementBaseXPath = "//table[@class='wikitable sortable sticky-header short-under col1left col2center jquery-tablesorter']/tbody/tr/td/a"
elements = driver.find_elements(by=By.XPATH, value=elementBaseXPath)
regions = []
links = []
for element in elements:
    regions.append(element.get_attribute('title'))
    links.append(element.get_attribute('href'))
print(regions)
print(links)

# Below refers to XPaths for other tables that we might need
# Skipping the first one because that's the enslaved population from 1790 to 1860
"//table[@class='wikitable sortable sticky-header short-under col1left jquery-tablesorter'][2]"
# and
"//table[@class='wikitable sortable sticky-header short-under col1left jquery-tablesorter'][3]"

# Need to do more things here like saving the links for each region
html = driver.page_source

tables = pandas.read_html(html)

driver.quit()

# From this we want to save tables 0, 2, and 3 only
for table in tables:
    print(table)

# Merge tables 0, 2, 3 with https://pandas.pydata.org/docs/user_guide/merging.html prior to adding it to the db.

# We need to add tables[0], tables[2], and tables[3], regions, and links into a db
# con = sqlite3.connect('db.sqlite')
# for table in tables: # Fix this so tat only tables 0, 2, and 3 are added in
#     table.to_sql('locations', con, if_exists='append', index=False) # 'locations' is the table in SQLite DB
# con.close()

# We might need to do this with the pandas data before adding it to the db
# import pandas as pd

# # Sample DataFrame with messy data
# data = {'Name': ['Alice', 'Bob', 'Charlie', 'Alice', 'David'],
#         'Age': [25, 30, None, 25, 40],
#         'City': ['New York', 'London', 'new york', 'Paris', 'London'],
#         'Salary': ['50,000', '60000', '75,000', '50000', '80,000']}
# df = pd.DataFrame(data)

# # 1. Fill missing 'Age' with the mean
# df['Age'].fillna(df['Age'].mean(), inplace=True)

# # 2. Remove duplicate rows
# df.drop_duplicates(inplace=True)

# # 3. Standardize 'City' column to title case
# df['City'] = df['City'].str.title()

# # 4. Clean 'Salary' column and convert to integer
# df['Salary'] = df['Salary'].str.replace(',', '').astype(int)

# print(df)
