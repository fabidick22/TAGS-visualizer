import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('KEAproyect-33f14b614eb8.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("Copia de TAGS v6.1.6").sheet1
