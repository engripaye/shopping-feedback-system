import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsClient:
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
        creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=creds)
        self.sheet = self.service.spreadsheets()
        self.spreadsheet_id = spreadsheet_id

    def append_row(self, range_: str, row_values: List[str], value_input_option: str = 'RAW'):

        """
        Appends a single row(List of values to set)
        """

        body = {"values": [row_values]}
        requests = self.sheet.values().append(
            spreadsheetId=self.spreadsheet_id,
            range=range_,
            valueInputOption=value_input_option,
            insertDataOption='INSERT_ROWS',
            body=body
        )

        return requests.execute()