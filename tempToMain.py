# Migrates the data from tempdb to db in the proper areas.
# We scrapped all of the tables from the main link
import sqlite3

from useful_variables import temp_db #, main_db
from useful_functions import cleanData, largeNumstrToNum

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

# Need to loop through the tables and clean this with new functions
# This only works with the first table and need to fix it for the others
table = tables[0]
is_converting = True
i = 1
while is_converting:
    print("Working on table:", table)
    print("Working on row:", i)
    try:
        cur_temp.execute("SELECT * FROM temp_data1 WHERE ROWID = ( ? )", (i,),)
        raw_data = cur_temp.fetchone()
    except:
        raw_data = None
    # print(type(raw_data))
    print(raw_data)
    if raw_data:
        data = {
            'id': i, # This will need to change
            'name': cleanData(raw_data[0]),
            'census': [{} for _ in range(24)], # 24 because 1790, 1800, ..., 2020
        }
    else:
        data = None
        is_converting = False
    if is_converting and raw_data and data and table is 'temp_data1': # Fix this later
        if raw_data[1]:
            data['admitted'] = int(raw_data[1])
        y = 0 # Census number-1
        d = 2 # index from raw_data tuple
        while d < len(raw_data) and y < 8:
            if raw_data[d]:
                try:
                    pop_raw = cleanData(raw_data[d])
                except:
                    pop_raw = None
                if pop_raw:
                    population = largeNumstrToNum(pop_raw)
                else:
                    population = int(raw_data[d])
                data['census'][y] = {
                    'year': (y*10) + 1790,
                    'population': population
                }
            d += 1
            y += 1
    print(data)
    if data:
        if data['name'] not in table_raw_data:
            table_raw_data[data['name']] = data
    i += 1

con_temp.close()
print(table_raw_data)

# Need to save the data to the main db
