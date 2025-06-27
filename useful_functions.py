# List of useful functions to help configure data
import sqlite3
import re
import json
import pandas

def removeBrackets(data: str) -> str:
    # also removes the garbage within the []
    temp = re.sub(r'\[.*?\]', '', data)
    return temp.rstrip() # removes the whitespace after temp

def addCensusTable(table: pandas.DataFrame, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    admit_title = 'Admitted[d]'
    if admit_title in table.columns:
        has_admit = True
    else:
        has_admit = False
    for index, row in table.iterrows():
        name = table.at[row, 'Name']
        if '[' in name:
            name = removeBrackets(name)
        cur.execute("SELECT * FROM locations WHERE name = ? ", (name,))
        location_raw = cur.fetchone()[0]
        location = json.loads(location_raw)
        if has_admit and 'admitted' in location:
            if 'id' in location and location['admitted'] is None:
                admit_raw = table.at[row, admit_title]
                if admit_raw:
                    admitted = int(admit_raw)
                else:
                    admitted = 1776 # Historical formation of USA
                cur.execute("UPDATE locations SET admitted = ? WHERE id = ? ", (admitted, location['id'],))
                con.commit()
        for col_name, value in row.items():
            if col_name is not 'Name' and col_name is not admit_title:
                if '[' in col_name:
                    year_raw = removeBrackets(col_name)
                    year = int(year_raw)
                else:
                    year = int(col_name)
                if type(value) is float:
                    pop = int(value)
                elif type(value) is str:
                    if '[' in value:
                        temp = removeBrackets(value)
                        cleantemp = temp.replace(',', '')
                        pop = int(cleantemp)
                    else:
                        pop = int(value)
                elif type(value) is None:
                    pop = 0
                cur.execute("INSERT OR IGNORE INTO census (year, population, location_id) VALUES ( ?, ?, ?)", (year, pop, location['id'],))
                con.commit()
