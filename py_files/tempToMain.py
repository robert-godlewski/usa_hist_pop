# Migrates the data from tempdb to db in the proper areas.
# We scrapped all of the tables from the main link
import sqlite3

from useful_variables import temp_db #, main_db
from useful_functions import cleanData, largeNumstrToNum

def _getTempData(table_name: str, row_index: int, cur: sqlite3.Cursor) -> tuple:
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

def _setUpData(table_name: str, raw_data: tuple) -> dict:
    # convert the information from raw_data pertaining to the table_name to a dictionary
    data = {}
    y = _setYearIndex(table_name)
    if y >= 0:
        data = _processRawData(table_name, raw_data, y, data)
    return data

def processRawTables(table_name: str, cur: sqlite3.Cursor, table_data: dict):
    # adds in the data from the given table to the data
    is_converting = True
    i = 1
    while is_converting:
        print("Working on table:", table_name)
        print("Working on row:", i)
        # Setting it up the data
        raw_data = _getTempData(table_name, i, cur)
        # Populating data or ending the loop
        if raw_data:
            data = _setUpData(table_name, raw_data)
        else:
            is_converting = False
            data = None
        print(data)
        # Adding in the final results in the table to add into the main DB
        if data:
            if data['name'] not in table_data:
                table_data[data['name']] = data
        i += 1


if __name__ == '__main__':
    tables = [
        'temp_data1', # USA region admittance dates with census populations from 1790 to 1860
        # 'temp_data2', # Slave populations in USA from 1790 to 1860
        'temp_data3', # Population in USA from 1870 to 1950
        'temp_data4', # Population in USA from 1960 to 2020
        'temp_data5', # Population in minor USA territories from 1910 to 2000
        # 'temp_data6', # Not sure what this is
        'temp_data7', # USA region admittance and relinquished dates with census populations from 1910 to 1990
        # 'temp_data8' Not useful at all
    ]
    table_raw_data = {}

    con_temp = sqlite3.connect(temp_db)
    cur_temp = con_temp.cursor()

    # This only works with the first table and need to fix it for the others
    # table = tables[0]
    for table in tables:
        processRawTables(table, cur_temp, table_raw_data)

    con_temp.close()
    print("final table:", table_raw_data)

    # Need to save the data to the main db
