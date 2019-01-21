import gspread
import datetime
import oauth2client
from cryptoScripts import decryptFileasJson
from locale import *
from generalFunctions import makeRelativePath


class updateAccountsForPermissions:
    def __init__(self, sheetInfo="noneProvided", StructuredData="noneInputted"):
        setlocale(LC_NUMERIC, '')

        self.credsUnlockKey = 'guued' # input("Creds Unlock Key?")

        self.client = self.getAuth()
        # Open a worksheet from spreadsheet with one shot

        # self.EnodgenAccountSheet = client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('AccountsBalance')
        # self.PositionSheet = client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('Analysis')
        self.ShareTrackingSheet = self.client.open_by_key('1Qjl_H4Mf7ChN0UqricRmArzdjIiXQ6fnTIq_OZqKrbU').worksheet('ShareTracking')
        #self.PersonalAccountSheet = self.client.open_by_key('10o-H7l5u0BvazIs4g3Fy4NpJcb8d4X6n7vFBVs0pKCc').worksheet('Statements')


    def getAuth(self):

        credJson = decryptFileasJson(self.credsUnlockKey,'(encrypted)GoogleSheetsClientCreds.json')

        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credJson, scope)
        client = gspread.authorize(creds)
        return client

    def changePermissions(self):
        permissions = self.client.list_permissions('10o-H7l5u0BvazIs4g3Fy4NpJcb8d4X6n7vFBVs0pKCc')
        print(permissions)

permisionRequest = updateAccountsForPermissions()

permisionRequest.changePermissions()
