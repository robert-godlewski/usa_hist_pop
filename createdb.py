import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Setting basic information for the basic information of the administrative division
# name = what it's called
# url = wiki link
# title = State/Territory/Country - added in later
# admitted = the year it was formed,
# disestablished = the year it was removed
cur.execute('''
CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            title TEXT,
            admitted INTEGER,
            disestableshed INTEGER
)''')
con.commit()

# Representing connections between location a with location b over time
cur.execute('''
CREATE TABLE IF NOT EXISTS location_relations (
            id INTEGER PRIMARY KEY,
            relation TEXT,
            location_a_id REFERENCES locations (id),
            location_b_id REFERENCES locations (id)
)''')
con.commit()

# Setting basic census data linking up to locations via location_id
cur.execute('''
CREATE TABLE IF NOT EXISTS census (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            population INTEGER,
            location_id REFERENCES locations (id)
)''')
con.commit()

con.close()
print('Saved Data')
