import gspread
import datetime
import oauth2client
from locale import *
from generalFunctions import makeRelativePath
from HoldingCoPositions import HoldingCoAccounts
from MSteelePersonalAccounts import PersonalAccounts #best to input it as a variable arguments eventually

class updateAccounts:
    def __init__(self, accountData):
        setlocale(LC_NUMERIC, '')

        self.accountdata = accountData

        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(makeRelativePath('GoogleSheetsClientCreds.json'), scope)
        client = gspread.authorize(creds)

        # Open a worksheet from spreadsheet with one shot
        self.HoldingCoAccountSheet = client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('AccountsBalance')
        self.PositionSheet = client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('Analysis')
        self.ShareTrackingSheet = client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('ShareTracking')
        self.PersonalAccountSheet = client.open_by_key('10o-H7l5u0BvazIs4g3Fy4NpJcb8d4X6n7vFBVs0pKCc').worksheet('Statements')

        #pullinAccountData
        self.PersonalAccounts = PersonalAccounts
        self.HoldingCoAccountSheet = HoldingCoAccounts


    def next_available_row(self,sheet):
        str_list = filter(None, sheet.col_values(1))  # fastest
        return str(len(list(str_list))+2)

    def fillLastRowofHoldingCo(self, row):
        next_row = self.next_available_row(self.HoldingCoAccountSheet)
        cell_list = self.HoldingCoAccountSheet.range(next_row,1,next_row,5)

        cell_list[0].value = datetime.date.today().strftime('%m/%d/%Y')
        cell_list[1].value = row['Account']
        cell_list[2].value = row['Invested']
        cell_list[3].value = row['Cash']
        cell_list[4].value = "={}+{}".format(row['Cash'], row['Invested'])

        self.HoldingCoAccountSheet.update_cells(cell_list, value_input_option='USER_ENTERED')

    def setValuationCell(self, row):
            next_row = self.next_available_row(self.HoldingCoAccountSheet)
            cell_list = self.HoldingCoAccountSheet.range(next_row,1,next_row,5)

            cell_list[0].value = datetime.date.today().strftime('%m/%d/%Y')
            cell_list[1].value = row['Account']
            cell_list[2].value = row['Invested']
            cell_list[3].value = row['Cash']
            cell_list[4].value = "={}+{}".format(row['Cash'], row['Invested'])

            self.HoldingCoAccountSheet.update_cells(cell_list, value_input_option='USER_ENTERED')


    def grabBalancesOfAccounts(self,person):
        PersonalCell = self.PositionSheet.find(person)
        PersonalBalance = self.PositionSheet.range(PersonalCell.row,4)
        return PersonalBalance[0].value

    def updateHCAccountData(self):
        HoldingData = {
            'positions':{
                "Matt" : self.grabBalancesOfAccounts("Matt"),
                "John" : self.grabBalancesOfAccounts("John"),
                "BnB" : self.grabBalancesOfAccounts("BnB"),
                "Lau" : self.grabBalancesOfAccounts("Lau")
            }
        }

        return HoldingData

    def updateHoldingPositions(self):
        HoldingData = self.updateHCAccountData()
        self.accountdata['HoldingData'] = HoldingData

        self.PersonalAccounts.append({
            "Account": "HoldingData",
            "Debit": float(self.accountdata['HoldingData']['positions']['Matt']) + float(self.accountdata['HoldingData']['positions']['BnB'])
        })
        print(self.PersonalAccounts)

    def fillLastRowofPersonalAccounts(self, row):
        next_row = int(self.next_available_row(self.PersonalAccountSheet)) - 1
        cell_list = self.PersonalAccountSheet.range(next_row,1,next_row,5)

        cell_list[0].value = datetime.date.today().strftime('%m/%d/%Y')
        cell_list[1].value = row['Account']
        cell_list[2].value = ""
        try:
            cell_list[3].value = row['Debit']
        except:
            pass
        try:
            cell_list[4].value = row['Credit']
        except:
            pass

        self.PersonalAccountSheet.update_cells(cell_list, value_input_option='USER_ENTERED')

    def execute(self):
        self.updateHoldingPositions()
        for eachRow in  self.HoldingCoAccounts:
            print (eachRow)
            self.fillLastRowofHoldingCo(eachRow)
        for eachRow in  self.PersonalAccounts:
            print (eachRow)
            self.fillLastRowofPersonalAccounts(eachRow)


# Create an interface for managing accounts that is flexible to adapt to anyone's accounts - yet still pull from holding co
# Create function for getting and setting account info
#
