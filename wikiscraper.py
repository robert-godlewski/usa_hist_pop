import sqlite3
# import pandas

from selenium.webdriver.common.by import By

from useful_functions import removeBrackets, removeParenthesis #, addCensusTable
from useful_variables import driver, usaRegionsUrl

driver.get(usaRegionsUrl)

# Scraping Links - Fix this to use hash maps instead to add in everything instead of using limits.
elementBaseXPath = "//table/tbody/tr/td/a" # Now collects over 200 which we really don't need all
elements = driver.find_elements(by=By.XPATH, value=elementBaseXPath)
regions = []
links = []
i = 0
while i < 57:
    # This is needed because there are technically only 56 regions within the USA and the USA's population and we only want the first table in this case
    element = elements[i]
    regions.append(element.get_attribute('title'))
    links.append(element.get_attribute('href'))
    i += 1
# print('Regions:', regions)
# print('Links:', links)

# Scraping Tables - Already added this in scrapewikitables.py
# html = driver.page_source
# tables = pandas.read_html(html)

driver.quit()

# From this we want to save tables 0, 2, and 3 only
# for table in tables: print(table)

print('Found Data')

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Adding in the region and link to existing table
i = 0
while i < len(regions) and i < len(links):
    print('Unformated region:', regions[i])
    if '[' in regions[i]:
        regions[i] = removeBrackets(regions[i])
    if '(' in regions[i]:
        regions[i] = removeParenthesis(regions[i])
    if ',' in regions[i]: # This is the USA capital
        regions[i] = 'District of Columbia'
    print('Formatted region:', regions[i])
    cur.execute("INSERT OR IGNORE INTO locations (name, url) VALUES ( ?, ? )", (regions[i], links[i],))
    con.commit()
    i += 1

# Now adding in more data from the tables - Need to migrate everything here to another file to grab data from tempdb.sqlite to db.sqlite
# t = 0
# while t < 4: # We only need tables 0, 2, and 3. Tables 1 and 4+ are irrelevant
#     if t == 0 or t == 2 or t == 3: addCensusTable(tables[t], con, cur)
#     t += 1
con.close()
print('Saved Data')
