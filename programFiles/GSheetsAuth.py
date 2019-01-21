import gspread
import datetime
import oauth2client
import sys
import cryptoScripts
import os
# from ... import cryptoScripts #import from parent folder


class GenTrackrGSheets:
    def __init__(self, initials):

        self.spreadsheetId = "1eeNiVYpVGK48AQcKsFm6s9jPNumHsqcUZjRoMY5NtgY"
        self.credsUnlockKey = os.getenv("GSCODE")
        self.client = self.getAuth()
        self.initials = initials
        self.Tracker = self.client.open_by_key(self.spreadsheetId)
        self.individualTrackerSheet = self.client.open_by_key(self.spreadsheetId).worksheet(initials)
        self.allTasks =  self.pullAllTasks()


    def getAuth(self):
        credJson = cryptoScripts.decryptFileasJson(self.credsUnlockKey,'(encrypted)GoogleSheetsClientCreds.json')

        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credJson, scope)
        client = gspread.authorize(creds)
        return client


    def next_available_row(self):
        str_list = filter(None, self.individualTrackerSheet.col_values(4))  # fastest
        return str(len(list(str_list))+1)

    def lastSheetRow(self):
        str_list = filter(None, self.individualTrackerSheet.col_values(1))  # fastest
        return str(len(list(str_list)))

    def updateTasks(self):
        return "you will have to restructure the sheet scripts so it assumes the current spreadsheet unless otherwise specified as a parameter for an api call"

    def pullAllTasks(self):
        list_of_lists = self.individualTrackerSheet.get_all_values()
        return list_of_lists


    def listCurrentTasks(self):
        cell_list = self.individualTrackerSheet.range(2,7,11,10)
        i = 0
        taskNum = 0
        rowValues = []
        taskRows = []

        for eachCell in cell_list:
            i += 1
            rowValues.append(eachCell.value)
            if i% 4 == 0:
                print(taskNum, "    ",rowValues)
                taskNum += 1
                taskRows.append(rowValues)
                rowValues = []
        return taskRows


    def grabContextOptions(self):
        cell_list = self.individualTrackerSheet.range(2,5,10,5)
        return cell_list


    def listProjects(self,arg):
        projectSheet = self.client.open_by_key(self.spreadsheetId).worksheet('ProjectRanges')
        values = projectSheet.get_all_values()
        columnToChooseFrom = []
        i = 0

        for eachRow in values:
            if self.args[0] == eachRow[0]:
                columnToChooseFrom = eachRow
                for eachCell in eachRow:
                    if i > 0 and len(eachCell)>1:
                        print(i, "  ",eachCell)
                    i += 1

        projectSelectionNumb = input("Which Project (by#)?")

        projectSelection = columnToChooseFrom[int(projectSelectionNumb)]

        return projectSelection



    def createNewLine(self):
        lastRow = int(self.lastSheetRow())
        recentLineRow = int(self.next_available_row())
        newRow = recentLineRow + 1

        formattedRow = self.individualTrackerSheet.row_values(lastRow, value_render_option='FORMULA')
        formmatedRowBasedOnNewRow = []

        for eachCell in formattedRow:
            newCell = eachCell.replace(str(lastRow), str(recentLineRow))
            formmatedRowBasedOnNewRow.append(newCell)

        self.individualTrackerSheet.insert_row(formmatedRowBasedOnNewRow, index=recentLineRow,value_input_option='USER_ENTERED')

        return recentLineRow



# Create an interface for managing accounts that is flexible to adapt to anyone's accounts - yet still pull from holding co
# Create function for getting and setting account info
#
