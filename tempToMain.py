# Migrates the data from tempdb to db in the proper areas.
# We scrapped all of the tables from the main link
import sqlite3

from useful_variables import temp_db #, main_db
from useful_functions import cleanData #, largeNumstrToNum

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

# Need to loop this for all tables and rows within each table
cur_temp.execute("SELECT * FROM temp_data1 WHERE ROWID = 1")
raw_data = cur_temp.fetchone()
print(type(raw_data)) # This is a tuple
print(raw_data)

name = cleanData(raw_data[0])
data = {
    'id': 1, # This will need to change
    'name': cleanData(raw_data[0]),
    'census': [{} for _ in range(24)], # 24 because 1790, 1800, ..., 2020
}

# Add in more things to do here.

con_temp.close()
