# Description
Tracking the population of each region of the USA over time based off of census data since the first one in 1790 to 2020.

# Commands
Generally run this program as a CLI within the computer terminal.

## Creating an environment
To create the environment for the first time just run the following in the terminal: % `bash createenv.sh`

This will also create a database as well.

## To Scrape
Run the following to scrape data from wikipedia: % `bash scrape.sh`

> Warning: This just runs wikiscraper.py and not the tables!

> Note: will need to fix this so that you will need to choose between collecting links or data in tables to save to the db.

# References
* [Selenium Documentation](https://www.selenium.dev/documentation/)
* [NumPy Documentation](https://numpy.org/doc/stable/)
* [Pandas Documentation](https://pandas.pydata.org/docs/)
* [SQLite Documentation](https://sqlite.org/lang.html)
* [Wikipedia Data Scraped from](https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_historical_population)
* [Markdown Guide](https://www.markdownguide.org/cheat-sheet/)
* https://www.youtube.com/watch?v=jdj6IC7Pi0I&ab_channel=NeroplusIT
