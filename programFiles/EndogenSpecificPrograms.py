


# pull position data for each account


pull data from spreadsheet

take name of account holder from account structure

key into sheet data for accountHolder


class PullPositionData:
    def __init__(self, sheetInfo, StructuredData):
        setlocale(LC_NUMERIC, '')

        self.StructuredData = StructuredData

        client = self.getAuth()
        spreadsheetId = "1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU"
        worksheet = "AccountsBalance"

        self.AccountBalanceSheet = client.open_by_key(spreadsheetId).worksheet(worksheet)

    def getAuth(self):

        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(makeRelativePath('GoogleSheetsClientCreds.json'), scope)
        client = gspread.authorize(creds)
        return client

    def pullAccountSpecificData(name):






# set valuation
