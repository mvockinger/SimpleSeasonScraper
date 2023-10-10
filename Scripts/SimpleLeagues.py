from bs4 import BeautifulSoup
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('SimpleSeasonScrapeClient.json', scope)
client = gspread.authorize(creds)

# Öffnen des ganzen Spreadsheets
sheet = client.open('Simple Season Scrape')
ligen = sheet.worksheet('Leagues')
#headers = ligen.get_all_records()
#print(headers)

def getLeagueTablename(country, league):
    al = ligen.get_all_records()
    for key in al:
        if(key.get('Country') == country):
            #print('Land gefunden: ', key.get('Country'))
            if(key.get('League') == league):
                #print('Liga gefunden: ', key.get('League'))
                tname = key.get('Tablename')
                return tname
    return 'NOT'

def getLeagueSuffix(tname):
    al = ligen.get_all_records()
    for key in al:
        if(tname == key.get('Tablename')):
            tsuffix = key.get('Suffix')
            return tsuffix
    
def getTablenameBySuffix(url):
    al = ligen.get_all_records()
    suffix = url.split('/alle_spiele/')
    for key in al:
        if(key.get('Suffix') in suffix[1]):
            tname = key.get('Tablename')
            return tname
    return 'NOT'

def getStartingSeasonByTablename(tname):
    al = ligen.get_all_records()
    for key in al:
        if(key.get('Tablename') in tname):
            startingSeason = key.get('Starting_at')
            return startingSeason
    return 'NOT'

def getCurrentSeasons():
    td = str(date.today())
    today = td.split('-')
    seasons = []
    if(int(today[1])<=6 and int(today[2])<=30):
        s1 = int(today[0])-1
        season1 = str(s1) + '/' + today[0]
        seasons.append(season1)
    else:
        s2 = int(today[0])+1
        season2 = today[0] + '/' + str(s2)
        seasons.append(season2)
    
    
    
    
# Entwicklung
#getLeagueTablename('Frankreich', 'Ligue 1')
#getTablenameBySuffix('https://www.weltfussball.de/alle_spiele/bundesliga-2019-2020/')
getCurrentSeasons()