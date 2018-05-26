#from AccountData import AllAccountInfo as AI
import os
from selenium import webdriver
from cryptoScripts import decryptFileasJson, encryptJson
import ast
import sys
import UpdateHoldingCo
import GetAccountData
import pickle
import glob
from pprint import pprint
from generalFunctions import makeRelativePath,loadOldAccountData
 # potentially have inputted at a later stage


def copy(data):
    print(data + " copied")
    os.system("echo '%s' | pbcopy" % data)

def runLookup(AI, command="none"):
    lowerKeysAI =  {k.lower(): v for k, v in AI.items()}
    # print(command)
    #if additional factors were passed in the first line
    inputedText = command.lower()
    if command == "none":
        inputedText = input("Account? -c to list commands : ").lower().replace(" ","")

    commands = {#figure out how to print out commands pretty
        "-a" : "list all accounts",
        "-c" : "list all commands",
        "-e" : "escape",
        "-updateAcc": "will update all accounts - be sure to put in account info as needed",
        "add" : "add a new account and/or data point",
        "del" : "remove a new account and/or data point",
        "loadAccountData": "Loads old account data based on date",
        "+": "commands are chained with +",
        "nameOfAccount +command" : ["account specific commands",
                                    {
                                        "+i": "list all account specific info",
                                        "+Key": "look for specific data by key",
                                        "+u": "list us*rn*me",
                                        "+p": "list p*ssw*rd (password is default output if no command provided)",
                                    }]

    }

    def shortLookUp(inputedText,accountFactor):
        if inputedText in lowerKeysAI:
            if accountFactor != "allInfo":
                try:
                    copy(lowerKeysAI[inputedText][accountFactor])
                    return lowerKeysAI[inputedText][accountFactor]
                except:
                    print(accountFactor," info not added")
            elif accountFactor == "allInfo":
                print(lowerKeysAI[inputedText])
        else:
            for each in lowerKeysAI.keys():
                if inputedText in each:
                    correctAccountQuestion = input(each+" ? y/n")
                    if correctAccountQuestion == "y":
                        correctAccount = each
                        if accountFactor != "allInfo":
                            print(lowerKeysAI[correctAccount]['Pass'])
                            copy(lowerKeysAI[correctAccount][accountFactor])
                            return lowerKeysAI[correctAccount][accountFactor]
                        elif accountFactor == "allInfo":
                            return lowerKeysAI[correctAccount]
                            break
                    elif correctAccountQuestion == "n":
                        pass
    #accountloading functions:
    def OldAccountDataRequest():
        dateInput = input("select dates (20180521) or (D)isplay dates : ")
        if dateInput == "D":
            for each in glob.glob(makeRelativePath("AccountDataPickles/*.pickle")):
                print(os.path.basename(each[:-18]))
            OldAccountDataRequest()
        else:
            try:
                oldAccountData = loadOldAccountData(dateInput)
                pprint(oldAccountData)
            except:
                print("Error of some kind, returning to main menu")
                runLookup(AI)

    def loadOldAccountData(date):
        fileRead = open(makeRelativePath('AccountDataPickles/{}accountData.pickle'.format(date)), 'rb')
        accountData = pickle.load(fileRead)
        return accountData


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
        print(inputedText)
        if " " in inputedText:
            x,y = inputedText.split(" ")
            AccountName = y
            print("worked!")
        else:
            AccountName = input("account name?: ")

        keyInputed = input("key? ('Usr','Pass','Handle','Id'): ")
        valueInputed = input("value?: ")

        try:
            currentData = AI[AccountName] #ast.literal_eval()
            print(currentData)
            AI[AccountName].update({keyInputed:valueInputed})
        except:
            AI[AccountName] = {keyInputed:valueInputed}

        print(AI[AccountName])

        encryptJson(unlockKey,AI,"(encrypted)AccountData.json")
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

        #print(AI)
        encryptJson(unlockKey,AI,"(encrypted)AccountData.json")
        runLookup(AI)


    if "updateacc" in inputedText:
        accountData = GetAccountData.compileAllData(AI)
        updateClass = UpdateHoldingCo.updateAccounts(accountData)
        updateClass.execute()

    #loadOldAccountData
    if "loadaccountdata" in inputedText: #potentiall ancrypt old data
        OldAccountDataRequest()


    if "+" in inputedText:
        x,y = inputedText.split("+")
        if "i" in y:
            shortLookUp(x,"allInfo")
        elif "u" in y:
            shortLookUp(x,"Usr")
        elif "p" in y:
            shortLookUp(x,"Pass")
        else:
            try:
                url = shortLookUp(x,y)
            except:
                print("key not found")
            # print(url)
            # if url=="None":
            #     pass
            # else:
            #     driver = webdriver.Chrome()
            #     driver.get(url)

    elif inputedText in lowerKeysAI:
        copy(lowerKeysAI[inputedText]["Pass"])


    else:
        print("Heading back to main interface")
        runLookup(AI)

def Main():
    global unlockKey
    try:
        type(sys.argv[1]) == "<class 'str'>"
    except:
        unlockKey = input("Account Key?").replace(" ","")
    else:
        unlockKey = sys.argv[1]

    try:
        AI = decryptFileasJson(unlockKey,"(encrypted)AccountData.json")
    except:
        tryAgain = input("nope - you are likely less wrong than you are sloppy - Try the code again? (y/n)")
        if 'y' in tryAgain:
            Main()
        if 'n' in tryAgain:
            print("Okay, bye Felicia")
    else:
        try:
            runLookup(AI,sys.argv[2])
        except:
            runLookup(AI)

if __name__ == '__main__':
    Main()



# figure out dual selection and
# pass in all line arguments
# do dual selection after shortLookUp
# might be interesting to integrate a decorator that allows an escape option for each function
# Take out all critical files and put them in a sub folder and shift to a github repot with encrypted file, and remove all sensitive material, and save main copy on desktop and out of the cloud, as well as key.
# figure out how to shift everything to a github account such that when downloaded everything works, after installing the dependencies
