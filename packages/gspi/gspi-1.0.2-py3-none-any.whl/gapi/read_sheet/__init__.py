import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def getsheets(sheetid,creds):
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.get(spreadsheetId=sheetid).execute()
        sheets = []
        for s in result.get('sheets',''):
            try:
                s['properties']['hidden']
            except:
                sheets.append(s['properties']['title'])
        return sheets
    except HttpError as err:
        return(err)

def get_all_data(sheetid,sheetname,creds):
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheetid,
                                    range=sheetname).execute()
        values = result.get('values', [])
        data = []
        for row in values:
            data.append(row)
        return data
    except HttpError as err:
        return(err)

def get_specific_data(sheetid,sheetname,header_name,creds):
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheetid,
                                    range=sheetname).execute()
        values = result.get('values', [])
        header_row = values[0]
        header_index = header_row.index(header_name)
        column_values = [row[header_index] for row in values[1:]]
        return column_values
    except HttpError as err:
        return(err)
