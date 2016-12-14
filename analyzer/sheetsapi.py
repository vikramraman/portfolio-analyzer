from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import helper

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

def parse_spreadsheet(sheetID, indices):
    """
    Parses a given spreadsheet.
    sheetID -- the google spreadsheet ID
    indices -- dictionary mapping the six required fields to their indices
    """
    if not sheetID or not indices:
        raise ValueError("Invalid input arguments")

    titles = _get_titles(sheetID)
    rows = []
    for title in titles:
        data = _parse_worksheet(sheetID, title, indices)
        if data:
            rows.extend(data)
    return rows

def _parse_worksheet(sheetID, title, indices):
    """
    Gets the data for a given worksheet.
    sheetID -- the google spreadsheet ID
    title -- the worksheet title
    indices -- dictionary mapping the six required fields to their indices
    """
    result = _get_worksheet(sheetID, title)
    if result:
        values = result.get('values', [])
        return helper.get_rows(values, indices)

def _get_titles(sheetID):
    """
    Gets a list of worksheet titles for the given spreadsheetId.
    """
    service = _get_service()
    result = service.spreadsheets().get(
                spreadsheetId=sheetID, fields='sheets.properties').execute()
    titles = [d['properties']['title'] for d in result['sheets'] if result]
    return titles[0:2]

def _get_worksheet(sheetID, title):
    service = _get_service()
    range_name = title + '!A2:H'
    try:
        return service.spreadsheets().values().get(
                    spreadsheetId=sheetID, range=range_name).execute()
    except:
        return None
