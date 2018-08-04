#from AccountData import AllAccountInfo as AI
import os
from selenium import webdriver
from cryptoScripts import decryptFileasJson, encryptJson
import loadAccountDataFiles
import ast
import sys
import UpdatePositions
import GetAccountData
from generalFunctions import makeRelativePath, copy, gitPush, gitPull
from AccountStructurePrograms.StructureAccounts import StructureAccounts


from pprint import pprint
from commandOptions import commands


def runLookup(AI, command="none"):
    lowerKeysAI =  {k.lower(): v for k, v in AI.items()}
    inputedText = command.lower()
    if command == "none":
        inputedText = input("Account? -c to list commands : ").lower().replace(" ","")

    if "-a" in inputedText:
        for each in AI:
            print (each)
        runLookup(AI)

    elif "-c" in inputedText:
        pprint (commands)
        runLookup(AI)

    elif "-e" in inputedText:
        print("bye Felicia")
        quit()

    if "add" in inputedText:

        if " " in inputedText:
            x,y = inputedText.split(" ")
            AccountName = y
        else:
            AccountName = input("account name?: ")

        keyInputed = input("key? ('Usr','Pass','Handle','Id'):, add in new dict with {} ")

        if "{" in keyInputed:
            AI[AccountName] = ast.literal_eval(keyInputed)
        else:
            valueInputed = input("value?: ")
            try:
                currentData = AI[AccountName]
                pprint(currentData)
                AI[AccountName].update({keyInputed:valueInputed})
            except:
                AI[AccountName] = {keyInputed:valueInputed}

        pprint(AI[AccountName])



        encryptJson(unlockKey,AI,accountDataFileName)
        gitPush()
        runLookup(AI)

    elif "del" in inputedText:
        delChoice = input("Remove (A)ccount or account (D)ata?: ")
        delAccountName = "None"
        delAccountKey = "None"
        if "A" in delChoice:
            for each in AI.keys():
                print (each)
            delAccountName = input("Account name?: ")
            pprint(AI[delAccountName])
            if delAccountName in AI.keys():
                AI.pop(delAccountName)
            else:
                print("Account name not found")
        elif "D" in delChoice:
            delAccountName = input("Account name?: ")
            delAccountKey = input("Data key?: ")
            pprint(AI[delAccountName])
            if delAccountName in AI.keys():
                if delAccountKey in AI[delAccountName].keys():
                    AI[delAccountName].pop(delAccountKey)
                else:
                    print("Data key not found")
            else:
                print("Account name not found")
        else:
            print("not an option")

        encryptJson(unlockKey,AI, accountDataFileName)
        gitPush()
        runLookup(AI)


    if "updateacc" in inputedText:
        sheetInfo = loadAccountDataFiles.loadAccountSheetInfo(whichAccountArchive)
        AccountName = sheetInfo["account"]
        accountData = GetAccountData.compileAllData(AI,AccountName)
        # accountData = loadAccountDataFiles.loadOldAccountData("20180714MSteele")
        # pprint(accountData)

        StructuredData = StructureAccounts(sheetInfo,accountData)
        # pprint(StructuredData)

        updatedAccounts = UpdatePositions.updateAccounts(sheetInfo,StructuredData)
        updatedAccounts.updateSheets()


    #loadOldAccountData
    if "loadaccountdata" in inputedText: #potentially encrypt old data
        loadAccountDataFiles.OldAccountDataRequest()


    if "+" in inputedText: #reformat this as a recursive function for allowing short lookups
        x,y = inputedText.split("+")
        if "i" in y:
            shortLookUp(x,"allInfo",lowerKeysAI)
        elif "u" in y:
            shortLookUp(x,"Usr",lowerKeysAI)
        elif "p" in y:
            shortLookUp(x,"Pass",lowerKeysAI)
        else:
            try:
                url = shortLookUp(x,y,lowerKeysAI)
            except:
                print("key not found")
            # print(url)
            # if url=="None":
            #     pass
            # else:
            #     driver = webdriver.Chrome()
            #     driver.get(url)

    elif inputedText in lowerKeysAI:
        print("going straight to copy")
        copy(lowerKeysAI[inputedText]["Pass"])


    elif inputedText not in lowerKeysAI:
        shortLookUp(inputedText,"allInfo",lowerKeysAI)

def shortLookUp(inputedText,accountFactor,lowerKeysAI):
    if inputedText in lowerKeysAI:
        if accountFactor != "allInfo":
            try:
                copy(lowerKeysAI[inputedText][accountFactor])
                return lowerKeysAI[inputedText][accountFactor]
            except:
                print(accountFactor," info not added")
        elif accountFactor == "allInfo":
            pprint(lowerKeysAI[inputedText])
    else:
        for each in lowerKeysAI.keys():
            if inputedText in each:
                print("Let me try to guess")
                correctAccountQuestion = input(each+" ? y/n : ")
                if correctAccountQuestion == "y":
                    correctAccount = each
                    if accountFactor != "allInfo":
                        print(lowerKeysAI[correctAccount]['Pass'])
                        copy(lowerKeysAI[correctAccount][accountFactor])
                        return lowerKeysAI[correctAccount][accountFactor]
                    elif accountFactor == "allInfo":
                        pprint (lowerKeysAI[correctAccount])
                        break
                elif correctAccountQuestion == "n":
                    pass


def Main():

    def higherLogic():
        gitPull()
        global accountDataFileName
        accountDataFileName = IdentifyArchive()
        unlockKey = checkForKey()

        decryptFile(accountDataFileName, unlockKey)


    def IdentifyArchive():
        listOfArchives = loadAccountDataFiles.loadAccountDataFiles()
        #if key in dict - test first before implementing
        global whichAccountArchive
        try:
            whichAccountArchive = sys.argv[1]
        except:
            pprint(listOfArchives)
            whichAccountArchive = input("Which archive?").replace(" ","")

        if whichAccountArchive in listOfArchives.keys():
            accountDataFileName = listOfArchives[whichAccountArchive]
        else:
            print("not in the list")
            IdentifyArchive()

        return accountDataFileName


    def checkForKey():
        global unlockKey
        try:
            unlockKey = sys.argv[2]
            type(unlockKey) == "<class 'str'>"
        except:
            unlockKey = input("Account Archive Key?").replace(" ","")

        return unlockKey

    def decryptFile(accountDataFileName,unlockKey):

        try:
            AI = decryptFileasJson(unlockKey,accountDataFileName)
        except:
            tryAgain = input("nope - you are likely less wrong than you are sloppy - Try the code again? (y/n)")
            if 'y' in tryAgain:
                unlockKey = input("Account Archive Key?").replace(" ","")
                Main()
            if 'n' in tryAgain:
                print("Okay, bye Felicia")
        else:
            try:
                runLookup(AI,sys.argv[3])
            except:
                runLookup(AI)


    higherLogic()



if __name__ == '__main__':
    Main()



# figure out dual selection and
# pass in all line arguments
# do dual selection after shortLookUp
# might be interesting to integrate a decorator that allows an escape option for each function
# Take out all critical files and put them in a sub folder and shift to a github repot with encrypted file, and remove all sensitive material, and save main copy on desktop and out of the cloud, as well as key.
# figure out how to shift everything to a github account such that when downloaded everything works, after installing the dependencies
