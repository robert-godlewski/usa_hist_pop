import sqlite3
import pandas

from useful_variables import driver, usaRegionsUrl

# Get the tables from wikipedia
driver.get(usaRegionsUrl)
html = driver.page_source
tables = pandas.read_html(html)
driver.quit()

con = sqlite3.connect('tempdb.sqlite')
cur = con.cursor()


# Save the tables temporarily into a sql db
i = 1
for table in tables:
    print(table)
    print(table.info(verbose=False))
    table.to_sql(name=f'temp_data{i}', con=con, if_exists='append', index=False)
    i+=1

print("Saved raw tables")
