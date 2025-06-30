import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Setting basic information for the basic information of the administrative division
# name = what it's called
# url = wiki link
# title = State/Territory/Country - added in later
# admitted = the year it was formed
cur.execute('''
CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            title TEXT,
            admitted INTEGER
)''')
con.commit()

# Setting basic census data linking up to locations via location_id
cur.execute('''
CREATE TABLE IF NOT EXISTS census (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            population INTEGER,
            location_id REFERENCES locations (id) ON DELETE CASCADE
)''')
con.commit()

con.close()
print('Saved Data')
