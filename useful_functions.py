# List of useful functions to help configure data
import sqlite3
import re
# import json
# import pandas

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# from .useful_variables import ADMIT_TITLE - This is causing bugs for some reason?

def removeBrackets(data: str) -> str:
    # also removes the garbage within the []
    temp = re.sub(r'\[.*?\]', '', data)
    return temp.rstrip() # removes the whitespace after temp

def removeParenthesis(data: str) -> str:
    temp = re.sub(r'\(.*?\)', '', data)
    return temp.rstrip()

def largeNumstrToNum(value: str) -> int:
    temp = removeBrackets(value)
    cleantemp = temp.replace(',','') # turns '1,000' to '1000'
    return int(cleantemp)

def scrapeLinks(xpath: str, driver: Chrome, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None: # Will need to test this function later on
    element = driver.find_element(by=By.XPATH, value=xpath)
    link = element.get_attribute('href')
    region = element.get_attribute('title')
    print('Unformatted region:', region)
    if '[' in region:
        region = removeBrackets(region)
    if '(' in region:
        region = removeParenthesis(region)
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

# Fix the functions below
# def addRegionAdmittance(row, location, table: pandas.DataFrame, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
#     if ADMIT_TITLE in table.columns:
#         has_admit = True
#     else:
#         has_admit = False
#     if has_admit and 'id' in location:
#         admit_raw = table.at[row, ADMIT_TITLE]
#         if admit_raw:
#             admitted = int(admit_raw)
#         else:
#             admitted = 1776 # Historical formation of the USA
#         cur.execute("UPDATE locations SET admitted = ? WHERE id = ? ", (admitted, location['id'],))
#         con.commit()

# def saveCensusData(location, value, col_name: str, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
#     if '[' in col_name:
#         year_raw = removeBrackets(col_name)
#         year = int(year_raw)
#     else:
#         year = int(col_name)
#     if type(value) is float:
#         pop = int(value)
#     elif type(value) is str:
#         if '[' in value:
#             pop = largeNumstrToNum(value)
#         else:
#             pop = int(value)
#     elif type(value) is None:
#         pop = 0
#     cur.execute("INSERT OR IGNORE INTO census (year, population, location_id) VALUES ( ?, ?, ? )", (year, pop, location['id'],))
#     con.commit()

# def addCensusTable(table: pandas.DataFrame, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
#     for index, row in table.iterrows():
#         print(f'Index: {index}')
#         print('Row:', row)
#         # print('Name:', table[row]['Name'])
#         name = table.at[row, 'Name'] # This is breaking for some reason - Review https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.at.html#pandas.DataFrame.at
#         if '[' in name:
#             name = removeBrackets(name)
#         cur.execute("SELECT * FROM locations WHERE name = ? ", (name,))
#         location_raw = cur.fetchone()[0]
#         location = json.loads(location_raw)
#         addRegionAdmittance(row, location, table, con, cur)
#         for col_name, value in row.items():
#             if col_name is not 'Name' and col_name != ADMIT_TITLE:
#                 saveCensusData(location, value, col_name, con, cur)
