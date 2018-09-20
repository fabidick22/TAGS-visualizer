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
from arquitecturaApps import settings as stt

def authenticate_google_docs():
    urlJson=stt.BASE_DIR+"/dataOfTwitter/keys/your-app-2e6b0704e6bf.json"
    f = open(urlJson, 'rb')
    SIGNED_KEY = f.read()
    f.close()
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
    #scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(urlJson, scope)

    data = {
        'refresh_token' : 'your-token-hul2g2WIN1fEis-qn8PjfIMNpZ2',
        'client_id' : 'your-client_id.apps.googleusercontent.com',
        'client_secret' : 'Cliente-secret-h4Mzbb4RZSZG',
        'grant_type' : 'refresh_token',
    }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)
    credentials.access_token = ast.literal_eval(r.text)['access_token']

    gc = gspread.authorize(credentials)
    return gc

CLIENT_ID = '578335401812itj.apps.googleusercontent.com'
CLIENT_SECRET = 'GghbKvIsnXw_h4M'


flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           scope='https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
                           redirect_uri='http://example.com/auth_return')

