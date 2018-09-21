import glob
import os
import pickle
from AccountStructurePrograms.MSteeleAccountStructure import loadPersonalAccounts #come up with a more modular approach later
from AccountStructurePrograms.EndogenAccountStructure import loadEndogenAccounts
from generalFunctions import makeRelativePath, copy

def loadAccountDataFiles():
    AccountDataFiles = {
            "M" : "(encrypted)AccountDataMSteele.json",
            "E" : "(encrypted)AccountDataEndogen.json",
            "G" : "(encrypted)AccountDataGenus.json",
            "O" : "other"
    }
    return AccountDataFiles

# def loadAccountDataNames(whichArchive):
#     return {
#             "M" : "MSteele",
#             "E" : "Endogen",
#             "G" : "Genus"
#     }[whichArchive]

def loadAccountSheetInfo(whichArchive):
    return {
        "M" : loadPersonalAccounts(),
        "E" : loadEndogenAccounts(),
        "G" : "none available"
    }[whichArchive]

#accountloading functions:
def OldAccountDataRequest():
    dateInput = input("select dates and Name (20180521Name) or (D)isplay dates : ")
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
