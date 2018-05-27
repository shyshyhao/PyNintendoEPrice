# -*- coding: utf-8 -*-

# Use google/google-api-python-client to storage data into google sheet
# We Save the All of games which nintendo games and these game tw name.

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetApiPipeline(object):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # Setup the Sheets API
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        store = file.Storage('../client_secret.json')
        creds = store.get()
        # print(creds)
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('../client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        # Call the Sheets API
        SPREADSHEET_ID = '1nKH1bfETw7NIUl2EzOu_1L_sgd7hcom3DFMsZ3lb-k0'
        RANGE_NAME = 'Class Data!A2:E'
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                    range=RANGE_NAME).execute()

        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s' % (row[0], row[4]))
        return item

if __name__ == "__main__":
    pipline = GoogleSheetApiPipeline()
    pipline.process_item(None, None)