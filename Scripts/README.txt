Funcionalities of the seperate Scripts

This project was created to scrape data from football matches in given leagues from serveral seasons.
The scraper should be able to scrape every given season with only one call on the targetwebsite (www.weltfussball.de/...)

SimpleLeagues.py
This script generates the necessary links of each league, that is marked on the speciffic column in the 'Leagues'-table of the google sheet (or in example data in the data folder)
It is only required, that there is an Entry for the Column Starting_at, then the script will run over the whole table and check for a new entry. 
Afterwards it will generate a link for each season starting from the one in the colum until the actual season

SimpleSeason.py
The SimpleSeason-script is the actual scraper, that executes the call from a given link and collects the required data. 
It appends the data into an array and writes it into a googlespreadsheet via an api-call.
Unfortunately there a some difficulties with the current google api, because it is not possible to write a whole dataset into it, so there has to be made one call for each row.
This triggers a limitation mechanism of the api, in which it is only allowed to make 500 calls each 500 seconds. 
In the future, if there is no workaround for the one row per call issue, there will be coded some logic, that trigger a sleep timer every 500 calls to avoid this limitation mechanism.

SimpleSeasonDaily.py
Will perform a daily run on another link after 00:00 o'clock to get the last day into the sheets and keep the dataset up-to-date.
Is still under development.

SimpleSeasonHistory.py
This script receives the starting year from the 'Starting_at'-column trough the Simple Leagues.py-script and generates a link for every season from the startingpoint until a given year and starts the SimpleSeason.py-script for each link

