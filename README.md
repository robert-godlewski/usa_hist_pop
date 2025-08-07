# Description
Tracking the population of each region of the USA over time based off of census data since the first one in 1790 to 2020.

> Note: the python files are within the py_files directory.

# DB layout
This project saves the data to a sqlite database to temporarily save the data to constantly refer to.

## Locations
This table has the basic information for each general "region" within the USA.

Column data:
* id: Foreign Key
* name: What the region is called
* url: url link to refer to
* title: Country/ State/ Territory
* admitted: Year added into the USA
* disestablished: Year removed from the USA

# Commands
Generally run this program as a CLI within the computer terminal.

## Creating an environment
To create the environment for the first time just run the following in the terminal: % `bash createenv.sh`

This will also create a database as well.

### To manually create a new db
Generally don't need to run this command at all in your CLI because it's done when creating a new environment.
However, if you need to reestablish the main db for some reason then run the following in the terminal: % `bash createdb.sh`

## To Scrape
> Warning: When scraping you can only run one script at a time so that you don't get blocked by the [MediaWikiAPI](https://www.mediawiki.org/wiki/API:Main_page) or else you will not get anything except for errors for 24 hours!

Run the following to scrape data from wikipedia: % `bash scrape.sh`

> Warning: This just no longer works and needs to be fixed!

> Note: will need to fix this so that you will need to choose between collecting links or data in tables to save to the db.

# References
* [Selenium Documentation](https://www.selenium.dev/documentation/)
* [NumPy Documentation](https://numpy.org/doc/stable/)
* [Pandas Documentation](https://pandas.pydata.org/docs/)
* [SQLite Documentation](https://sqlite.org/lang.html)
* [Wikipedia Data Scraped from](https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_historical_population)
* [Markdown Guide](https://www.markdownguide.org/cheat-sheet/)
* https://www.youtube.com/watch?v=jdj6IC7Pi0I&ab_channel=NeroplusIT
