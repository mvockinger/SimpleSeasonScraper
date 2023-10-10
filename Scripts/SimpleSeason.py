from bs4 import BeautifulSoup
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import SimpleLeagues
import time

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('SimpleSeasonScrapeClient.json', scope)
client = gspread.authorize(creds)

def getSeasonSimple(url):

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    sn = soup.find('h1')
    season_name = sn.get_text().split(' » ')

    #season_name[0] -> Bundesliga, season_name[1] -> alle anderen Ligen
    if(len(season_name) == 2):
        season_name.insert(0,'Deutschland')

    # Das Jahr der Saison
    sns = season_name[1].split()
    sn = sns[-1:]
    s = sn[0]

    l = len(season_name[1])
    lname = season_name[1][:l-len(s)-1]

    # Öffnen des ganzen Spreadsheets
    sheet = client.open('Simple Season Scrape')
    # Öffnen des gewünschten Worksheets
    tn = SimpleLeagues.getLeagueTablename(season_name[0], lname)
    if(tn != 'NOT'):
        print('Scrape gestartet für', tn, 'Saison:', s)
        wks = sheet.worksheet(tn)
        tables = soup.find_all('table', class_='standard_tabelle')
        season = tables[0]
        mds = season.find_all('tr')
        matchdays = []
        matchday = ''
        date = ''
        for md in mds:
            match = []
            if('Spieltag' in md.get_text()):
                matchday = md.get_text().strip()
            else: 
                match.append(matchday)
                m = md.get_text().strip()
                match.extend(m.splitlines())
                if(len(match) == 8):
                    date = match[1]
                else:
                    match.insert(1,date)
                if(len(match) == 8):
                    # Damit keine Matches im Vorhinein in die Tabelle kommen, ohne dieses if werden auch bereits terminierte matches in das spreadsheet geschrieben
                    # nicht ausgetragene Matches kommen auch nicht in das spreadsheet
                    if(match[7].strip() == '-:-' or match[7].strip() == 'n.gesp.' or match[7].strip() == 'annull.' or match[7].strip() == 'verl.'):
                        pass
                    else:
                        if(match[7].strip() == 'abgebr.'):
                            goals = ['-','-']
                            halftimescore = ['-','-','Spiel Abgebrochen']
                        else:
                            score = match[7].split()

                            # Enstand -> fulltimescore[0] - Tore Heimteam, fulltimescore[1] - Tore Auswärtsteam
                            goals = score[0].split(':')
                            halftimescore = []
                            if(len(score) == 2):
                                # Halbzeitstand -> halftimescore = [0] - Tore Heimteam, halftimescore[1] - Tore Auswärtsteam  -> Prüfen ob vorhanden
                                if('(' in score[1] and ')' in score[1]):
                                    hs = score[1].split(':')
                                    homeHalftime = hs[0]
                                    halftimescore.append(homeHalftime[1:])
                                    awayHalftime = hs[1]
                                    halftimescore.append(awayHalftime[:-1])
                                elif(score[1] == 'Wert.'):
                                    halftimescore = ['-','-', 'Wertung']
                            else:
                                halftimescore = ['-','-']
                        goals.extend(halftimescore)
                        match = match[:-1]
                        match.extend(goals)
                        matchdays.append(match)

        # Saison wie im GSheet erstellen
        seasonsimple = []
        for m in matchdays:
            matchsimple = []
            matchsimple.append(s)
            matchsimple.append(m[0])
            matchsimple.append(m[1])
            matchsimple.append(m[3])
            matchsimple.append(m[7])
            matchsimple.append(m[8])
            matchsimple.append(m[5])
            matchsimple.append(m[9])
            matchsimple.append(m[10])
            seasonsimple.append(matchsimple)
        #print(seasonsimple)
        #appendData(wks, seasonsimple, tn)

        for m in seasonsimple:
            # falls script abstürzt if Bedingung anpassen
            fm = m[1].split('.')
            if(int(fm[0]) > 0):
                wks.append_row(m)
        print('Saison', s, 'für', tn, 'fertig!')
        
    else:
        print('Liga nicht erkannt')

# Entwicklung
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2009-2010/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2010-2011/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2011-2012/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2012-2013/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2013-2014/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2014-2015/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2015-2016/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2016-2017/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2017-2018/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2018-2019/')
getSeasonSimple('https://www.weltfussball.de/alle_spiele/eng-league-one-2019-2020/')