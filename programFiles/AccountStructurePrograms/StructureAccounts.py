
def StructureAccounts(sheetInfo, AllAccountData):
    print("printing all account Data")
    print(AllAccountData)
    print(type(AllAccountData))

    def higherLogic(AllAccountData):
        dataOrganized = []
        print("printing all account Data")
        print(AllAccountData)
        for eachAccount in AllAccountData:
            print(eachAccount)

            structureBuildout = {
                "AccountName" : eachAccount.strip("$")
            }

            for eachDataType in sheetInfo["structure"]:
                type = sheetInfo["structure"][eachDataType]
                if type not in structureBuildout:
                    structureBuildout.update({
                        type : addUpByType(type,AllAccountData[eachAccount])
                    })

            dataOrganized.append(structureBuildout)

        return dataOrganized

    def addUpByType(type, AccountSpecficData):
        totalByType = 0

        for eachEntryKey in AccountSpecficData:

            if eachEntryKey in sheetInfo["structure"].keys():
                if sheetInfo["structure"][eachEntryKey] == type:
                    if isinstance(AccountSpecficData[eachEntryKey],str) == True:
                        data2Add = float(AccountSpecficData[eachEntryKey].strip("$").replace(",",""))
                    elif isinstance(AccountSpecficData[eachEntryKey],int):
                        data2Add = float(AccountSpecficData[eachEntryKey])
                    else:
                        data2Add = float(AccountSpecficData[eachEntryKey])
                    totalByType += data2Add
                else:
                    pass
            else:
                pass

            # try:
            #     print(sheetInfo["structure"][eachEntryKey])#
            #

            #         print("accountInfoToAdd"+AccountSpecficData[eachEntryKey])

                    #
            # except:
            #     pass
            print("working!")

        return totalByType

    return higherLogic(AllAccountData)
