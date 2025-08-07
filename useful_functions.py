# List of useful functions to help configure data
import sqlite3
import re
# import json
# import pandas

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# from .useful_variables import ADMIT_TITLE - This is causing bugs for some reason?

def _removeBrackets(data: str) -> str:
    # also removes the garbage within the []
    temp = re.sub(r'\[.*?\]', '', data)
    return temp.rstrip() # removes the whitespace after temp

def _removeParenthesis(data: str) -> str:
    temp = re.sub(r'\(.*?\)', '', data)
    return temp.rstrip()

def cleanData(data: str) -> str:
    if '[' in data:
        data = _removeBrackets(data)
    if '(' in data:
        data = _removeParenthesis(data)
    return data

def largeNumstrToNum(value: str) -> int:
    temp = cleanData(value)
    cleantemp = temp.replace(',','') # turns '1,000' to '1000'
    return int(cleantemp)

def scrapeLinks(xpath: str, driver: Chrome, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None: # Will need to test this function later on
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

def getTempData(table_name: str, row_index: int, cur: sqlite3.Cursor) -> tuple:
    # Attempts to retrive data from the given table and row in the db
    try:
        # cur_temp.execute("SELECT * FROM temp_data1 WHERE ROWID = ( ? )", (i,),)
        script = f"SELECT * FROM {table_name} WHERE ROWID = ( ? )"
        cur.execute(script, (row_index,),)
        return cur.fetchone()
    except:
        return ()

def _setYearIndex(table_name: str) -> int:
    if table_name == 'temp_data1': # index 0 to 7 is 1790 to 1860
        return 0
    elif table_name == 'temp_data3': # index 8 to 16 is 1870 to 1950
        return 8
    elif table_name == 'temp_data4': # index 17 to 23 is 1960 to 2020
        return 17
    elif table_name == 'temp_data5' or table_name == 'temp_data7': # 1910 is index 12
        return 12
    else:
        return -1

def _addInCensus(raw, yearIndex: int) -> dict:
    try:
        pop_raw = cleanData(raw)
    except:
        pop_raw = None
    if pop_raw:
        pop = largeNumstrToNum(pop_raw)
    elif raw:
        pop = int(raw)
    else:
        return {}
    return {
        'year': (yearIndex*10)+1790,
        'population': pop,
    }

def _processRawData(table_name: str, raw_data: tuple, yearIndex: int, data: dict) -> dict:
    data['census'] = [{} for _ in range(24)] # from census 1790 to 2020
    d = 0
    while d < len(raw_data):
        if d == 0:
            data['name'] = cleanData(raw_data[d])
        elif d == 1 and (table_name == 'temp_data1' or table_name == 'temp_data5' or table_name == 'temp_data7') and raw_data[d]:
            data['admitted'] = int(raw_data[d])
        elif d == 2 and table_name == 'temp_data7' and raw_data[d]:
            relinquished = cleanData(raw_data[d])
            data['disestablished'] = int(relinquished)
        else:
            data['census'][yearIndex] = _addInCensus(raw_data[d], yearIndex)
            yearIndex += 1
        d += 1
    return data

def setUpData(table_name: str, raw_data: tuple) -> dict:
    # convert the information from raw_data pertaining to the table_name to a dictionary
    data = {}
    y = _setYearIndex(table_name)
    if y >= 0:
        data = _processRawData(table_name, raw_data, y, data)
    return data

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
