
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = os.path.expanduser('~') + '/.credentials/client_secret.json'
APPLICATION_NAME = 'Portfolio Analyzer'

def _getCredentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def _getService():
    """
    Creates a Google Sheets API service object.
    """
    credentials = _getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service

def getRows(spreadsheetID):
    service = _getService()
    titles = _getTitles(spreadsheetID)
    rows = []
    for title in titles:
        data = _getSheetData(spreadsheetID, title)
        if data:
            rows.extend(data)
    return rows

def _getSheetData(sheetID, title):
    """
    Gets the data for a given spreadsheetID and sheet title.
    """
    result = _getSheet(sheetID, title)
    if not result:
        return None

    values = result.get('values', [])
    data = []
    for row in values:
        symbol = _getRowData(row, 0)
        qty = _getRowData(row, 1)
        buyRate = _getRowData(row, 2)
        buyDate = _getRowData(row, 4)
        saleRate = _getRowData(row, 5)
        saleDate = _getRowData(row, 7)
        if symbol is None or qty is None:
            continue
        data.append([symbol, qty, buyRate, buyDate, saleRate, saleDate])
    return data

def _getTitles(sheetID):
    """
    Gets a list of sheet titles for the given spreadsheetId.
    """
    names = []
    service = _getService()
    result = service.spreadsheets().get(
                spreadsheetId=sheetID, fields='sheets.properties').execute()
    if result:
        props = result['sheets']
        for prop in props:
            names.append(prop['properties']['title'])
    return names[0:2]

def _getSheet(sheetID, title):
    service = _getService()
    rangeName = title + '!A2:H'
    try:
        return service.spreadsheets().values().get(
                    spreadsheetId=sheetID, range=rangeName).execute()
    except:
        return None

def _getRowData(row, index):
    try:
        return _cleanData(row[index])
    except IndexError:
        return None

def _cleanData(data):
    if data[0] == '$':
        return str(data[1:])
    return data
