
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

def _get_credentials():
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

def _get_service():
    """
    Creates a Google Sheets API service object.
    """
    credentials = _get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service

def parse_spreadsheet(sheetID):
    service = _get_service()
    titles = _get_titles(sheetID)
    rows = []
    for title in titles:
        data = _parse_worksheet(sheetID, title)
        if data:
            rows.extend(data)
    return rows

def _parse_worksheet(sheetID, title):
    """
    Gets the data for a given worksheet.
    """
    result = _get_worksheet(sheetID, title)
    if not result:
        return None

    values = result.get('values', [])
    data = []
    for row in values:
        symbol = _get_row_data(row, 0)
        qty = _get_row_data(row, 1)
        buy_rate = _get_row_data(row, 2)
        buy_date = _get_row_data(row, 4)
        sale_rate = _get_row_data(row, 5)
        sale_date = _get_row_data(row, 7)
        if symbol is None or qty is None:
            continue
        data.append([symbol, qty, buy_rate, buy_date, sale_rate, sale_date])
    return data

def _get_titles(sheetID):
    """
    Gets a list of worksheet titles for the given spreadsheetId.
    """
    names = []
    service = _get_service()
    result = service.spreadsheets().get(
                spreadsheetId=sheetID, fields='sheets.properties').execute()
    if result:
        props = result['sheets']
        for prop in props:
            names.append(prop['properties']['title'])
    return names[0:2]

def _get_worksheet(sheetID, title):
    service = _get_service()
    range_name = title + '!A2:H'
    try:
        return service.spreadsheets().values().get(
                    spreadsheetId=sheetID, range=range_name).execute()
    except:
        return None

def _get_row_data(row, index):
    try:
        return _clean_data(row[index])
    except IndexError:
        return None

def _clean_data(data):
    if data[0] == '$':
        return str(data[1:])
    return data
