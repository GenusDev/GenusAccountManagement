import gspread
import datetime
import oauth2client
from cryptoScripts import decryptFileasJson
from locale import *
from generalFunctions import makeRelativePath


#you could structure the spreadsheets so they are always outputted the Same
# you could potentially let HoldingCo be a bit different and have specific programs for it, that
# are separate

class updateAccounts:
    def __init__(self, sheetInfo="noneProvided", StructuredData="noneInputted"):
        setlocale(LC_NUMERIC, '')

        self.credsUnlockKey = input("Creds Unlock Key?")

        self.client = self.getAuth()
        self.sheetInfo = sheetInfo
        self.StructuredData = StructuredData

        # Open a worksheet from spreadsheet with one shot
        # self.EnodgenAccountSheet = client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('AccountsBalance')
        # self.PositionSheet = client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('Analysis')
        # self.ShareTrackingSheet = client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('ShareTracking')
        # self.PersonalAccountSheet = client.open_by_key('10o-H7l5u0BvazIs4g3Fy4NpJcb8d4X6n7vFBVs0pKCc').worksheet('Statements')


    def getAuth(self):

        credJson = decryptFileasJson(self.credsUnlockKey,'(encrypted)GoogleSheetsClientCreds.json')

        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credJson, scope)
        client = gspread.authorize(creds)
        return client


    def updateSheets(self):
        spreadsheetId = self.sheetInfo["spreadsheetId"]
        worksheet = self.sheetInfo["worksheets"][0]

        self.AccountSheet = self.client.open_by_key(spreadsheetId).worksheet(worksheet)


        for eachAccount in self.StructuredData:
            print (eachAccount)
            self.fillLastRow(eachAccount)

        if self.sheetInfo['account'] == "Endogen":
            self.setValuationCell()


    def next_available_row(self,sheet):
        str_list = filter(None, sheet.col_values(1))  # fastest
        return str(len(list(str_list))+2)

    def pullEndogenAccountSpecificData(self,ID):
        self.AccountBalanceSheet = self.client.open_by_key("1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU").worksheet("Analysis")
        MemberIDCell = self.AccountBalanceSheet.find(ID)
        memberPositionCell = self.AccountBalanceSheet.cell(MemberIDCell.row,5)
        return memberPositionCell.value


    def setValuationCell(self):
        self.ShareTrackingSheet = self.client.open_by_key("1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU").worksheet("ShareTracking")

        next_row = self.next_available_row(self.ShareTrackingSheet)
        cell_list = self.ShareTrackingSheet.range(int(next_row)-1,1,int(next_row)-1,10)
        row = cell_list[0].row

        cell_list[0].value = datetime.date.today().strftime('%m/%d/%Y')
        cell_list[1].value = 'Valuation'
        cell_list[2].value = ''
        cell_list[3].value = 'Valuation'
        cell_list[4].value = 'Valuation'
        cell_list[5].value = ''
        cell_list[6].value = '=if(B{row}="Valuation",iferror(sum(query(AccountsBalance!$A$1:$E,"select E where A = date '.format(row=row)+"'"+'"& text(A{row},'.format(row=row)+ '"yyyy-mm-dd"'+')& '+'"'+"'"+'"'+',0)),G{rowAbove}),G{rowAbove}+F{row})'.format(row=row,rowAbove=row-1)
        cell_list[7].value = ''
        cell_list[8].value = '=I{}'.format(row-1)
        cell_list[9].value = '=G{row}/I{row}'.format(row=row)

        self.ShareTrackingSheet.update_cells(cell_list, value_input_option='USER_ENTERED')


    def fillLastRow(self,AccountDataValue):
        next_row = int(self.next_available_row(self.AccountSheet)) - 1
        cell_list = self.AccountSheet.range(next_row,1,next_row,5)

        cell_list[0].value = datetime.date.today().strftime('%m/%d/%Y')
        i = 1
        sum = 0
        for eachFactor in AccountDataValue:
            print(eachFactor)
            input = AccountDataValue[eachFactor]
            cell_list[i].value = input
            i += 1
            print(type(AccountDataValue[eachFactor]))
            if eachFactor == "Credit":
                input = input*-1

            if isinstance(input, float) or isinstance(input, int):
                sum += input
        # i += 1
        cell_list[i].value = sum

        self.AccountSheet.update_cells(cell_list, value_input_option='USER_ENTERED')



# Create an interface for managing accounts that is flexible to adapt to anyone's accounts - yet still pull from holding co
# Create function for getting and setting account info
#
