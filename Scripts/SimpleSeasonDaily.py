from bs4 import BeautifulSoup
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import SimpleLeagues
from datetime import datetime, timedelta
import time

# Ergebnisse des Vortages scrapen -> spiele sind spätestens nach 03:00 Uhr beendet
# Link zum Vortag generieren
# https://www.weltfussball.de/tore_tabellen/jahr/monat/tag/ -> monat mit 3 Buchstaben
thedaybeforetodayplusdate = str(datetime.now() - timedelta(1))
thedaybeforetoday = thedaybeforetodayplusdate.split()
# z.B. yesterday ['2021', '02', '27']
yesterday = thedaybeforetoday[0].split('-')
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

yesterdaysUrl = 'https://www.weltfussball.de/tore_tabellen/' + yesterday[0] + '/' + months[int(yesterday[1])-1] + '/' + yesterday[2] + '/'

# GSpread Autentifizierung
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('SimpleSeasonScrapeClient.json', scope)
client = gspread.authorize(creds)

def getDailyUpdate(url):
    # Idee: Erkennen der Liga, falls Vorhanden Link weitergeben an eigene Routine
    # -> /wettbewerb/... scrapen und Daten via Datum abgleichen
    # -> Methode(link, tname, datum)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    tables = soup.find_all('table', class_="standard_tabelle")
    yesterdaysMatches = tables[0]
    rows = yesterdaysMatches.find_all('tr')
    todaysLeagues = []
    for row in rows:
        if(len(row) == 7):
            print(row.get_text().split())
        #if(row.find('th') != 'None'):
            #print(row.get_text().split())
    


    #tname = SimpleLeagues.getLeagueTablename()

# Entwicklung
#getDailyUpdate('https://www.weltfussball.de/tore_tabellen/2021/apr/15/')