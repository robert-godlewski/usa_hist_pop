# List of useful variables used in multiple files
from selenium.webdriver import Chrome #, Firefox

main_db = 'db.sqlite'
temp_db = 'tempdb.sqlite'

driver = Chrome()
# driver = Firefox()
baseUrl = 'https://en.wikipedia.org'
usaRegionsUrl = baseUrl + '/wiki/List_of_U.S._states_and_territories_by_historical_population'

ADMIT_TITLE = 'Admitted[d]'
