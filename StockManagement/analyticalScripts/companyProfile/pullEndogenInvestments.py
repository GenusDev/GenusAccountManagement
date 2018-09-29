import sys
sys.path.append('../../../../GenusAccountManagement/programFiles')
import loadAccountDataFiles


def EndogenAccountDataPull():
    accountData = loadAccountDataFiles.OldAccountDataRequest("20180828Endogen")

    def formatData(accountData):
        positionDataOrganized = {}
        for eachAccount in accountData:
            print(accountData[eachAccount].keys())
            if "positions" in accountData[eachAccount].keys():
                positions = accountData[eachAccount]['positions']
                positionDataOrganized.update(positions)
        return positionDataOrganized


    positionData = formatData(accountData)
    return positionData
