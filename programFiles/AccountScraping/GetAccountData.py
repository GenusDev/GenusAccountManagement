import time
import json
import datetime
import pickle
from generalFunctions import makeRelativePath, copy
from AccountScraping import pullBankAccountInfoPrograms

def compileAllData(AllAccountInfo, AccountName):
    accountData = {}
    def higherLogic(accountData):

        for eachAccount in AllAccountInfo:
            if AccountName == '$tdjohnira':
                if "Update" in AllAccountInfo[eachAccount].keys():
                    # if "Owner" in AllAccountInfo[eachAccount].keys():
                    #     owner = AllAccountInfo[eachAccount]["Owner"]
                    accountData[eachAccount] = updateBasedOnProgram(eachAccount, AllAccountInfo[eachAccount])
                    print("printing Final Output")
                    print(accountData[eachAccount])

        logDataToPickle(accountData,AccountName)

        accountDataWithOutText = pullBankAccountInfoPrograms.removeText(accountData)
        return accountDataWithOutText

    def updateBasedOnProgram(accountName, eachAccountDataInfo):
        print(accountName)
        updateSignal = eachAccountDataInfo["Update"]

        if updateSignal == "normally":
            try:
                return pullBankAccountInfoPrograms.AccountGrab(eachAccountDataInfo)
            except:
                print("did the account pull not happen")
                return inputDirectly(accountName)

        elif updateSignal == 'inputInfo':
            return inputDirectly(accountName)
        elif updateSignal == 'special':
            try:
                return findRelevantAccountGrab(accountName, eachAccountDataInfo)
            except:
                return inputDirectly(accountName)

    def inputDirectly(accountName):
        print(accountName)
        cash = input("cash?")
        invested = input("invested?")
        Data = {
            "cash": cash,
            "invested": invested
        }
        return Data


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
