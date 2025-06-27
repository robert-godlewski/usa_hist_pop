import sqlite3
import pandas

from selenium import webdriver
from selenium.webdriver.common.by import By

from useful_functions import removeBrackets, addCensusTable

driver = webdriver.Chrome()
baseUrl = 'https://en.wikipedia.org'
url = baseUrl + '/wiki/List_of_U.S._states_and_territories_by_historical_population'

driver.get(url)

# Scraping Links
#elements = driver.find_element(by=By.TAG_NAME, value="table")
elementBaseXPath = "//table[@class='wikitable sortable sticky-header short-under col1left col2center jquery-tablesorter']/tbody/tr/td/a"
elements = driver.find_elements(by=By.XPATH, value=elementBaseXPath)
regions = []
links = []
for element in elements:
    regions.append(element.get_attribute('title'))
    links.append(element.get_attribute('href'))
print('Regions:', regions)
print('Links:', links)

# Below refers to XPaths for other tables that we might need
# Skipping the first one because that's the enslaved population from 1790 to 1860
"//table[@class='wikitable sortable sticky-header short-under col1left jquery-tablesorter'][2]"
# and
"//table[@class='wikitable sortable sticky-header short-under col1left jquery-tablesorter'][3]"

# Scraping Tables
html = driver.page_source

tables = pandas.read_html(html)

driver.quit()

# From this we want to save tables 0, 2, and 3 only
for table in tables:
    print(table)

print('Found Data')

# We need to add tables[0], tables[2], and tables[3], regions, and links into a db
con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Setting basic information for the basic information of the administrative division
# name = what it's called
# url = wiki link
# title = State/Territory/Country - added in later
# admitted = the year it was formed
cur.execute('''
CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            title TEXT,
            admitted INTEGER
)''')
con.commit()

# Adding in the region and link to existing table
i = 0
while i < len(regions) and i < len(links):
    print('Unformated region:', regions[i])
    if '[' in regions[i]:
        regions[i] = removeBrackets(regions[i])
    print('Formatted region:', regions[i])
    cur.execute("INSERT OR IGNORE INTO locations (name, url) VALUES ( ?, ? )", (regions[i], links[i],))
    con.commit()
    i += 1

# Setting basic census data linking up to locations via location_id
cur.execute('''
CREATE TABLE IF NOT EXISTS census (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            population INTEGER,
            location_id REFERENCES locations (id) ON DELETE CASCADE
)''')
con.commit()

# Now adding in more data from the tables
t = 0
while t < 4: # We only need tables 0, 2, and 3. Tables 1 and 4+ are irrelevant
    if t == 0 or t == 2 or t == 3:
        addCensusTable(tables[t], con, cur)
    t += 1

# for table in tables: # This is the simple way but doesn't clean the data
#     table.to_sql('locations', con, if_exists='append', index=False) # 'locations' is the table in SQLite DB
con.close()
print('Saved Data')
