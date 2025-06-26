from selenium import webdriver

driver = webdriver.Chrome()
url = 'https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_historical_population'

driver.get(url)

# Need to do more things here

driver.quit()
