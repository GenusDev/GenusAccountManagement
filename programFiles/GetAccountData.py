import time
import json
import datetime
import pickle
from generalFunctions import makeRelativePath, copy
import pullBankAccountInfoPrograms

def compileAllData(AllAccountInfo, AccountName):
    accountData = {}
    def higherLogic(accountData):

        for eachAccount in AllAccountInfo:
            if "Update" in AllAccountInfo[eachAccount].keys():
                # if "Owner" in AllAccountInfo[eachAccount].keys():
                #     owner = AllAccountInfo[eachAccount]["Owner"]
                accountData[eachAccount] = updateBasedOnProgram(eachAccount,AllAccountInfo[eachAccount])
                print(accountData[eachAccount])

        logDataToPickle(accountData,AccountName)

        accountDataWithOutText = pullBankAccountInfoPrograms.removeText(accountData)
        return accountDataWithOutText

    def updateBasedOnProgram(accountName,eachAccountDataInfo):

        updateSignal = eachAccountDataInfo["Update"]

        if updateSignal == "normally":
            return pullBankAccountInfoPrograms.AccountGrab(eachAccountDataInfo)
        elif updateSignal == 'inputInfo':
            return eachAccountDataInfo
        elif updateSignal == 'special':
            return findRelevantAccountGrab(accountName, eachAccountDataInfo)


    def findRelevantAccountGrab(accountName, eachAccountDataInfo):

        if accountName == "$Robinhood":
            return pullBankAccountInfoPrograms.RDataPull(eachAccountDataInfo)
        elif accountName == "$Endogen":
            return pullBankAccountInfoPrograms.EndogenPositionPull(eachAccountDataInfo)


    def logDataToPickle(accountData,AccountName):

        date = datetime.date.today().strftime('%Y%m%d')
        path = makeRelativePath('AccountDataPickles/{date}{AccountName}accountData.pickle'.format(date=date,AccountName=AccountName))

        fileWrite = open(path, 'wb')
        pickle.dump(accountData, fileWrite)
        fileWrite.close()


    return higherLogic(accountData)
