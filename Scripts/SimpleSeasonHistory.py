import SimpleLeagues
import SimpleSeason
import time

# Jahr eingeben, bis wann die Daten geholt werden sollen -> z.B. 2020 für 2019/2020
untilyear = 2020
# Liga eingeben, die gescraped werden sollen
tablename = 'TUN1'

baseurl = 'https://www.weltfussball.de/alle_spiele/'
leagueurl = SimpleLeagues.getLeagueSuffix(tablename)
startingseason = SimpleLeagues.getStartingSeasonByTablename(tablename)
if(startingseason == 'NOT'):
    print('Start Saison nicht in das Spreadsheet eintragen!')
else:
    print('Season History Scrape startet..')
    if('/' in str(startingseason)):
        years = startingseason.split('/')
        #print(years)
        years = list(map(int, years))
        while(years[0] < untilyear):
            y1 = str(years[0])
            y2 = str(years[1])
            url = baseurl+leagueurl+y1+'-'+y2+'/'
            years[0] += 1
            years[1] += 1
            # hier den scrape aufrufen
            SimpleSeason.getSeasonSimple(url)
            time.sleep(300)
    else:
        year = startingseason
        while(year < untilyear):
            url = baseurl+leagueurl+str(year)+'/'
            year += 1
            # hier den scrape aufrufen
            SimpleSeason.getSeasonSimple(url)
    print('Season History Scrape beendet.')