import sqlite3

from useful_functions import scrapeLinks
from useful_variables import driver, usaRegionsUrl

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
driver.get(usaRegionsUrl)

# Scraping Links
# For the current regions in the USA with significan populations (1-57)
r = 1
while r <= 57:
    xpath = f"//table[@class='wikitable sortable sticky-header sort-under col1left col2center jquery-tablesorter']/tbody/tr[{r}]/td/a"
    scrapeLinks(xpath, driver, con, cur)
    r += 1

# Now getting the Minor Islands and former territories' populations (1-14)
t = 1
while t <= 14:
    xpath = f"//table[@class='wikitable sortable sort-under col1left col2center jquery-tablesorter']/tbody/tr[{t}]/td/a"
    scrapeLinks(xpath, driver, con, cur)
    t += 1

driver.quit()
print('Found Data')

con.close()
print('Saved Data')
