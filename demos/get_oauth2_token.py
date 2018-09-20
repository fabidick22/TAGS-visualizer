'''
    This script will attempt to open your webbrowser,
    perform OAuth 2 authentication and print your access token.

    It depends on two libraries: oauth2client and gflags.

    To install dependencies from PyPI:

    $ pip install python-gflags oauth2client

    Then run this script:

    $ python get_oauth2_token.py
    
    This is a combination of snippets from:
    https://developers.google.com/api-client-library/python/guide/aaa_oauth
'''

from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.file import Storage
import requests, gspread
import os, ast
from oauth2client.service_account import ServiceAccountCredentials


def authenticate_google_docs():
    f = open(os.path.join('utplApps-2e6b0704e6bf.json'), 'rb')
    SIGNED_KEY = f.read()
    f.close()
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
    #scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    #credentials = ServiceAccountCredentials.from_p12_keyfile('dicksonarmijos@gmail.com', os.path.join('KEAproyect-a1fdc21d964c.p12'), scope)
    #credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join('KEAproyect-b4ff9f7e595f.json'), scope)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join('utplApps-2e6b0704e6bf.json'), scope)

    data = {
        'refresh_token' : '1/YVTM7_qH7J4FvYqpqllLnP51vpXbBT2wbifbHhul2g2WIN1fEis-qn8PjfIMNpZ2',
        'client_id' : '578335401812-hjaadped4a4peakui54npumc0jukpitj.apps.googleusercontent.com',
        'client_secret' : 'GghbKvIsnXw_h4Mzbb4RZSZG',
        'grant_type' : 'refresh_token',
    }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)
    credentials.access_token = ast.literal_eval(r.text)['access_token']

    gc = gspread.authorize(credentials)
    return gc

CLIENT_ID = '578335401812-hjaadped4a4peakui54npumc0jukpitj.apps.googleusercontent.com'
CLIENT_SECRET = 'GghbKvIsnXw_h4Mzbb4RZSZG'


flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           scope='https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
                           redirect_uri='http://example.com/auth_return')
print("permite:")
print(flow.step1_get_authorize_url())

storage = Storage('creds.data')

credentials = tools.run_flow(flow, storage)

print("access_token: %s"%credentials.access_token)

gc = authenticate_google_docs()

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/11oq-zIk6KULgIv9_T73U7ghNkm3Z69oq4T_g-cS4y1s/edit#gid=0')
worksheet = sh.get_worksheet(0)
print(worksheet.col_values(1))


