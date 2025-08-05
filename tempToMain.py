# Migrates the data from tempdb to db in the proper areas.
# We scrapped all of the tables from the main link
import sqlite3

from useful_variables import temp_db #, main_db
from useful_functions import cleanData, largeNumstrToNum, getTempData, setUpData

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
    # try:
    #     # cur_temp.execute("SELECT * FROM temp_data1 WHERE ROWID = ( ? )", (i,),)
    #     script = f"SELECT * FROM {table} WHERE ROWID = ( ? )"
    #     cur_temp.execute(script, (i,),)
    #     raw_data = cur_temp.fetchone()
    # except:
    #     raw_data = None
    # print(type(raw_data))
    # print(raw_data)
    # if len(raw_data) > 0:
    #     data = {
    #         # 'id': i, # This will need to change
    #         'name': cleanData(raw_data[0]),
    #         'census': [{} for _ in range(24)], # 24 because 1790, 1800, ..., 2020
    #     }
    # else:
    #     data = None
    #     is_converting = False
    # Populating data or ending the loop
    if len(raw_data) <= 0:
        is_converting = False
    else:
        # Make everything below into a function and fix this whole thing
        data = {}
        d = 0
        data['name'] = cleanData(raw_data[d])
        d += 1
        data['census'] = [{} for _ in range(24)] # 24 for each census 1790 to 2020
        if table == 'temp_data3':
            y = 8 # to y = 16 which is 1870 to 1950
        elif table == 'temp_data4':
            y = 17 # to y = 23 which is 1960 to 2020
        elif raw_data[d]: # might need to fix but this is fine for now
            data['admitted'] = int(raw_data[d])
            d += 1 # d is now 2
            if table == 'temp_data1':
                y = 0 # to y = 7 which is 1790 to 1860
            else: # table is 'temp_data5' or 'temp_data7'
                y = 12 # which is 1910
            if table == 'temp_data7':
                relinquished = cleanData(raw_data[d])
                data['disestablished'] = int(relinquished)
                d += 1 # d is now 3
        else:
            y = None
        # For some reason this loop is not working
        while y and d < len(raw_data):
            if raw_data[d]:
                print(f"{type(raw_data[d])} => {raw_data[d]}")
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
    # Adding in the final results in the table to add into the main DB
    if data:
        if data['name'] not in table_raw_data:
            table_raw_data[data['name']] = data
    i += 1

con_temp.close()
print("final table", table_raw_data)

# Need to save the data to the main db
