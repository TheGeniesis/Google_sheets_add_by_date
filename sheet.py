from flask import request, jsonify
from sheetfu import SpreadsheetApp

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def create():
    data = request.get_json()
    date = data['date']
    time = data['time']
    temperature = data['temperature']
    humility = data['humility']
    voltage = data['voltage']

    sheetname = 'Sheet1'
    file_name = date

    creds = False
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    param = {'q': 'mimeType="application/vnd.google-apps.spreadsheet"'}
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(**param,
                                   pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    spreadsheet_app = SpreadsheetApp('secrets.json')
    sheet = None
    if items:
        for item in items:
            if item['name'] == file_name:
                sheet = spreadsheet_app.open_by_id(item['id']).get_sheet_by_name(sheetname)

    if not sheet:
        sheet = spreadsheet_app.create(file_name, editor="<email>")
        selected_spread_sheet = spreadsheet_app.open_by_id(sheet.id)

        sheet = selected_spread_sheet.get_sheet_by_name(sheetname)
        sheet.get_range(1, 1).set_value('Date')
        sheet.get_range(1, 2).set_value('Time')
        sheet.get_range(1, 3).set_value('Temperature')
        sheet.get_range(1, 5).set_value('Voltage')

    last_row = sheet.get_data_range().coordinates.number_of_rows + 1

    sheet.get_range(last_row, 1).set_value(date)
    sheet.get_range(last_row, 2).set_value(time)
    sheet.get_range(last_row, 3).set_value(temperature)
    sheet.get_range(last_row, 4).set_value(humility)
    sheet.get_range(last_row, 5).set_value(voltage)

    resp = jsonify(success=True)

    return resp

