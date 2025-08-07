import sqlite3

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from useful_functions import cleanData
from useful_variables import main_db, driver, usaRegionsUrl

def scrapeLinks(xpath: str, driver: Chrome, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None: 
    # Retrives the data from each column with a link
    element = driver.find_element(by=By.XPATH, value=xpath)
    link = element.get_attribute('href')
    region = element.get_attribute('title')
    print('Unformatted region:', region)
    region = cleanData(region)
    # Special cases specific to USA
    if ', D.C.' in region: # American Capital
        region = 'District of Columbia'
    if 'Swan Islands,' in region: # Old territory now part of Honduras
        region = 'Swan Islands'
    print('Formatted region:', region)
    print('Link:', link)
    try:
        cur.execute("SELECT name, url FROM locations WHERE ( name, url ) AS ( ?, ? )", (region, link,))
        print("Already have this in db.")
    except:
        cur.execute("INSERT OR IGNORE INTO locations (name, url) VALUES ( ?, ? )", (region, link,))
        print('Added in new data.')
    finally:
        con.commit()

def convertTable(table: dict, driver: Chrome, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    # Goes through each table to retrieve all of the links to save to db
    r = 1
    while r <= table['regions']:
        xpath = f"{table['xpath_base']}/tbody/tr[{r}]/td/a"
        scrapeLinks(xpath, driver, con, cur)
        r += 1


if __name__ == '__main__':
    con = sqlite3.connect(main_db)
    cur = con.cursor()
    driver.get(usaRegionsUrl)

    tables = [
        {
            # For the current regions in the USA with significan populations (1-57)
            "regions": 57,
            "xpath_base": "//table[@class='wikitable sortable sticky-header sort-under col1left col2center jquery-tablesorter']",
        },
        {
            # Minor Islands and former territories' populations (1-14)
            "regions": 14,
            "xpath_base": "//table[@class='wikitable sortable sort-under col1left col2center jquery-tablesorter']"
        },
    ]

    for table in tables:
        convertTable(table, driver, con, cur)

    driver.quit()
    print('Found Data')

    con.close()
    print('Saved Data')
