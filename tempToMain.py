# Migrates the data from tempdb to db in the proper areas.
# We scrapped all of the tables from the main link
import sqlite3

from useful_variables import temp_db #, main_db
from useful_functions import getTempData, setUpData

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
    # Setting it up the data
    raw_data = getTempData(table, i, cur_temp)
    # Populating data or ending the loop
    if raw_data:
        data = setUpData(table, raw_data)
    else:
        is_converting = False
    print(data)
    # Adding in the final results in the table to add into the main DB
    if data:
        if data['name'] not in table_raw_data:
            table_raw_data[data['name']] = data
    i += 1

con_temp.close()
print("final table", table_raw_data)

# Need to save the data to the main db
